# flake8: noqa
# pylint: skip-file
# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys

sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath("../../"))

project = "Python Freckle Client"
copyright = "2023, OmbuLabs - The Lean Software Boutique, LLC"
author = "OmbuLabs - The Lean Software Boutique, LLC"
release = "v1.0.0"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "myst_parser",
    "sphinx_rtd_theme",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
]

templates_path = ["_templates"]
exclude_patterns = ["venv/*"]

source_paths = ["source"]
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}
autodoc_mock_imports = [
    "requests",
    "pydantic",
    "python-dateutil",
    "dateutil",
    "pydantic_core",
]
# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_theme_options = {
    "style_external_links": True,
    "style_nav_header_background": "#282828",
}
