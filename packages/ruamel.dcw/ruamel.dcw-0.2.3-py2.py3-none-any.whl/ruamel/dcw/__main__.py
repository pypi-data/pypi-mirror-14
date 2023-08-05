# coding: utf-8

from __future__ import print_function
from __future__ import absolute_import

import sys                                   # NOQA
import os                                    # NOQA
import traceback                             # NOQA
import ruamel.yaml                           # NOQA
from ruamel.std.pathlib import Path          # NOQA
from ruamel.showoutput import show_output    # NOQA

from ruamel.dcw import __version__

dbg = int(os.environ.get('DCWDBG', 0))


class DockerComposeWrapper(object):
    def __init__(self):
        self._args = None
        self._file_name = None
        self._data = None
        self._show_help = False
        for p in sys.path:
            pp = os.path.join(p, 'docker-compose')
            if dbg > 0:
                print('pp', pp)
            if os.path.exists(pp):
                self._dc = pp
                break
        else:
            print(sys.path)
            print('docker-compose not found in path')
            sys.exit(1)

    def process_args(self, args):
        if (len(args) > 1) and args[0] in ['-f', '--file']:
            self._file_name = self.find_yaml(args[1])
            self._args = args[2:]
        elif (len(args) > 0) and (args[0].startswith('--file=') or args[0].startswith('-f=')):
            self._file_name = self.find_yaml(args[0].split('=', 1)[1])
            self._args = args[1:]
        else:
            self._file_name = Path('docker-compose.yml')
            self._args = args
        if args and args[0] in ['version', '--version']:
            print('dcw', __version__)
            self._show_help = True

    def find_yaml(self, name):
        for file_name in [
            Path(name),                                         # full path
            Path(name) / 'docker-compose.yml',                  # base dir
            Path('/opt/docker') / name / 'docker-compose.yml',  # standard docker dir
        ]:
            if file_name.exists():
                # print('Found', file_name)
                file_name.parent.chdir()
                return file_name

    def load_yaml(self):
        if self._show_help:
            self._data = {}
            return
        with self._file_name.open() as fp:
            self._data = ruamel.yaml.load(fp, Loader=ruamel.yaml.RoundTripLoader)

    def set_os_env_defaults(self):
        if self._show_help:
            return
        envs = self._data.get('user-data', {}).get('env-defaults')
        if envs is None:
            return
        # some values that can be <named in
        host_name_file = Path('/etc/hostname')
        lookup = {}
        lookup['hostname'], lookup['domain'] = host_name_file.read_text().strip().split('.', 1)
        # assume hostname is in the hosts file
        hosts_file = Path('/etc/hosts')
        for line in hosts_file.read_text().splitlines():
            sline = line.split('#')[0].split()
            if lookup['hostname'] in sline:
                lookup['hostip'] = sline[0]
        # print(lookup)
        env_inc = Path('.dcw_env_vars.inc')
        fp = None
        if not self._show_help and not env_inc.exists() or (env_inc.stat().st_mtime <
                                                            self._file_name.stat().st_mtime):
            print('writing', str(env_inc))
            fp = env_inc.open('w')
        for k in envs:
            if k not in os.environ:
                value = str(envs[k])
                if value and value[0] == '<':
                    value = lookup.get(value[1:], value)
                os.environ[k] = value  # str for those pesky port numbers
            if fp:
                fp.write(u'export {}="{}"\n'.format(k, os.environ[k]))
        if fp:
            fp.close()
        # print(env_inc.read_text())
        # sys.exit(1)

    def write_temp_file_call_docker_compose(self):
        odata = ruamel.yaml.comments.CommentedMap()
        for k in self._data:
            try:
                if k == 'user-data' or k.startswith('user-data-'):
                    continue
            except TypeError:
                pass
            odata[k] = self._data[k]
        sys.argv = [self._dc]
        if not self._show_help:
            alt_yaml = Path('.dcw_alt.yml')
            ruamel.yaml.round_trip_dump(odata, stream=alt_yaml.open('wb'),
                                        encoding='utf-8')
            sys.argv.append('--file={}'.format(alt_yaml))
        sys.argv.extend(self._args)
        # print(sys.argv)
        try:
            import compose.cli.main
        except ImportError:

            print(sys.path)
        compose.cli.main.main()


def main():
    if dbg > 0:
        print('---------------------------------')

    dcw = DockerComposeWrapper()
    dcw.process_args(sys.argv[1:])
    dcw.load_yaml()
    dcw.set_os_env_defaults()
    sys.exit(dcw.write_temp_file_call_docker_compose())

if __name__ == "__main__":
    main()
