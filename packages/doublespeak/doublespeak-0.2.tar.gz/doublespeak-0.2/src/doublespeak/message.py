"""Inspired by
http://trac.edgewall.org/attachment/ticket/6353/babel-l10n-js.diff#L590 """

import os
import glob
import distutils
import json
from babel._compat import StringIO
from babel._compat import string_types
from babel.messages import frontend as babel
from babel.messages.pofile import read_po
import gettext

TEMPLATE = '''\
/*jshint indent: 4 */
if (typeof window.json_locale_data === 'undefined') {{
    window.json_locale_data = new Object();
}}
window.json_locale_data['{domain}'] = {messages};
'''


def check_js_message_extractors(dist, name, value):
    """Validate the ``js_message_extractors`` keyword argument to ``setup()``.

    :param dist: the distutils/setuptools ``Distribution`` object
    :param name: the name of the keyword argument (should always be
                 "js_message_extractors")
    :param value: the value of the keyword argument
    :raise `DistutilsSetupError`: if the value is not valid
    """
    assert name == 'js_message_extractors'
    if not isinstance(value, dict):
        raise distutils.errors.DistutilsSetupError(
            'the value of the "js_message_extractors" parameter must be a '
            'dictionary')


class extract_js_messages(babel.extract_messages):
    """Mostly a wrapper for Babel's extract_messages so that we can configure
       it explicitly for JS files in setup.cfg
    """

    def _get_mappings(self):
        """Override to check js_message_extractors keywords and not
           message_extractors
        """
        mappings = {}
        if self.mapping_file:
            mappings = babel.extract_messages._get_mappings(self)
        elif getattr(self.distribution, 'js_message_extractors', None):
            message_extractors = self.distribution.js_message_extractors
            for dirname, mapping in message_extractors.items():
                if isinstance(mapping, string_types):
                    method_map, options_map = \
                        babel.parse_mapping(StringIO(mapping))
                else:
                    method_map, options_map = [], {}
                    for pattern, method, options in mapping:
                        method_map.append((pattern, method))
                        options_map[pattern] = options or {}
                mappings[dirname] = method_map, options_map
        else:
            mappings = babel.extract_messages._get_mappings(self)
        return mappings


class init_js_catalog(babel.init_catalog):
    """Wrapper for Babel's init_catalog so that we can configure it
       explicitly for JS files in setup.cfg
    """


class update_js_catalog(babel.update_catalog):
    """Wrapper for Babel's update_catalog so that we can configure it
       explicitly for JS files in setup.cfg
    """


class compile_js_catalog(distutils.cmd.Command):
    """Generating message javascripts command for use ``setup.py`` scripts.
    """

    description = 'generate message javascript file from PO files'
    user_options = [
        ('domain=', 'D',
         "domain of PO file (default 'messages')"),
        ('input-dir=', 'I',
         'path to base directory containing the catalogs'),
        ('output-dir=', 'o',
         'path to the output directory'),
        ('output-prefix=', 'p',
         'filename prefix for files in output directory'),
        ('fallback-locale=', 'l',
         "fallback locale (default 'en')"),
        ('use-fuzzy', 'f',
         'also include fuzzy translations'),
        ('statistics', None,
         'print statistics about translations')
    ]
    boolean_options = ['use-fuzzy', 'statistics']

    def initialize_options(self):
        self.domain = 'messages'
        self.input_dir = None
        self.output_dir = None
        self.output_prefix = ''
        self.fallback_locale = 'en'
        self.use_fuzzy = False
        self.statistics = False

    def finalize_options(self):
        pass

    def run(self):
        found_po_files = False

        for in_dir in glob.glob(os.path.join(self.input_dir, '*')):
            locale = in_dir.rstrip('/').split('/')[-1]
            if not os.path.isdir(in_dir):
                distutils.log.warn(
                    "can't generate JS for locale {} because the "
                    "directory {} doesn't exist".format(locale, in_dir))
                continue
            po_file = os.path.join(in_dir, 'LC_MESSAGES', self.domain + '.po')
            if not os.path.exists(po_file):
                distutils.log.warn(
                    "can't generate JS for locale \"{}\" because the file {}"
                    "doesn't exist".format(locale, po_file))
                continue

            found_po_files = True

            infile = open(po_file, 'rb')
            try:
                catalog = read_po(infile, locale)
            finally:
                infile.close()

            # statistics.
            if self.statistics:
                translated = 0
                for message in list(catalog):
                    if message.id == '':
                        continue
                    if message.string:
                        translated +=1
                percentage = 0
                if len(catalog):
                    percentage = translated * 100 // len(catalog)
                distutils.log.info('%d of %d messages (%d%%) translated in %r',
                         translated, len(catalog), percentage, po_file)

            if catalog.fuzzy and not self.use_fuzzy:
                distutils.log.warn('warning: catalog %r is marked as fuzzy, skipping', po_file)
                continue

            for message, errors in catalog.check():
                for error in errors:
                    distutils.log.error(
                        'error: %s:%d: %s', po_file, message.lineno, error)

            # Don't leak private information to the frontend.
            messages = {'': [None, '']}

            for message in list(catalog):
                # See comment above about not leaking private information to the
                # frontend.
                if message.id == '':
                    continue
                if not self.use_fuzzy and message.fuzzy:
                    continue
                # If you need pluralization here, make a pull request.
                messages[message.id] = [None, message.string]

            js_file_path = os.path.join(
                self.output_dir,
                '{}{}.js'.format(self.output_prefix, locale))
            open(js_file_path, 'w').write(TEMPLATE.format(
                messages=json.dumps(messages),
                domain=self.domain
            ))
            distutils.log.info(
                'compiling Javascript catalog {} to {}.'.format(
                    po_file, js_file_path))

        if not found_po_files:
            raise distutils.errors.DistutilsOptionError(
                'no compiled catalogs found')
