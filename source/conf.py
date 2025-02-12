# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'High-Assurance Cyber-Physical Systems'
copyright = '2024, Daniel G. Cole'
author = 'Daniel G. Cole'
version = '1.0'
release = '1.0-beta'


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [   'sphinxcontrib.ansi']

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# import better
# html_theme = 'better'
# html_theme_path = [better.better_theme_path]

# html_theme = 'sphinx_rtd_theme'
# html_theme = 'bizstyle'
html_theme = 'piccolo_theme'

html_static_path = ['_static']
html_baseurl = ''
html_title = 'HACPS'
html_sidebars = {'**':['globaltoc.html']}
# html_logo = './_static/logo.png'

# rst_prolog = """
# .. |imgpath| replace:: ../_static/images
# """
