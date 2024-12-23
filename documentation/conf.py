# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

author = u'Sofía Ortega Sosa'
copyright = u'2021-2023 Sofía Ortega Sosa'
extensions = ['breathe']
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
autosectionlabel_prefix_document = True
breathe_domain_by_extension = {'h': 'c'}
#html_theme = 'haiku'
html_static_path = ['_static']
latex_elements = {'releasename': 'Version'}
