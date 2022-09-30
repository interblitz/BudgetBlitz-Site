# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

####################################################################################
# Примечания
# В mxtheme для тега IMG установлен display: block, т.е. одна картинка на строку
# display удалил, исправленный sphinx_materialdesign_theme.css положил в _static
# Возможно стоит сделать отдельный стиль для IMG для tumbnail
####################################################################################

import sys
from os.path import basename
from io import StringIO

from docutils.parsers.rst import Directive
from docutils.parsers.rst.directives.misc import Raw
from docutils.parsers.rst.directives.misc import Replace
from docutils.parsers.rst.directives.tables import ListTable
from docutils import nodes

# sphinx-design extensions
from sphinx_design.badges_buttons import ButtonLinkDirective


class ExecDirective(Directive):
    """Execute the specified python code and insert the output into the document"""
    has_content = True

    def run(self):
        oldStdout, sys.stdout = sys.stdout, StringIO()
        try:
            exec('\n'.join(self.content))
            return [nodes.Text(sys.stdout.getvalue(), sys.stdout.getvalue())]
        except Exception as e:
            return [nodes.error(None, nodes.paragraph(text = "Unable to execute python code at %s:%d:" % (basename(self.src), self.srcline)), nodes.paragraph(text = str(e)))]
        finally:
            sys.stdout = oldStdout

class PutVarDirective(Directive):
    """Save var for subs"""
    required_arguments = 2
    optional_arguments = 0
    final_argument_whitespace = True

    def run(self):
        app = self.state.document.settings.env.app
        #app.config.vars = app.config.vars + [(self.arguments[0], self.arguments[1])]
        app.config.vars[self.arguments[0]] = self.arguments[1]

        return []

class VarsRawDirective(Raw):
    """Raw with vars"""

    def run(self):
        app = self.state.document.settings.env.app
        new_content = []
        existing_content = self.content
        for item in existing_content:
            #for pair in app.config.vars:
            for original, replacement in app.config.vars.items():
                #original, replacement = pair
                item = item.replace(original, replacement)
            new_content.append(item)

        self.content = new_content
        return list(Raw.run(self))

class VarsListTableDirective(ListTable):
    """ListTable with vars"""

    def run(self):
        app = self.state.document.settings.env.app
        existing_content = self.content
        for i in range(0, len(existing_content)):
            item = existing_content[i]
            for original, replacement in app.config.vars.items():
                #original, replacement = pair
                item = item.replace(original, replacement)
            self.content[i] = item
        return list(ListTable.run(self))

class VarsReplaceDirective(Replace):
    """Replace with vars"""
    has_content = True

    def run(self):
        app = self.state.document.settings.env.app
        existing_content = self.content
        for i in range(0, len(existing_content)):
            item = existing_content[i]
            for original, replacement in app.config.vars.items():
                #original, replacement = pair
                item = item.replace(original, replacement)
            self.content[i] = item

        return Replace.run(self)

##############################################################################################3
# sphinx-design extensions

class VarsButtonLinkDirective(ButtonLinkDirective):
    """ButtonLink with vars"""

    def run(self):
        app = self.state.document.settings.env.app
        existing_content = self.content

        for i in range(0, len(existing_content)):
            item = existing_content[i]
            for original, replacement in app.config.vars.items():
                #original, replacement = pair
                item = item.replace(original, replacement)
            self.content[i] = item

        arguments_0 = self.arguments[0]
        for original, replacement in app.config.vars.items():
            # original, replacement = pair
            arguments_0 = arguments_0.replace(original, replacement)
        self.arguments[0] = arguments_0

        return list(ButtonLinkDirective.run(self))


##############################################################################################3

project = 'Блиц бюджет для Android'
copyright = '2022, Basin Michael'
author = 'Basin Michael'
release = '2.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.todo',
    'sphinx.ext.ifconfig',
    'sphinxcontrib.images',
    'sphinx_design',
    'sphinx-favicon'
    ]

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'mxtheme'
html_theme_options = {
	 # Specify a list of menu in Header.
    # Tuples forms:
    #  ('Name', 'external url or path of pages in the document', boolean, 'icon name')
    #
    # Third argument:
    # True indicates an external link.
    # False indicates path of pages in the document.
    #
    # Fourth argument:
    # Specify the icon name.
    # For details see link.
    # https://material.io/icons/
'header_links' : [
        (u'Главная', 'index', False, ''),
        (u'Изменения', 'changes', False, ''),
        (u'Поддержите нас', 'support-us', False, ''),
        (u'Руководство пользователя', 'https://interblitz.github.io/BudgetBlitz-Manual/ru/build/html/index.html', True, ''),
        (u'Помощь', 'http://qa.bbmoney.biz/ru', True, ''),
        (u'Конфиденциальность', 'privacy', False, '')
    ],
    # Customize css colors.
    # For details see link.
    # https://getmdl.io/customize/index.html
    #
    # Values: amber, blue, brown, cyan deep_orange, deep_purple, green, grey, indigo, light_blue,
    #         light_green, lime, orange, pink, purple, red, teal, yellow(Default: indigo)
'primary_color': 'indigo',
    # Values: Same as primary_color. (Default: pink)
'accent_color': 'blue',
    # Customize layout.
    # For details see link.
    # https://getmdl.io/components/index.html#layout-section
'fixed_drawer': False,
'fixed_header': True,
'header_waterfall': True,
'header_scroll': False,

    # Render title in header.
    # Values: True, False (Default: False)
'show_header_title': False,
    # Render title in drawer.
    # Values: True, False (Default: True)
'show_drawer_title': True,
    # Render footer.
    # Values: True, False (Default: True)
'show_footer': True
}

html_show_sourcelink = False
html_static_path = ['_static']

favicons = [
    {
        "rel": "icon",
        "static-file": "favicon.ico",
        "sizes": "any",
        "type": "image/ico",
    },
    {
        "rel": "apple-touch-icon",
        "sizes": "180x180",
        "static-file": "apple-touch-icon.png",
        "type": "image/png",
    }
]

def setup(app):
    app.add_css_file('customstyle.css')
    app.add_config_value('vars', {}, 'html')
    app.add_directive('exec', ExecDirective)
    app.add_directive('vars_raw', VarsRawDirective)
    app.add_directive('vars_replace', VarsReplaceDirective)
    app.add_directive('vars_list-table', VarsListTableDirective)
    app.add_directive('put_var', PutVarDirective)

    app.add_directive('vars_button-link', VarsButtonLinkDirective)

    #import mxtheme
    #app.add_directive('card', mxtheme.CardDirective)
