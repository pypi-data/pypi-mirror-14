#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2015 Martin Heistermann <github[]mheistermann.de>

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

import sys
import shutil
import os.path
import argparse
import subprocess
import urllib.parse
import configparser

package_root = os.path.abspath(os.path.dirname(__file__))
example_path = os.path.join(package_root, 'remotes.conf.example')

class InputError(Exception):
    pass


class UploadError(Exception):
    pass


def upload(filename, rsync_remote):
    rsync_path = shutil.which('rsync')
    proc = subprocess.Popen([
        rsync_path,
        '--progress',
        '--protect-args', # no space-splitting; wildcard chars only
        '--copy-links',   # transform symlink into referent file/dir
                          # (useful for git-annex files)
        '--chmod=F644,D755',
        filename,
        rsync_remote])

    proc.communicate()

    if proc.returncode != 0:
        raise UploadError()


def readConfig():
    config = configparser.ConfigParser()
    config_path = os.path.expanduser('~/.config/cliPublish/remotes.conf')
    try:
        with open(config_path) as fp:
            config.read_file(fp)
    except FileNotFoundError:
        raise InputError("Warning: config file not found at {}.\nThere is an example config at {}.".format(config_path, example_path))


    remotes = config.sections()
    if len(remotes) == 0:
        raise InputError('No remote defined, please edit config.')
    if len(remotes) > 1:
        print("Warning: more than one remote defined, using the first one",
              file=sys.stderr)

    return config[remotes[0]]


def cli():
    parser = argparse.ArgumentParser(
        description='Upload a file and show its URL.\n',
        epilog='Sample config location is {}'.format(example_path))
    parser.add_argument('file', type=str,
                        help='the file to upload')
    parser.add_argument('remoteName', type=str, nargs='?',
                        help='filename on the remote server')
    args = parser.parse_args()

    remote_name = args.remoteName or os.path.split(args.file)[-1]
    if '/' in remote_name:
        raise InputError('No slash (/) allowed in remote name.')

    config = readConfig()
    try:
        upload(args.file, config["rsync_path"] + remote_name)
    except UploadError:
        print("Upload failed.", file=sys.stderr)
        return 1
    url = config["url_prefix"] + urllib.parse.quote(remote_name)
    print(url)
    return 0



def main():
    try:
        ret = cli()
    except InputError as e:
        print('Input error: ' + e.message, file=sys.stderr)
        ret = 1
    sys.exit(ret)

if __name__ == '__main__':
    main()
