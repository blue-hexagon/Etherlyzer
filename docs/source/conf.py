import os
import sys
from importlib.metadata import version

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Etherlyzer"
copyright = "2026, blue-hexagon"
author = "blue-hexagon"
release = version("etherlyzer")
version = release

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}
extensions = [
    "myst_parser",
    "sphinxext.opengraph",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx.ext.autosummary",
    "sphinx_copybutton",
    "sphinx.ext.todo",
    "sphinx_design",
    "sphinxcontrib.mermaid",
    "sphinx_autodoc_typehints",
    "sphinx_sitemap",
]


# MERMAID
# mermaid_version = "11.9.0"
html_baseurl = "https://etherlyzer.docs.manjana.dev/"
mermaid_light_theme = "default"
mermaid_dark_theme = "dark"

ogp_site_url = html_baseurl
ogp_site_name = "EtherLyzer"
ogp_description_length = 200
ogp_enable_meta_description = True

sitemap_show_lastmod = True
sitemap_indent = 2

todo_include_todos = False
nitpicky = True
html_css_files = [
    "custom.css",
]
html_permalinks_icon = "#"

myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "fieldlist",
    "tasklist",
    "attrs_inline",
    "substitution",
    "smartquotes",
    "strikethrough",
]
myst_substitutions = {
    "project": project,
    "version": version,
    "release": release,
    "version_badge": f"{{bdg-light}}`v{version}`",
}
# pygments_style = "friendly"
# pygments_dark_style = "dracula"
pygments_style = "sphinx"
pygments_dark_style = "monokai"
highlight_options = {
    "python": {
        "stripnl": False,
    }
}
html_favicon = "_static/favicon.ico"
html_last_updated_fmt = "%Y-%m-%d %H:%M:%S"
copybutton_prompt_text = r">>> |\.\.\. |\$ |PS [^>]*> "
copybutton_prompt_is_regexp = True
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}
# html_title = f"{project} Docs"

html_theme_options = {
    # GitHub integration
    "source_repository": "https://github.com/blue-hexagon/EtherLyzer/",
    "source_branch": "main",
    "source_directory": "docs/source/",
    # Navigation
    "navigation_with_keys": True,
    "sidebar_hide_name": True,
    "top_of_page_buttons": ["view", "edit"],
    # Branding
    "light_logo": "logo_light.png",
    "dark_logo": "logo_dark.png",
    # Light mode
    "light_css_variables": {
        "color-brand-primary": "#008FA3",
        "color-brand-content": "#007F99",
    },
    # Dark mode
    "dark_css_variables": {
        "color-brand-primary": "#00D5E8",
        "color-brand-content": "#25DCEB",
    },
    # Optional announcement banner
    # "announcement": "EtherLyzer documentation — v0.10.0",
}
html_title = project
autosummary_generate = True

autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "show-inheritance": True,
}
autodoc_typehints = "none"
always_document_param_types = True
typehints_use_rtype = False
napoleon_use_rtype = False

python_maximum_signature_line_length = 88
python_trailing_comma_in_multi_line_signatures = True
python_use_unqualified_type_names = True
viewcode_follow_imported_members = True
myst_heading_anchors = 5

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
html_theme = "furo"
templates_path = ["_templates"]
html_static_path = ["_static"]
exclude_patterns = []

sys.path.insert(0, os.path.abspath("../../src"))
html_show_sphinx = True
html_search_language = "en"
toc_object_entries = True
toc_object_entries_show_parents = "hide"
add_module_names = False
python_display_short_literal_types = True

smartquotes = True

viewcode_line_numbers = True
numfig = True
numfig_secnum_depth = 2
numfig_format = {
    "figure": "Figure %s",
    "table": "Table %s",
    "code-block": "Listing %s",
}
