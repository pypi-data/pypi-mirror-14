from __future__ import print_function
from __future__ import unicode_literals

import contextlib
import distutils.sysconfig
import os
import pipes
import shutil
import subprocess
import sys
import tempfile

from setuptools.command.build_ext import build_ext as _build_ext


PYPY = '__pypy__' in sys.builtin_module_names


def _get_cflags(compiler):
    return ' '.join('-I{}'.format(p) for p in compiler.include_dirs)


def _get_ldflags_pypy():
    if PYPY:  # pragma: no cover (pypy only)
        return '-L{} -lpypy-c'.format(
            os.path.dirname(os.path.realpath(sys.executable)),
        )
    else:
        return None


def _get_ldflags_pkg_config():
    try:
        return subprocess.check_output((
            'pkg-config', '--libs',
            'python-{}.{}'.format(*sys.version_info[:2]),
        )).decode('UTF-8').strip()
    except (subprocess.CalledProcessError, OSError):
        return None


def _get_ldflags_bldlibrary():
    return distutils.sysconfig.get_config_var('BLDLIBRARY')


def _get_ldflags():
    for func in (
            _get_ldflags_pypy,
            _get_ldflags_pkg_config,
            _get_ldflags_bldlibrary,
    ):
        ret = func()
        if ret is not None:
            return ret
    else:
        raise AssertionError('Could not determine ldflags!')


def _print_cmd(env, cmd):
    envparts = [
        '{}={}'.format(k, pipes.quote(v))
        for k, v in sorted(tuple(env.items()))
    ]
    print(
        '$ {}'.format(' '.join(envparts + [pipes.quote(p) for p in cmd])),
        file=sys.stderr,
    )


@contextlib.contextmanager
def _tmpdir():
    tempdir = tempfile.mkdtemp()
    try:
        yield tempdir
    finally:
        shutil.rmtree(tempdir)


def _get_build_extension_method(base, root):
    def build_extension(self, ext):
        def _raise_error(msg):
            raise IOError(
                'Error building extension `{}`: '.format(ext.name) + msg,
            )

        # If there are no .go files then the parent should handle this
        if not any(source.endswith('.go') for source in ext.sources):
            return base.build_extension(self, ext)

        if len(ext.sources) != 1:
            _raise_error(
                'sources must be a single file in the `main` package.\n'
                'Recieved: {!r}'.format(ext.sources)
            )

        main_file, = ext.sources
        if not os.path.exists(main_file):
            _raise_error('{} does not exist'.format(main_file))
        main_dir = os.path.dirname(main_file)

        # Copy the package into a temporary GOPATH environment
        with _tmpdir() as tempdir:
            root_path = os.path.join(tempdir, 'src', root)
            # Make everything but the last directory (copytree interface)
            os.makedirs(os.path.dirname(root_path))
            shutil.copytree('.', root_path)
            pkg_path = os.path.join(root_path, main_dir)

            env = {
                'GOPATH': tempdir,
                'CGO_CFLAGS': _get_cflags(self.compiler),
                'CGO_LDFLAGS': _get_ldflags(),
            }
            cmd_get = ('go', 'get')
            _print_cmd(env, cmd_get)
            subprocess.check_call(
                cmd_get, cwd=pkg_path, env=dict(os.environ, **env),
            )

            cmd_build = (
                'go', 'build', '-buildmode=c-shared',
                '-o', os.path.abspath(self.get_ext_fullpath(ext.name)),
            )
            _print_cmd(env, cmd_build)
            subprocess.check_call(
                cmd_build, cwd=pkg_path, env=dict(os.environ, **env),
            )

    return build_extension


def _get_build_ext_cls(base, root):
    class build_ext(base):
        build_extension = _get_build_extension_method(base, root)

    return build_ext


def set_build_ext(dist, attr, value):
    root = value['root']
    base = dist.cmdclass.get('build_ext', _build_ext)
    dist.cmdclass['build_ext'] = _get_build_ext_cls(base, root)
