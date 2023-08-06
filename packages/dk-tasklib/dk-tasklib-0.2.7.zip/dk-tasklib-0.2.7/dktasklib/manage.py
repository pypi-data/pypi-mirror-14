# -*- coding: utf-8 -*-
import os

from dkfileutils.path import Path
from dkfileutils.pfind import pfind
from dkfileutils.changed import changed
from invoke import ctask as task, run
from .utils import cd, env, find_pymodule
from .package import Package


DEFAULT_SETTINGS_MODULE = 'settings'
# DEFAULT_MANAGE_PY_PATH = os.path.join(os.environ.get('SRV', ''), 'src', 'datakortet')


@task
def manage(ctx, cmd, settings=None, manage_path=None, venv=None):
    """Run manage.py with `settings` in a separate process.
    """
    settings = settings or DEFAULT_SETTINGS_MODULE
    with env(DJANGO_SETTINGS_MODULE=settings):
        if manage_path is None:
            settings_dir = find_pymodule(settings)
            manage_path = Path(pfind(settings_dir, 'manage.py')).dirname()

        with cd(manage_path):
            # print "MANAGE_PATH:", manage_path
            # print "CWD:", os.getcwd()
            # run('python -c "import sys;print sys.path"')
            # run('vex dev python -c "import sys;print chr(10).join(sys.path)"')
            # run("python -c \"import sys;print '\n'.join(sys.path)\"")

            call = "python manage.py {cmd}"
            if venv:
                call = "vex {venv} python manage.py {cmd}"

            run(call.format(venv=venv, cmd=cmd))


@task
def collectstatic(ctx, settings=None, venv=None):
    "Run collectstatic with settings from package.json ('django_settings_module')"
    if not hasattr(ctx, 'pkg'):
        ctx.pkg = Package()

    try:
        settings = settings or ctx.pkg.django_settings_module
    except AttributeError:
        settings = DEFAULT_SETTINGS_MODULE
    print "using settings:", settings, 'venv:', venv
    manage(ctx, "collectstatic --noinput", settings=settings, venv=venv)
    # record changes made by collectstatic
    changed(ctx.pkg.staticdir)
