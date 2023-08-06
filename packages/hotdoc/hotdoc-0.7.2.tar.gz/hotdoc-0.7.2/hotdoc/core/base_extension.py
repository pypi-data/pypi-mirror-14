# -*- coding: utf-8 -*-
#
# Copyright © 2015,2016 Mathieu Duponchelle <mathieu.duponchelle@opencreed.com>
# Copyright © 2015,2016 Collabora Ltd
#
# This library is free software; you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation; either version 2.1 of the License, or (at your option)
# any later version.
#
# This library is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this library.  If not, see <http://www.gnu.org/licenses/>.

"""
Utilities and baseclasses for extensions
"""

import os

from collections import defaultdict, OrderedDict

from hotdoc.core.doc_tree import DocTree
from hotdoc.core.file_includer import find_md_file, resolve_markdown_signal
from hotdoc.core.exceptions import BadInclusionException
from hotdoc.formatters.html_formatter import HtmlFormatter
from hotdoc.utils.utils import OrderedSet
from hotdoc.utils.configurable import Configurable
from hotdoc.utils.loggable import debug, info, warn, error, Logger
from hotdoc.core.symbols import Symbol

Logger.register_error_code('smart-index-missing', BadInclusionException,
                           domain='base-extension')


# pylint: disable=too-few-public-methods
class ExtDependency(object):
    """
    Represents a dependency on another extension.

    If not satisfied, the extension will not be instantiated.

    See the `BaseExtension.get_dependencies` static method documentation
    for more information.

    Attributes:
        dependency_name: str, the name of the extension depended on.
        is_upstream: bool, if set to true hotdoc will arrange for
            the extension depended on to have its `BaseExtension.setup`
            implementation called first. Circular dependencies will
            generate an error.
    """

    def __init__(self, dependency_name, is_upstream=False):
        """
        Constructor for `BaseExtension`.

        Args:
            dependency_name: str, see `ExtDependency.dependency_name`
            is_upstream: bool, see `ExtDependency.is_upstream`
        """
        self.dependency_name = dependency_name
        self.is_upstream = is_upstream


class BaseExtension(Configurable):
    """
    All extensions should inherit from this base class

    Attributes:
        EXTENSION_NAME: str, the unique name of this extension, should
            be overriden and namespaced appropriately.
        doc_repo: doc_repo.DocRepo, the DocRepo instance which documentation
            hotdoc is working on.
        formatters: dict, a mapping of format -> `base_formatter.Formatter`
            subclass instances.
    """
    # pylint: disable=unused-argument
    EXTENSION_NAME = "base-extension"
    argument_prefix = ''

    index = None
    sources = None
    paths_arguments = {}
    path_arguments = {}
    smart_index = False

    def __init__(self, doc_repo):
        """Constructor for `BaseExtension`.

        This should never get called directly.

        Args:
            doc_repo: The `doc_repo.DocRepo` instance which documentation
                is being generated.
        """
        self.doc_repo = doc_repo

        if not hasattr(self, 'formatters'):
            self.formatters = {"html": HtmlFormatter([])}

        self.__created_symbols = defaultdict(OrderedSet)
        self.__overriden_md = {}
        self.__package_root = ''

    # pylint: disable=no-self-use
    def warn(self, code, message):
        """
        Shortcut function for `loggable.warn`

        Args:
            code: see `utils.loggable.warn`
            message: see `utils.loggable.warn`
        """
        warn(code, message)

    # pylint: disable=no-self-use
    def error(self, code, message):
        """
        Shortcut function for `utils.loggable.error`

        Args:
            code: see `utils.loggable.error`
            message: see `utils.loggable.error`
        """
        error(code, message)

    def debug(self, message, domain=None):
        """
        Shortcut function for `utils.loggable.debug`

        Args:
            message: see `utils.loggable.debug`
            domain: see `utils.loggable.debug`
        """
        if domain is None:
            domain = self.EXTENSION_NAME
        debug(message, domain)

    def info(self, message, domain=None):
        """
        Shortcut function for `utils.loggable.info`

        Args:
            message: see `utils.loggable.info`
            domain: see `utils.loggable.info`
        """
        if domain is None:
            domain = self.EXTENSION_NAME
        info(message, domain)

    def get_formatter(self, output_format):
        """
        Get the `base_formatter.Formatter` instance of this extension
        for a given output format.

        Args:
            output_format: str, the output format, for example `html`
        Returns:
            base_formatter.Formatter: the formatter for this format,
                or `None`.
        """
        return self.formatters.get(output_format)

    def setup(self):
        """
        Extension subclasses should implement this to scan whatever
        source files they have to scan, and connect to the various
        signals they have to connect to.

        Note that this will be called *after* the `doc_tree.DocTree`
        of this instance's `BaseExtension.doc_repo` has been fully
        constructed, but before its `doc_tree.DocTree.resolve_symbols`
        method has been called.
        """
        pass

    def get_stale_files(self, all_files):
        """
        Shortcut function to `change_tracker.ChangeTracker.get_stale_files`
        for the tracker of this instance's `BaseExtension.doc_repo`

        Args:
            all_files: see `change_tracker.ChangeTracker.get_stale_files`
        """
        return self.doc_repo.change_tracker.get_stale_files(
            all_files,
            self.EXTENSION_NAME)

    @staticmethod
    def get_dependencies():
        """
        Override this to return the list of extensions this extension
        depends on if needed.

        Returns:
            list: A list of `ExtDependency` instances.
        """
        return []

    @classmethod
    def parse_standard_config(cls, config):
        """
        Subclasses should call this in their
        `utils.configurable.Configurable.parse_config` implementation.

        Args:
            config: core.config.ConfigParser, the configuration holder.
        """
        prefix = cls.argument_prefix
        prefix += '_'
        cls.sources = config.get_sources(prefix)
        cls.index = config.get_index(prefix)
        cls.smart_index = bool(config.get('%s_smart_index' %
                                          cls.argument_prefix))

        for arg, dest in cls.paths_arguments.items():
            val = config.get_paths(arg)
            setattr(cls, dest, val)

        for arg, dest in cls.path_arguments.items():
            val = config.get_path(arg)
            setattr(cls, dest, val)

    @classmethod
    def add_index_argument(cls, group, prefix=None, smart=True):
        """
        Subclasses may call this to add an index argument.

        Args:
            group: arparse.ArgumentGroup, the extension argument group
            prefix: str, arguments have to be namespaced
            smart: bool, whether smart index generation should be exposed
                for this extension
        """
        prefix = prefix or cls.argument_prefix

        group.add_argument(
            '--%s-index' % prefix, action="store",
            dest="%s_index" % prefix,
            help=("Name of the %s root markdown file, can be None" % (
                cls.EXTENSION_NAME)))

        if smart:
            group.add_argument(
                '--%s-smart-index' % prefix, action="store_true",
                dest="%s_smart_index" % prefix,
                help="Smart symbols list generation in %s" % (
                    cls.EXTENSION_NAME))

    @classmethod
    def add_sources_argument(cls, group, allow_filters=True, prefix=None):
        """
        Subclasses may call this to add sources and source_filters arguments.

        Args:
            group: arparse.ArgumentGroup, the extension argument group
            allow_filters: bool,  Whether the extension wishes to expose a
                source_filters argument.
            prefix: str, arguments have to be namespaced.
        """
        prefix = prefix or cls.argument_prefix

        group.add_argument("--%s-sources" % prefix,
                           action="store", nargs="+",
                           dest="%s_sources" % prefix,
                           help="%s source files to parse" % prefix)

        if allow_filters:
            group.add_argument("--%s-source-filters" % prefix,
                               action="store", nargs="+",
                               dest="%s_source_filters" % prefix,
                               help="%s source files to ignore" % prefix)

    @classmethod
    def add_path_argument(cls, group, argname, dest=None, help_=None):
        """
        Subclasses may call this to expose a path argument.

        Args:
            group: arparse.ArgumentGroup, the extension argument group
            argname: str, the name of the argument, will be namespaced.
            dest: str, similar to the `dest` argument of
                `argparse.ArgumentParser.add_argument`, will be namespaced.
            help_: str, similar to the `help` argument of
                `argparse.ArgumentParser.add_argument`.
        """
        prefixed = '%s-%s' % (cls.argument_prefix, argname)
        if dest is None:
            dest = prefixed.replace('-', '_')
            final_dest = dest[len(cls.argument_prefix) + 1:]
        else:
            final_dest = dest
            dest = '%s_%s' % (cls.argument_prefix, dest)

        group.add_argument('--%s' % prefixed, action='store',
                           dest=dest, help=help_)
        cls.path_arguments[dest] = final_dest

    @classmethod
    def add_paths_argument(cls, group, argname, dest=None, help_=None):
        """
        Subclasses may call this to expose a paths argument.

        Args:
            group: arparse.ArgumentGroup, the extension argument group
            argname: str, the name of the argument, will be namespaced.
            dest: str, similar to the `dest` argument of
                `argparse.ArgumentParser.add_argument`, will be namespaced.
            help_: str, similar to the `help` argument of
                `argparse.ArgumentParser.add_argument`.
        """
        prefixed = '%s-%s' % (cls.argument_prefix, argname)
        if dest is None:
            dest = prefixed.replace('-', '_')
            final_dest = dest[len(cls.argument_prefix) + 1:]
        else:
            final_dest = dest
            dest = '%s_%s' % (cls.argument_prefix, dest)

        group.add_argument('--%s' % prefixed, action='store', nargs='+',
                           dest=dest, help=help_)
        cls.paths_arguments[dest] = final_dest

    def get_or_create_symbol(self, *args, **kwargs):
        """
        Extensions that discover and create instances of `symbols.Symbol`
        should do this through this method, as it will keep an index
        of these which can be used when generating a "naive index".

        See `doc_database.DocDatabase.get_or_create_symbol` for more
        information.

        Args:
            args: see `doc_database.DocDatabase.get_or_create_symbol`
            kwargs: see `doc_database.DocDatabase.get_or_create_symbol`

        Returns:
            symbols.Symbol: the created symbol, or `None`.
        """
        sym = self.doc_repo.doc_database.get_or_create_symbol(*args, **kwargs)

        # pylint: disable=unidiomatic-typecheck
        if sym and type(sym) != Symbol:
            self.__created_symbols[sym.filename].add(sym.unique_name)

        return sym

    def __get_rel_source_path(self, source_file):
        stripped = os.path.splitext(source_file)[0]
        return os.path.relpath(stripped, self.__package_root)

    def _get_languages(self):
        return []

    # pylint: disable=no-self-use
    def _get_naive_link_title(self, source_file):
        """
        When a "naive index" is generated by an extension, this class
        generates links between the "base index" and its subpages.

        One subpage is generated per code source file, for example
        if a source file named `my-foo-bar.c` contains documentable
        symbols, a subpage will be created for it, and the label
        of the link in the index will be `my-foo-bar`. Override this
        method to provide a custom label instead.

        Args:
            source_file: The name of the source file to provide a custom
                link label for, for example `/home/user/my-foo-bar.c`

        Returns:
            str: a custom label.
        """
        return os.path.basename(self.__get_rel_source_path(source_file))

    def _get_naive_page_description(self, source_file):
        """
        When a "naive index" is generated by an extension, this class
        will preface every subpage it creates for a given source file
        with a description, the default being simply the name of the
        source file, stripped of its extension.

        Override this method to provide a custom description instead.

        Args:
            source_file: The name of the source file to provide a custom
                description for, for example `/home/user/my-foo-bar.c`

        Returns:
            str: a custom description.
        """
        return '## %s\n\n' % (os.path.basename(
            self.__get_rel_source_path(source_file)))

    def _get_user_index_path(self):
        return None

    def _get_all_sources(self):
        return []

    def __get_naive_index_path(self):
        index_name = 'gen-' + self.EXTENSION_NAME + "-index.markdown"
        dirname = self.doc_repo.get_generated_doc_folder()
        return os.path.join(dirname, index_name)

    # pylint: disable=too-many-locals
    def create_naive_index(self, all_source_files):
        """
        This class can generate an index for the documentable symbols
        in a set of source files. To make use of this feature, subclasses
        should call on this method when the well known name they registered
        is encountered by the `DocRepo.doc_repo.doc_tree` of their instance's
        `BaseExtension.doc_repo`.

        This will generate a set of initially empty markdown files, which
        should be populated by calling `BaseExtension.update_naive_index`
        once symbols have been discovered and created through
        `BaseExtension.get_or_create_symbol`.

        Args:
            all_source_files: list, a list of paths, for example
                `[my_foo_bar.c]`.
            user_index: Path to a potential user index
        Returns: tuple, the arguments expected from a index handler.
        """
        user_index = self._get_user_index_path()
        index_path = self.__get_naive_index_path()
        epage = self.doc_repo.doc_tree.pages.get(index_path)

        common_prefix = os.path.commonprefix(all_source_files)
        self.__package_root = os.path.dirname(common_prefix)

        debug('Package root for %s is %s' % (self.EXTENSION_NAME,
                                             self.__package_root))

        user_index_is_stale = False
        subpages_changed = True
        user_subpages = set()

        if user_index:
            filename = find_md_file(user_index, self.doc_repo.include_paths)
            if filename is None:
                self.warn('smart-index-missing', "Unknown smart index %s" %
                          filename)
                return None

            stale, unlisted = self.doc_repo.change_tracker.get_stale_files(
                [filename], 'gen-index-' + self.EXTENSION_NAME)

            if stale or unlisted:
                user_index_is_stale = True

            user_tree = DocTree(self.doc_repo.include_paths,
                                self.doc_repo.get_private_folder())
            user_tree.build_tree(filename, self.EXTENSION_NAME)
            for subpage in user_tree.pages.values():
                rel_path = os.path.relpath(
                    subpage.source_file,
                    self.doc_repo.get_base_doc_folder())
                user_subpages.add(rel_path)

            with open(filename, 'r') as _:
                preamble = _.read()
        else:
            languages = self._get_languages()
            if languages:
                language = languages[0]
                preamble = '## %s API reference\n' % language.capitalize()
            else:
                preamble = '## %s API reference\n' % (
                    self.EXTENSION_NAME.capitalize())

        gen_paths = OrderedDict()
        full_gen_paths = set()
        for source_file in sorted(all_source_files):
            relpath = self.__get_rel_source_path(source_file)
            if relpath + '.markdown' in user_subpages:
                continue
            gen_path = self.__get_gen_path(source_file)
            gen_paths[relpath] = os.path.relpath(
                gen_path, self.doc_repo.get_generated_doc_folder())
            full_gen_paths.add(gen_path)

        if epage:
            subpages_changed = (full_gen_paths != set(epage.subpages.keys()))

        if user_index_is_stale or subpages_changed:
            with open(index_path, 'w') as _:
                _.write(preamble + '\n')
                for rel_path, markdown_name in gen_paths.items():
                    _.write('#### [%s](%s)\n' % (os.path.basename(rel_path),
                                                 markdown_name))

        return index_path, '', self.EXTENSION_NAME

    def __get_gen_path(self, source_file):
        dirname = self.doc_repo.get_generated_doc_folder()
        rel_path = self.__get_rel_source_path(source_file)
        dirname = os.path.join(dirname, os.path.dirname(rel_path))
        bname = os.path.basename(rel_path)
        gen_path = 'gen-' + bname + '.markdown'
        return os.path.abspath(os.path.join(dirname, gen_path))

    def __make_gen_path(self, source_file):
        gen_path = self.__get_gen_path(source_file)
        dname = os.path.dirname(gen_path)
        if not os.path.exists(dname):
            os.makedirs(dname)
        return gen_path

    def __create_symbols_list(self, source_file, symbols, user_file):
        gen_path = self.__make_gen_path(source_file)

        if user_file:
            with open(user_file, 'r') as _:
                preamble = _.read()
        else:
            preamble = self._get_naive_page_description(source_file)

        info("Generating symbols list for %s" % source_file)

        with open(gen_path, 'w') as _:
            _.write(preamble + '\n')
            for symbol in sorted(symbols):
                containing_pages =\
                    self.doc_repo.doc_tree.get_pages_for_symbol(symbol)
                if containing_pages and gen_path not in containing_pages:
                    debug("symbol %s is already contained elsewhere" % symbol)
                    continue
                # FIXME: more generic escaping
                debug("Adding symbol %s to page %s" % (symbol, gen_path))
                unique_name = symbol.replace('_', r'\_')
                _.write('* [%s]()\n' % unique_name)

    def __resolve_markdown_path(self, filename):
        return self.__overriden_md.get(filename)

    # pylint: disable=too-many-locals
    def update_naive_index(self, smart=False):
        """
        This method can populate the pages generated by
        `BaseExtension.create_naive_index` with the symbols created through
        `BaseExtension.get_or_create_symbol`.

        In smart mode, this method will take existing markdown files into
        account, according to this logic:

        For all source files as returned by `BaseExtension._get_all_sources`
        (which must thus be implemented), we try to find a markdown file
        in the markdown include paths named similarly, if one is found
        its contents are prepended to the generated page.

        Args:
            smart: bool, take existing markdown files into account.
        """
        index_path = self.__get_naive_index_path()
        subtree = DocTree(self.doc_repo.include_paths,
                          self.doc_repo.get_private_folder())

        user_files = {}
        self.__overriden_md = {}
        gen_paths = []
        source_map = {}

        if smart:
            all_sources = self._get_all_sources()
            for source in all_sources:
                relpath = self.__get_rel_source_path(source)
                user_file = find_md_file(relpath + '.markdown',
                                         self.doc_repo.include_paths)
                if user_file:
                    user_files[source] = user_file
                    source_map[user_file] = source
                    self.__overriden_md[relpath + '.markdown'] = \
                        self.__get_gen_path(source)

        stale, unlisted = self.doc_repo.change_tracker.get_stale_files(
            user_files.values(), 'gen-' + self.EXTENSION_NAME)
        stale |= unlisted

        for source_file, symbols in self.__created_symbols.items():
            user_file = user_files.pop(source_file, None)
            gen_paths.append(self.__get_gen_path(source_file))
            self.__create_symbols_list(source_file, symbols, user_file)

            if user_file:
                try:
                    stale.remove(user_file)
                except IndexError:
                    pass

        for user_file in stale:
            source_file = source_map[user_file]
            gen_path = self.__get_gen_path(source_file)
            gen_paths.append(gen_path)
            epage = self.doc_repo.doc_tree.pages[gen_path]
            self.__create_symbols_list(source_file, epage.symbol_names,
                                       user_file)

        resolve_markdown_signal.connect(self.__resolve_markdown_path)

        index_root = subtree.build_tree(
            index_path,
            extension_name=self.EXTENSION_NAME,
            parent_tree=self.doc_repo.doc_tree)

        resolve_markdown_signal.disconnect(self.__resolve_markdown_path)

        for gen_path in gen_paths:
            page = subtree.pages.get(gen_path)
            if page:
                if not page.symbol_names:
                    index_root.remove_subpage(page.source_file)

        self.doc_repo.doc_tree.pages.update(subtree.pages)

    def format_page(self, page, link_resolver, output):
        """
        Called by `doc_repo.DocRepo.format_page`, to leave full control
        to extensions over the formatting of the pages they are
        responsible of.

        Args:
            page: doc_tree.Page, the page to format.
            link_resolver: links.LinkResolver, object responsible
                for resolving links potentially mentioned in `page`
            output: str, path to the output directory.
        """
        formatter = self.get_formatter('html')
        if page.is_stale:
            page.languages = self._get_languages()
            debug('Formatting page %s' % page.link.ref, 'formatting')
            page.formatted_contents = \
                self.doc_repo.doc_tree.page_parser.format_page(
                    page, link_resolver, formatter)
            actual_output = os.path.join(output, formatter.get_output_folder())
            if not os.path.exists(actual_output):
                os.makedirs(actual_output)
            page.format(formatter, link_resolver, actual_output)
        else:
            debug('Not formatting page %s, up to date' % page.link.ref,
                  'formatting')
