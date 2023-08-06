# -*- coding: utf-8 -*-
import os
import textwrap

from invoke import ctask as task, Collection

from dktasklib import runners
from dktasklib.commands import Command
from dktasklib.executables import requires
from dktasklib.utils import cd, dest_is_newer_than_source
from dktasklib.version import version_name, add_version


def ensure_package_json(ctx):
    """Is this a node package?
    """
    package_json = os.path.join(ctx.pkg.root, 'package.json')
    if not os.path.exists(package_json):
        print "Missing package.json file, creating default version.."
        with cd(ctx.pkg.root):
            ctx.run("npm init -f")
    else:
        return True


def ensure_babelrc(ctx):
    """babel needs a .babelrc file to do any work.
    """
    babelrc = os.path.join(ctx.pkg.root, '.babelrc')
    if not os.path.exists(babelrc):
        print 'Misssing %s (creating default version)' % babelrc
        with open(babelrc, 'w') as fp:
            fp.write(textwrap.dedent("""
            {
                "presets": ["es2015"]
            }
            """))
    else:
        return True


def ensure_node_modules(ctx):
    """Has node init been called? (if not call it).
    """
    node_modules = os.path.join(ctx.pkg.root, 'node_modules')
    if not os.path.exists(node_modules):
        with cd(ctx.pkg.root):
            ctx.run("npm install --no-color")
    else:
        return True


# def ensure_babel(ctx):
#     if 'babel' not in runners.run("npm ls -g --depth=0 babel --no-color"):
#         print "didn't find babel, installing it.."
#         with cd(ctx.pkg.root):
#             ctx.run("npm install -g babel")
#     else:
#         return True


# def ensure_browserify(ctx):
#     if 'browserify' not in runners.run("npm ls -g --depth=0 browserify --no-color"):
#         print "didn't find browserify, installing it.."
#         with cd(ctx.pkg.root):
#             ctx.run("npm install -g browserify")
#     else:
#         return True


def ensure_es2015(ctx):
    if 'babel-preset-es2015' not in runners.run("npm ls --depth=0 babel-preset-es2015 --no-color"):
        print "didn't find babel-preset-es2015, installing it.."
        with cd(ctx.pkg.root):
            ctx.run("npm install babel-preset-es2015 --save-dev")
    else:
        return True


def ensure_babelify(ctx):
    if 'babelify' not in runners.run("npm ls --depth=0 babelify --no-color"):
        print "didn't find babelify, installing it.."
        with cd(ctx.pkg.root):
            ctx.run("npm install --save-dev babelify --no-color", echo=False, encoding='utf-8')
    else:
        return True


@requires('nodejs', 'npm', 'babel')
@task
def babel(ctx, source, dest, source_maps=True, force=False):
    """
    --source-maps --out-file $ProjectFileDir$/$ProjectName$/static/$ProjectName$/$FileNameWithoutExtension$.js $FilePath$
    """
    if not force and dest_is_newer_than_source(source, dest):
        print 'babel:', dest, 'is up-to-date.'
        return dest

    ensure_package_json(ctx)
    ensure_node_modules(ctx)
    # ensure_babel(ctx)
    ensure_es2015(ctx)
    ensure_babelrc(ctx)

    options = ""
    if source_maps:
        options += " --source-maps"

    ctx.run("babel {options} --out-file {dest} {source}".format(**locals()))
    return dest


def version_js(ctx, fname, kind='pkg', force=False):
    """Add version number to a .js file.
    """
    dst = add_version(
        ctx,
        fname, version_name(fname),
        kind=kind,
        force=force
    )
    if force or not os.path.exists(dst):
        ctx.run('cp {src} {dst}'.format(
            src=fname,
            dst=dst
        ))
    else:
        print """
        Filename already exists, add --force or call upversion: {}
        """.format(dst)
    return dst


@requires('nodejs', 'npm', 'browserify')
@task
def browserify(ctx,
               source, dest,
               babelify=False,
               require=(),
               external=(),
               entry=None):
    """
    Run ``browserify``

    Args:
        ctx (pyinvoke.Context):  context
        source (str):            root source file
        dest (str):              path/name of assembled file
        babelify (Bool):         use babel transform
        require (iterable):      A module name or file to bundle.require()
                                 Optionally use a colon separator to set the target.
        external:                Reference a file from another bundle. Files can be globs.
        entry:

    Returns:
        None

    """
    print 'ensure package.json:', ensure_package_json(ctx)
    print 'ensure node_modules:', ensure_node_modules(ctx)
    # print 'ensure browserify:', ensure_browserify(ctx)

    # options = "--debug"  # source maps
    options = ""  # no source maps
    if babelify:
        print 'ensure babelify:', ensure_babelify(ctx)
        options += ' -t babelify'
    for r in require:
        options += ' -r "%s"' % r
    for e in external:
        options += ' -x "%s"' % e
    if entry:
        options += ' -e "%s"' % entry
    cmd = "browserify {source} -o {dest} {options}".format(**locals())
    ctx.run(cmd)
    with open(dest, 'rb') as fp:
        txt = fp.read()
    if '\r\n' in txt:
        with open(dest, 'wb') as fp:
            fp.write(txt.replace('\r\n', '\n'))
    return dest


uglifycmd = Command('uglifyjs', '{src} {opts} -o {dst}',
                    requirements=('nodejs', 'npm', 'uglify'))


@requires('nodejs', 'npm', 'uglify')
@task
def uglifyjs(ctx,
             src, dst,
             compress=True, mangle=True):
    uglifycmd(
        ctx,
        src=src,
        dst=dst,
        compress=compress,
        mangle=mangle
    )
    return dst


ns = Collection(babel, browserify, uglifyjs)
ns.configure({
    'static': 'static/{pkg.name}'
})
