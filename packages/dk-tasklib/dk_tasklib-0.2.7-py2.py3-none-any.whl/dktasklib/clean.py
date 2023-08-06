# -*- coding: utf-8 -*-

from invoke import ctask as task


@task
def clean(ctx, directory):
    """Remove all contents from build subdirectory `directory`.
    """
    ctx.run("rm -rf build/{directory}/*".format(directory=directory))
