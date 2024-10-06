# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

sys.path.insert(0, os.path.abspath('../../src/'))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'WSE'
copyright = '2024, Sergei Mikurov'
author = 'Sergei Mikurov'
release = '0.0.1'

# -- GitHub information ------------------------------------------------
github_user = 'svmikurov'
github_repo_name = 'wse-gui'
github_version = 'main'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    # Include documentation from docstrings
    # https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#module-sphinx.ext.autodoc
    'sphinx.ext.autodoc',
    # Add copy button from block
    # https://sphinx-copybutton.readthedocs.io/en/latest/#sphinx-copybutton
    'sphinx_copybutton',
    # Allow reference sections using its title
    # https://www.sphinx-doc.org/en/master/usage/extensions/autosectionlabel.html#module-sphinx.ext.autosectionlabel
    'sphinx.ext.autosectionlabel',
]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']
# https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-add_module_names
add_module_names = False