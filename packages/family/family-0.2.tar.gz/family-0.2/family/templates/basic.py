


import os
from paste.script.templates import Template, var
from paste.util.template import paste_script_template_renderer


class FalconTemplate(Template):

    _template_dir = 'falcon'
    summary = "A basic daixm microserivce falcon package"
    vars = [
        var('version', 'Version (like 0.1)'),
        var('description', 'One-line description of the package'),
        var('long_description', 'Multi-line description (in reST)'),
        var('keywords', 'Space-separated keywords/tags'),
        var('author', 'Author name'),
        var('author_email', 'Author email'),
        var('url', 'URL of homepage'),
        ]

    template_renderer = staticmethod(paste_script_template_renderer)

    def post(self, command, output_dir, vars):
        os.rename('%s/gitignore' % output_dir, '%s/.gitignore' % output_dir)
