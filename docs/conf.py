# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Collaboration Documentation'
copyright = '2025, MIT License'
author = 'Kabir, Geordie, Lea, Chunhua, Simon'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# Enable better typography and layout
extensions = [
    "myst_parser",  # Markdown support
    "sphinx_rtd_theme"
]


templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# Use the ReadTheDocs theme
html_theme = "sphinx_rtd_theme"

# Additional configurations for visuals
html_theme_options = {
    "navigation_depth": 3,  # Show deeper navigation levels
    "collapse_navigation": False,  # Expand sidebar sections
}
html_static_path = ['_static']
