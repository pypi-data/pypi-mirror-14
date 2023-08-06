# -*- coding: utf-8 -*-

import os
import webbrowser
from os.path import join

from dkfileutils.changed import changed
from invoke import ctask as task, Collection
from dktasklib import Package


@task(name='clean')
def _clean(ctx):  # Underscored func name to avoid shadowing kwargs in build()
    """Nuke docs build target directory so next build is clean.
    """
    if 'pkg' not in ctx:
        ctx.pkg = Package()
    builddir = ctx.pkg.root / 'build' / 'docs'
    if os.path.exists(builddir) and len(os.listdir(builddir)) > 0:
        ctx.run("rm -rf {0}/*".format(builddir))


# Ditto
@task(name='browse')
def _browse(ctx):  # pragma: nocover
    """Open build target's index.html in a browser (using the :py:mod:`webbrowser` module).
    """
    index = join(ctx.pkg.root / 'build' / 'docs' / 'index.html')
    webbrowser.open_new(index)


@task(default=True, help={
    'opts': "Extra sphinx-build options/args",
    'clean': "Remove build tree before building",
    'browse': "Open docs index in browser after building",
    'warn': "Build with stricter warnings/errors enabled",
    'builder': "Builder to use, defaults to html",
    'force': "Force re-reading of all files (ignore cache)",
})
def build(ctx, clean=False, browse=False, warn=False,
          builder='html',
          force=True,
          opts=""):
    """
    Build the project's Sphinx docs.
    """
    if not force and not changed(ctx.pkg.docsdir):
        print """
        No changes detected in {}, add --force to build docs anyway.
        """.format(ctx.pkg.docsdir)
        return  # should perhaps check if code has changed too? (autodoc)

    if clean:
        _clean(ctx)
    if opts is None:  # pragma: nocover
        opts = ""
    opts += " -b %s" % builder
    if warn:
        opts += " -n -W"
    if force:
        opts += " -a -E"
    cmd = "sphinx-build {opts} {ctx.pkg.docsdir} {ctx.pkg.root}/build/docs".format(opts=opts, ctx=ctx)
    dj_settings = ctx.pkg.get('django_settings_module', "")
    if dj_settings:
        os.environ['DJANGO_SETTINGS_MODULE'] = dj_settings
    ctx.run(cmd)
    if browse:  # pragma: nocover
        _browse(ctx)


@task
def tree(ctx):
    """Display the docs tree.
    """
    ignore = ".git|*.pyc|*.swp|dist|*.egg-info|_static|_build|_templates"
    ctx.run('tree -Ca -I "{0}" {1}'.format(ignore, ctx.pkg.docsdir))


# Vanilla/default/parameterized collection for normal use
ns = Collection('docs', _clean, _browse, build, tree)
ns.configure({
    'docs': {
        'source': 'docs',
        'builddir': join('build', 'docs'),
        'target_file': 'index.html',
    }
})
