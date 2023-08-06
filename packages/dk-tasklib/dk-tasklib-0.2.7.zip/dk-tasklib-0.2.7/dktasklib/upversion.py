# -*- coding: utf-8 -*-
"""
Update a package's version number.
"""

import re
import os
import textwrap
import warnings

from dkfileutils.path import Path
from invoke import ctask as task, Collection
from .rule import BuildRule
from .package import Package


def files_with_version_numbers():
    pkg = Package()
    root = pkg.root
    default = {
        root / 'setup.py',
        root / 'package.json',
        root / 'package.ini',
        root / 'package.yaml',
        root / 'docs' / 'conf.py',
        pkg.sourcedir / '__init__.py',
        pkg.sourcedir / '_version.py',
    }
    return default


def _replace_version(fname, cur_version, new_version):
    """Replace the version string ``cur_version`` with the version string
       ``new_version`` in ``fname``.
    """
    if not fname.exists():
        return False

    with open(fname, 'rb') as fp:
        txt = fp.read()

    if cur_version not in txt:  # pragma: nocover
        # warnings.warn("Did not find %r in %r" % (cur_version, fname))
        return False
    occurences = txt.count(cur_version)
    if occurences > 2:  # pragma: nocover
        warnings.warn(
            "Found version string (%r) multiple times in %r, skipping" % (
                cur_version, fname
            )
        )
    txt = txt.replace(cur_version, new_version)

    with open(fname, 'wb') as fp:
        fp.write(txt)
    return 1


@task(
    autoprint=True,
    default=True
)
def upversion(ctx, major=False, minor=False, patch=False):
    """Update package version (default patch-level increase).
    """
    pkg = Package()
    if not (major or minor or patch):
        patch = True  # pragma: nocover
    txt_version = pkg.version
    cur_version = [int(n, 10) for n in txt_version.split('.')]
    if major:
        cur_version[0] += 1
        cur_version[1] = 0
        cur_version[2] = 0
    elif minor:
        cur_version[1] += 1
        cur_version[2] = 0
    elif patch:
        cur_version[2] += 1
    new_version = '.'.join([str(n) for n in cur_version])

    changed = 0
    for fname in files_with_version_numbers():
        changed += _replace_version(fname, txt_version, new_version)
    if changed == 0:
        warnings.warn("I didn't change any files...!")  # pragma: nocover
    print "changed %d files" % changed
    return new_version


class UpdateTemplateVersion(BuildRule):
    def __call__(self, fname):
        fname = fname.format(**self.ctx)

        if not os.path.exists(fname):
            Path(self.ctx.pkg.root).makedirs(Path(fname).dirname())
            with open(fname, 'w') as fp:
                fp.write(textwrap.dedent("""
                {% load staticfiles %}
                {% with "0.0.0" as version %}
                    {# keep the above exactly as-is (it will be overwritten when compiling the css). #}
                    {% with app_path="PKGNAME/PKGNAME-"|add:version|add:".min.css" %}
                        {% if debug %}
                            <link rel="stylesheet" type="text/css" href='{% static "PKGNAME/PKGNAME.css" %}'>
                        {% else %}
                            <link rel="stylesheet" type="text/css" href="{% static app_path %}">
                        {% endif %}
                    {% endwith %}
                {% endwith %}
                """).replace("PKGNAME", self.ctx.pkg.name))

        with open(fname, 'r') as fp:
            txt = fp.read()

        newtxt = re.sub(
            r'{% with "(\d+\.\d+\.\d+)" as version',
            '{{% with "{}" as version'.format(self.ctx.pkg.version),
            txt
        )
        with open(fname, 'w') as fp:
            fp.write(newtxt)
        print 'Updated {% import %} template:', fname


ns = Collection(
    'upversion',
    upversion,
)
ns.configure({
    'force': False,
    'pkg': {
        'name': '<package-name>',
        'version': '<version-string>',
    },
})
