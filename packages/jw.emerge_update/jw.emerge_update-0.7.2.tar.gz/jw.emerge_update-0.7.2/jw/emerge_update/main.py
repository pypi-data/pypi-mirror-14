#!/usr/bin/env python
#
# Copyright (c) 2015 Johnny Wezel
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Main program
"""
from __future__ import print_function

import io
from traceback import format_exc

import pip
from future import standard_library
from six import PY2

standard_library.install_aliases()

import platform
import pwd
import subprocess
import sys
from argparse import ArgumentParser, Action
from glob import glob
from itertools import chain
from subprocess import check_output
from time import strftime
from urllib.parse import urlsplit

import os
import re
from builtins import filter
from builtins import object
from jw.util import file
from jw.util.python3hell import Bytes2Str, SetDefaultEncoding, Open
from pkg_resources import get_distribution
from requests import head, get

SetDefaultEncoding()

JDK_FETCH_RESTRICTION_RE = re.compile(r"Fetch failed for .dev-java/oracle-jdk-bin")
JDK_FILE_RE = re.compile(r"jdk-(\w+)-linux-\w+.tar.gz")
JDK_LOG_FILE_RE = re.compile(r"\*  '(/var/tmp/portage/dev-java/oracle-jdk-bin-1.8.0.77/temp/build.log)'")
JDK_DOWNLOAD_URL = 'http://download.oracle.com/otn-pub/java/jdk/{VERSION}-b{BUILD:02}/jdk-{VERSION}-linux-{PLATFORM}.tar.gz'
PLATFORM = {'x86_32': 'x86', 'x86_64': 'x64'}[platform.machine()]

def Processors():
    """
    Get number of CPUs in system

    :return: # of CPUs
    :rtype: int
    """
    if os.path.exists('/proc/cpuinfo'):
        return len([line for line in open('/proc/cpuinfo').readlines() if line.startswith('processor\t:')])

__version__ = get_distribution('jw.emerge_update').version
VERSION_INFO = """emerge_update %s
Copyright (c) 2015 Johnny Wezel
License: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software. you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.""" % __version__

EMERGE = (
    "emerge --jobs 4 --load-average {} --nospinner --update --newuse --deep --keep-going --autounmask y "
    "--autounmask-write y".format(Processors())
)
BACKUP_DIR = '/var/lib/emerge_update'
BACKUP_GENERATIONS = 8

passwd = pwd.getpwuid(os.geteuid())
DEFAULT_ENVIRONMENT = {
    'LOGNAME': passwd.pw_name,
    'USER': passwd.pw_name,
    'HOME': passwd.pw_dir,
    'LANG': 'en_US.UTF-8',
    'PATH': '{HOME}/.local/bin:/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin'.format(HOME=passwd.pw_dir),
}

def JdkVersion(version, high=99, low=0, output=None):
    """
    Download JDK from Oracle

    :param version: version, like "8u74"
    :type version: str
    :param high: highest build
    :type high: int
    :param low:
    :type low: int
    :return: download URL
    :rtype: str

    Searches for the latest build of the JDK by binary dissection.
    """
    for guess in range(10, 0, -1):
        if high - low < 2:
            return JDK_DOWNLOAD_URL.format(VERSION=version, PLATFORM=PLATFORM, BUILD=low)
        url = JDK_DOWNLOAD_URL.format(VERSION=version, PLATFORM=PLATFORM, BUILD=guess)
        resp = get(
            url,
            allow_redirects=True,
            cookies={
                'gpw_e24': 'http://www.oracle.com/',
                'oraclelicense': 'accept-securebackup-cookie'
            }
        )
        if resp.status_code == 200:
            return JDK_DOWNLOAD_URL.format(VERSION=version, PLATFORM=PLATFORM, BUILD=guess)

def JdkDownload(version, output=None):
    url = JdkVersion(version, output=output)
    if url:
        filename = os.path.basename(urlsplit(url).path)
        resp = get(
            url,
            allow_redirects=True,
            cookies={
                'gpw_e24': 'http://www.oracle.com/',
                'oraclelicense': 'accept-securebackup-cookie'
            }
        )
        archive = '/usr/portage/distfiles/' + filename
        open(archive, 'wb').write(resp.content)
        os.chmod(archive, 0o744)
        print('Downloaded', url, file=output or sys.stdout)

def TerminalSize():
    if sys.stdout.isatty():
        import fcntl, termios, struct
        h, w, hp, wp = struct.unpack(
            'HHHH',
            fcntl.ioctl(0, termios.TIOCGWINSZ, struct.pack('HHHH', 0, 0, 0, 0))
        )
        return w, h
    else:
        return 128, 1

def grep(lines, pattern):
    if isinstance(pattern, str):
        pattern = re.compile(pattern)
    if pattern.groups:
        return next((occ.groups() for occ in (pattern.search(line) for line in lines) if occ is not None), None)
    else:
        return next((occ.group() for occ in (pattern.search(line) for line in lines) if occ is not None), None)

class Version(Action):
    """
    Action: Display version
    """

    def __call__(self, *args, **kw):
        """
        Display version
        """
        print(VERSION_INFO)
        sys.exit(0)

def Main():
    import sys

    class Program(object):
        """
        Program
        """

        def __init__(self):
            argp = ArgumentParser(description='Extended package maintenance')
            argp.add_argument('--dry-run', '-n', action='store_true', help="don't execute commands, just print them")
            argp.add_argument('--verbose', '-v', action='store_true', help="print commands as they are executed")
            argp.add_argument('--version', '-V', action=Version, nargs=0, help='display program version and license')
            argp.add_argument('--output', '-o', action='store', help='specify output file')
            argp.add_argument('--quick', '-q', action='store_true', help='quick mode')
            argp.add_argument(
                '--append', '-a', action='store_true', help='append to output file instead of overwriting'
            )
            self.args = argp.parse_args()
            self.variables = {
                'EMERGE': EMERGE
            }
            if self.args.output in ('-', None):
                self.output = sys.stdout
            else:
                self.output = Open(self.args.output, 'wa'[self.args.append], 1)

        def do(self, *args):
            """
            Run something in shell

            :param args: list of arguments which are concatenated with space
            """
            if self.args.dry_run:
                self.log(*args)
                return 0, ''
            else:
                if self.args.verbose:
                    self.log(*args)
                proc = subprocess.Popen(
                    self.subst(*args),
                    stdin=None,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    shell=True
                )
                output = [Bytes2Str(line) for line in proc.stdout.readlines()]
                status = proc.wait()
                self.output.writelines(output)
                return status, output

        def log(self, *args):
            """
            Write something to the output file
            """
            self.output.write('\n=== {}\n'.format(self.subst(*args)))
            self.output.flush()

        def subst(self, *args):
            """
            Join and substitute arguments

            :param args: list of arguments concatenated with space
            """
            return ' '.join(a.format(**self.variables) for a in args)

        def backup(self, path):
            """
            Back up a file or directory

            :param path: pathname to file
            :type path: str

            The path follows symbolic links.

            Backups are done by renaming and hard linking if possible or tar if the path is a mount point.
            """
            rpath = os.path.realpath(path)
            if os.path.ismount(rpath):
                # In this case, we can't just move the directory. A full backup is due.
                tarpath = os.path.join(BACKUP_DIR, rpath.lstrip('/').replace('/', '-') + '.tar.gz')
                if self.args.verbose or self.args.dry_run:
                    self.log('Backup', rpath, 'with tar to', tarpath, "because it's a mount point")
                if not self.args.dry_run:
                    try:
                        os.makedirs(BACKUP_DIR)
                        open(os.path.join(BACKUP_DIR, '.no-backup'), 'w')
                    except OSError as e:
                        if e.errno == 17:
                            if self.args.verbose or self.args.dry_run:
                                self.log('Created backup directory', BACKUP_DIR)
                        else:
                            raise
                self.do('tar --totals --backup=t -czf', tarpath, rpath + os.path.sep)
            else:
                # Backup by hard-linking
                if self.args.verbose or self.args.dry_run:
                    self.log('Backup', rpath, 'to', rpath + '.1')
                if not self.args.dry_run:
                    backup = file.Backup(rpath, mode=BACKUP_GENERATIONS)
                    backup()
                # Use bash to do the dirty work
                self.do('cp --link --archive {0}.1 {0}'.format(rpath))

        def updateEmerge_update(self):
            """
            Update jw.emerge-update

            :raise RuntimeError: if location could not be derived from pip show command
            """
            try:
                stdout = sys.stdout
                stderr = sys.stderr
                # Get information about package
                sys.stdout = sys.stderr = io.BytesIO() if PY2 else io.StringIO()
                pip.main(['show', 'jw.emerge-update'])
                pipInfo = sys.stdout.getvalue()
                sys.stdout.close()
                match = re.search(r'^Location: (.*)$', pipInfo, re.MULTILINE)
                if not match:
                    raise RuntimeError('Could not find location of jw.emerge-update in output of "pip show":\n' + pipInfo)
                path = match.group(1)
                # Try to figure out how package was installed
                if path.startswith(os.path.join(os.environ['HOME'], '.local', 'lib')):
                    option = [' --user']
                else:
                    option = []
                # TODO: check for custom installation locations (set with --target, --root)
                # Do update
                args = ['install', '-v', '--quiet', '--upgrade'] + option + ['jw.emerge-update']
                self.log(*['pip'] + args)
                sys.stdout = sys.stderr = self.output
                pip.main(args)
            finally:
                sys.stdout = stdout
                sys.stderr = stderr

        def run(self):
            """
            Run program
            """
            sys.stderr = self.output
            self.log(
                'emerge_update {} on {} '.format(
                    __version__, strftime('%F at %T')
                ).ljust(max(0, TerminalSize()[0] - 4) or 128, '=')
            )
            for k, v in list(DEFAULT_ENVIRONMENT.items()):
                if k not in os.environ:
                    os.putenv(k, v)
                    os.environ[k] = v
                    self.output.write('%s="%s"\n' % (k, v))
            # Try to update jw.emerge-update
            try:
                self.updateEmerge_update()
            except Exception as e:
                self.output.write(format_exc())
            # Run qcheck if not in quick mode
            if not self.args.quick:
                st, qcheckLog = self.do('qcheck --badonly')
                if qcheckLog and qcheckLog[0].startswith('Usage:'):
                    # Older versions of qcheck needed a --all/-a option to list all packages
                    st, qcheckLog = self.do('qcheck --badonly --all')
                if qcheckLog:
                    self.do('qcheck ' + ' '.join('"%s"' % p.rstrip() for p in qcheckLog))
            # Run eix-sync
            self.do('eix-sync -v -q')
            # Backup /etc if not in quick mode
            if not self.args.quick:
                self.backup('/etc')
            # Run emerge, first try
            st, emerge = self.do('{EMERGE} @world')
            retryEmerge = False
            # If changes were necessary in /etc/portage, commit them and reschedule
            if any('Autounmask changes successfully written' in line for line in emerge):
                if glob('/etc/portage/._cfg*') or glob('/etc/portage/*/._cfg*'):
                    self.log('Update config files and retry.')
                    self.do('etc-update --automode -5 /etc/portage')[1]
                    retryEmerge = True
                else:
                    self.log('Something is not quite right. Autounmask written but no ._cfg files anywhere?')
            # If JDK needs to be downloaded, do so and reschedule
            if grep(emerge, JDK_FETCH_RESTRICTION_RE):
                self.log('Download Oracle JDK')
                try:
                    jdklog = [line.rstrip() for line in open(grep(emerge, JDK_LOG_FILE_RE)[0])]
                except Exception as e:
                    print('Could not open log file:', e, file=self.output)
                else:
                    archive = grep(jdklog, JDK_FILE_RE)[0]
                    JdkDownload(archive, output=self.output)
                    retryEmerge = True
            # If second pass of emerge required, do so
            if retryEmerge:
                emerge.extend(self.do('{EMERGE} @world')[1])
            packagesInstalled = any('>>> Installing' in line for line in emerge)
            if packagesInstalled:
                # Clean old packages
                self.do('emerge --depclean')
                # Repair inconsistencies from emerge
                self.do('revdep-rebuild --ignore')
                self.do('emerge --jobs 4 --load-average {} --nospinner --keep-going @preserved-rebuild'.format(Processors()))
                # Run Python updater if Python was updated
                if any('dev-lang/python' in line for line in emerge):
                    self.do('python-updater')
                # Run Perl cleaner
                self.do('perl-cleaner --all')
                # Update configuration files
                self.do('cfg-update --update --automatic-only')
                self.do('cfg-update --optimize-backups | grep -v -- "- Skip file"')
                if not self.args.quick:
                    # Prelinking
                    self.do('prelink --all')
                    # Do system checks
                    self.do('emaint --check all')
                    # Clean old packagages
                    self.do('eclean-dist')
                    # Backup /var/db/pkg
                    self.backup('/var/db/pkg')
                    # Reset system file status if inconsistencies were detected before
                    if qcheckLog:
                        self.do('qcheck --all --update | grep -v "^Updating"')
            else:
                self.log('No package maintenance done because no packages were installed/updated')
            return 0

    program = Program()
    return program.run()

if __name__ == '__main__':
    sys.exit(Main())
