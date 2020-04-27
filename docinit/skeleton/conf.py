# Configuration file for the Sphinx documentation builder.

# -- Path setup --------------------------------------------------------------

from timeflux import __version__
from datetime import datetime

# -- Project information -----------------------------------------------------

project = 'Timeflux'
copyright = '2018–{}, Pierre Clisson and the Timeflux community'.format(datetime.now().year)
author = 'Pierre Clisson'
version = __version__
release = __version__
language = None

# -- Setup-----------------------------------------------------------------

rst_prolog = """
.. |br| raw:: html

   <br>
"""

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.intersphinx',
    'autoapi.extension',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.todo',
    'sphinx.ext.mathjax'
]

templates_path = ['_templates']
master_doc = 'index'
language = None
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

autodoc_default_options = {
    'special-members': '__init__',
    'member-order': 'bysource'
}

autoapi_dirs = ['../timeflux']
autoapi_type = 'python'
autoapi_root = 'api'
autoapi_add_toctree_entry = False
autoapi_ignore = ['*migrations*', '*__main__.py', '*timeflux.py', '*classifiers*']
autoapi_template_dir = '_templates'

napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_use_ivar = True
pygments_style = 'sphinx'
todo_include_todos = True

# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'collapse_navigation': False,
    'display_version': True,
}
html_logo = 'static/img/logo.png'

html_static_path = ['_static']

globals()['foo'] = 'bar'
print(foo)
