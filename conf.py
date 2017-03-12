# -*- coding: utf-8 -*-

import tinkerer
import tinkerer.paths
import sys, os

# **************************************************************
# TODO: Edit the lines below
# **************************************************************

# Change this to the name of your blog
project = 'beberlei.de'

description = 'Blog of Benjamin Eberlei, covering a wide range of programming, bootstrapping and entrepreneurial topics'

# Change this to the tagline of your blog
tagline = ''

# Change this to your name
author = 'Benjamin Eberlei'

# Change this to your copyright string
copyright = '2008-2017, ' + author

# Change this to your blog root URL (required for RSS feed)
website = 'https://www.beberlei.de'

# **************************************************************
# More tweaks you can do
# **************************************************************

# Add your Disqus shortname to enable comments powered by Disqus
disqus_shortname = 'whitewashing'

# Change your favicon (new favicon goes in _static directory)
html_favicon = 'tinkerer.ico'

# Pick another Tinkerer theme or use your own
html_theme = "bootstrap"

# Theme-specific options, see docs
html_theme_options = { }

# Link to RSS service like FeedBurner if any, otherwise feed is
# linked directly
rss_service = None

# **************************************************************
# Edit lines below to further customize Sphinx build
# **************************************************************

# Add other Sphinx extensions here
sys.path.append(os.path.abspath('_ext'))
extensions = ['tinkerer.ext.blog', 'tinkerer.ext.disqus', 'phprss']

# Add other template paths here
templates_path = ['_templates']

# Add other static paths here
html_static_path = ['_static', tinkerer.paths.static]

# Add other theme paths here
html_theme_path = ['_theme', tinkerer.paths.themes]

# Add file patterns to exclude from build
exclude_patterns = ["drafts/*"]

# Add templates to be rendered in sidebar here
html_sidebars = {
    "**": ["recent.html"]
}

rss_for_categories = True
rss_categories_to_build = ["PHP", "php"]

posts_per_page=5


# **************************************************************
# Do not modify below lines as the values are required by
# Tinkerer to play nice with Sphinx
# **************************************************************

source_suffix = tinkerer.source_suffix
master_doc = tinkerer.master_doc
version = tinkerer.__version__
release = tinkerer.__version__
html_title = project
html_use_index = False
html_show_sourcelink = False
html_add_permalinks = None

