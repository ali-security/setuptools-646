import os
import platform

import pytest


collect_ignore = []


if platform.system() != 'Windows':
    collect_ignore.extend(
        [
            'distutils/command/bdist_msi.py',
            'distutils/msvc9compiler.py',
        ]
    )


@pytest.fixture
def save_env():
    orig = os.environ.copy()
    try:
        yield
    finally:
        for key in set(os.environ) - set(orig):
            del os.environ[key]
        for key, value in orig.items():
            if os.environ.get(key) != value:
                os.environ[key] = value


@pytest.fixture
def needs_zlib():
    pytest.importorskip('zlib')


@pytest.fixture
def distutils_managed_tempdir(request):
    from distutils.tests import py38compat as os_helper
    self = request.instance
    self.old_cwd = os.getcwd()
    self.tempdirs = []
    try:
        yield
    finally:
        # Restore working dir, for Solaris and derivatives, where rmdir()
        # on the current directory fails.
        os.chdir(self.old_cwd)
        while self.tempdirs:
            tmpdir = self.tempdirs.pop()
            os_helper.rmtree(tmpdir)
