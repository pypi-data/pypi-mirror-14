# coding: utf-8

from __future__ import print_function
from __future__ import absolute_import

import sys
import os

from ruamel.std.pathlib import Path


class VirtualEnvUtils(object):
    def __init__(self, args, config):
        self._args = args
        self._config = config
        self._venv_dirs = None

    def alias(self):
        aliases = dict()
        keys = []
        venv_dirs = self.venv_dirs[:]
        for d in venv_dirs[:]:
            # check for configuration file
            conf = d / 'virtualenvutils.conf'
            if not conf.exists():
                continue
            venv_dirs.remove(d)
            # print('conf file', d, file=sys.stderr)
            for line in conf.read_text().splitlines():
                line = line.strip()
                if not line:
                    continue
                # print('line', line, file=sys.stderr)
                if u':' in line:
                    util, full = line.strip().split(u":", 1)
                    full = d / 'bin' / full
                else:
                    util = line
                    full = d / 'bin' / util
                if not full.exists():
                    print('cannot find {}\n  from line {}\  in {}'.format(
                        full, line, conf), file=sys.stderr)
                if util in aliases:
                    print('virtualenvutils name clashes {}\n  {}\n  {}'.format(
                        util,
                        util,
                        aliases[util],
                        ), file=sys.stderr)
                else:
                    aliases[util] = full
                    keys.append(util)
        for d in venv_dirs[:]:
            util = d / 'bin' / (d.stem)
            if not util.exists():
                continue
            venv_dirs.remove(d)
            # print('matching virtualenv name', d, file=sys.stderr)
            if util.name in aliases:
                print('virtualenvutils name clashes {}\n  {}\n  {}'.format(
                    util.name,
                    util,
                    aliases[util.name],
                    ), file=sys.stderr)
            else:
                aliases[util.stem] = util
                keys.append(util.stem)
        for d in venv_dirs[:]:
            for util in (d / 'bin').glob('*'):
                if not util.is_file():
                    continue
                for skip in ['activate', 'easy_install', 'python', 'pip', 'wheel']:
                    if util.stem.startswith(skip):
                        break
                else:
                    if d in venv_dirs:  # only first time
                        venv_dirs.remove(d)
                    if util.name.endswith('.so'):
                        continue
                    if util.name.endswith('.pyc'):
                        continue
                    if util.name.endswith('.py'):
                        # can make xyz.py into util xyz, or skip. Yeah, skip
                        continue
                    if util.name in aliases:
                        if self._args.verbose > 0:
                            print('skipping name clashes {}\n  {}\nin favor of\n  {}'.format(
                                util.name,
                                util,
                                aliases[util.name],
                                ), file=sys.stderr)
                    else:
                        aliases[util.name] = util
                        keys.append(util.name)
        assert not venv_dirs
        for k in keys:
            print("alias {}='{}'".format(k, aliases[k]))

    @property
    def venv_dirs(self):

        def test_a_dir(sub_dir):
            if not sub_dir.is_dir():
                return False
            for x in ('bin', 'lib', 'include'):
                sub_sub_dir = sub_dir / x
                if not sub_sub_dir.exists():
                    break
                if not sub_sub_dir.is_dir():
                    break
            else:
                activate = sub_dir / 'bin' / 'activate'
                if activate.exists() and activate.is_file():
                    self._venv_dirs.append(sub_dir)
                    return True
            return False

        if self._venv_dirs is not None:
            return self._venv_dirs
        self._venv_dirs = []
        for d in self._args.dir:
            d = Path(d).expanduser()
            if test_a_dir(d):
                continue
            for sub_dir in d.glob('*'):
                test_a_dir(sub_dir)
        return self._venv_dirs

    def update(self):
        import pkgutil  # NOQA
        import pkg_resources  # NOQA
        # pkg_resources.working_set is what pip relies upon, that is bound to the
        # pip/python that is running
        # print('x', [x for x in pkg_resources.working_set])
        # print('pip', pip.__file__)
        pip_args = ['list', '--outdated']
        pre = ['--pre'] if self._args.pre else []
        has_run = False
        for d in self.venv_dirs:
            has_run = True
            pip_cmd = [str(d / 'bin' / 'pip')]
            res = [x.split(None, 1)[0] for x in check_output(
                pip_cmd + pip_args + pre).splitlines()]
            print('update', d, res)
            # NOT WORKING: this gives you the packages from the calling environment
            # for package in pip.get_installed_distributions():
            #     print('package', package)
            #
            # for p in (d / 'lib').glob('python*'):
            #     if p:
            #         break
            # else:
            #     continue  # no lib/python* found
            # pth = [str(p / 'site-packages')]
            # NOT WORKING: does give you only toplevel names and not in original dotted
            #              package form
            # for pkg in pkgutil.iter_modules(path=pth):
            #     continue
            #     if pkg[2]:
            #         print('pkg', pkg[1])
            #
            # NOT WORKING: only gives non-namespace packages
            # for pkg in pkgutil.walk_packages(path=pth):
            #     continue
            #     if pkg[2]:
            #         print('pkg', pkg[1])
            #
            if res:
                print(check_output(pip_cmd + ['install', '-U'] + pre + res))
        if not has_run:
            print('no project(s) found')

    def install(self):
        os.environ['PATH'] = os.path.dirname(sys.executable) + ':' + os.environ['PATH']
        for d in self._args.dir:
            p = Path(d)
            if self._args.pkg:
                assert len(self._venv.dirs) == 1
                pkg = self._args.pkg
            else:
                pkg = Path(d).name
            print('pkg', pkg)
            cmd = ['virtualenv']
            if self._args.python:
                cmd.extend(['--python', self._args.python])
            check_output(cmd + [str(p)], verbose=2)
            check_output([str(p / 'bin' / 'pip'), 'install', pkg], verbose=2)


def check_output(*args, **kw):
    import subprocess
    verbose = kw.pop('verbose', 0)
    if verbose > 1:
        print('cmd', args[0])
    res = subprocess.check_output(*args, **kw).decode('utf-8')
    if verbose > 0:
        print(res)
    return res

if __name__ == "__main__":
    print("change directory if you're doing python -m virtualenvutils")
