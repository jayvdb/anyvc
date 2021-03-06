# -*- coding: utf-8 -*-
import sys
import os

cur = os.path.abspath(__file__)
base = os.path.dirname(os.path.dirname(cur))
sys.path.insert(0, base)


# General configuration
# ---------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.viewcode',
    'sphinx.ext.graphviz',
    'sphinx.ext.inheritance_diagram',
]

templates_path = ['.templates']
source_suffix = '.rst'
master_doc = 'index'

# General substitutions.
project = u'anyvc'
copyright = u'2008, Pida Team'

# The default replacements for |version| and |release|, also used in various
# other places throughout the built documents.
#
# The full version, including alpha/beta/rc tags.

import hgdistver
version = hgdistver.get_version(root=base)
# The short X.Y version.
if version:
    release = '.'.join(version.split('.')[:3])
else:
    release = 'unknown'
# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
#today = ''
# Else, today_fmt is used as the format for a strftime call.
today_fmt = '%B %d, %Y'

# List of documents that shouldn't be included in the build.
exclude_patterns = [
    'workdir/cli.rst',  # XXX:
    'readme.rst',  # XXX:
]

# List of directories, relative to source directories,
# that shouldn't be searched for source files.
exclude_trees = [
    'draco',
]

# dont show the module names for class specs
add_module_names = False

# Options for HTML output
# -----------------------

# The style sheet to use for HTML and HTML Help pages. A file of that name
# must exist either in Sphinx' static/ path, or in one of the custom paths
# given in html_static_path.
# html_style = 'default.css'

#XXX: get the draco theme back
#html_theme_path = ['.']
#html_theme = 'draco'

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
#html_title = None

# A shorter title for the navigation bar.  Default is the same as html_title.
html_short_title = release

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
html_logo = '_static/tarsius.png'

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
#html_favicon = None

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
html_last_updated_fmt = '%b %d, %Y'

html_theme_options = {
    'tagline': 'all version control systems through a single API',
    'bitbucket_project': 'RonnyPfannschmidt/anyvc',
    'nosidebar': True,
}

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
#html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
#html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
#html_additional_pages = {}

# If false, no module index is generated.
#html_use_modindex = True

# If false, no index is generated.
#html_use_index = True

# If true, the index is split into individual pages for each letter.
#html_split_index = False

# If true, the reST sources are included in the HTML build as _sources/<name>.
#html_copy_source = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
#html_use_opensearch = ''

# If nonempty, this is the file name suffix for HTML files (e.g. ".xhtml").
#html_file_suffix = ''

# Output file base name for HTML help builder.
htmlhelp_basename = 'anyvcdoc'


# Options for LaTeX output
# ------------------------

# The paper size ('letter' or 'a4').
#latex_paper_size = 'letter'

# The font size ('10pt', '11pt' or '12pt').
#latex_font_size = '10pt'

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target, title, author, document class [howto/manual])
latex_documents = [
    ('index', 'anyvc.tex', u'anyvc Documentation',
     u'Pida Team', 'manual'),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
#latex_logo = None

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
#latex_use_parts = False

# Additional stuff for the LaTeX preamble.
#latex_preamble = ''

# Documents to append as an appendix to all manuals.
#latex_appendices = []

# If false, no module index is generated.
#latex_use_modindex = True
