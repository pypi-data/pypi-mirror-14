# -*- coding: utf-8 -*-


from invoke import ctask as task

from . import Package


@task(
    default=True
)
def publish(ctx, force=False):
    """Publish to PyPi
    """
    pkg = Package()
    with pkg.root.cd():
        if force:  # pramga: nocover
            ctx.run("python setup.py sdist bdist_wheel")
            ctx.run("python setup.py build_sphinx")
            ctx.run("python setup.py sdist bdist_wheel upload")
            ctx.run("python setup.py upload_docs")
        else:
            ctx.run("python setup.py sdist")
            print 'You need to add --force to invoke the upload commands'
