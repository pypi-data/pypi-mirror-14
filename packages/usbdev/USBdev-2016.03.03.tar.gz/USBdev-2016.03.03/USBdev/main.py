#!/usr/bin/env python
# -*- coding: utf-8 -*-

# main.py file is part of USBdev.

# Copyright 2015 Dimitris Zlatanidis <d.zlatanidis@gmail.com>
# All rights reserved.

# USBdev is a tool recognition of USB devices.

# https://github.com/dslackw/USBdev

# USBdev is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import sys
import time
import usb.core
from __metadata__ import (
    __prog__,
    __version__,
    __lib_path__
)


def usb_ids():
    """ find plugin usb devices """
    dict_ids = {}
    dev = usb.core.find(find_all=True)
    for cfg in dev:
        dict_ids[hex(cfg.idVendor)] = hex(cfg.idProduct)
    return dict_ids


def repository():
    """ read usb ids repository """
    with open(__lib_path__ + 'usb.ids', 'r') as f:
        return f.read()


def fixID(ven_id):
    """ convert id from hex to string """
    len_id = len(ven_id)
    if len_id < 4:
        return('0' * (4 - len_id) + ven_id)
    return ven_id


def usbDatabase():
    """ create usb database dictionary with vendor name
    as key and products name as value """
    data = {}
    for line in repository().splitlines():
        if line and not line.startswith('\t'):
            vn = line.strip()
            data[vn] = []
        if line.startswith('\t'):
            data[vn] += [line.strip()]
    return data


def findUSB(diff):
    """ return usb vendor name and device name """
    usbFind = {}
    vendID, prodID = '', ''
    for ven, pro in diff.items():
        if ven:
            vendID = fixID(ven[2:])
        if pro:
            prodID = fixID(pro[2:])
        for key, value in usbDatabase().iteritems():
            if vendID == key[:4]:
                vn = '{0} ({1})'.format(key[5:].strip(), vendID.strip())
                usbFind[vn] = '{0} ({1})'.format('Not found', vendID.strip())
                for v in value:
                    if prodID in v:
                        usbFind[vn] = '{0} ({1})'.format(v[5:].strip(),
                                                         prodID.strip())
    return usbFind


def daemon(stb):
    """ main loop recognize if usb plugin """
    sys.stdout.write('Plugin USB device(s) now ...')
    sys.stdout.flush()
    count = 0
    try:
        while True:
            before = usb_ids()
            time.sleep(stb)
            count += 1
            sys.stdout.write('.')
            sys.stdout.flush()
            after = usb_ids()
            diff = dict(set(after.items()) - set(before.items()))
            if diff or count == 60:
                sys.stdout.write('Done')
                break
        return diff
    except KeyboardInterrupt:
        return {}


def options():
    """USBdev is a tool recognition of USB devices

Optional  arguments:
  -h, --help               Display this help and exit
  -v, --version            Print program version and exit
  -t, --time [sec]         Waiting time before plugin"""
    sys.exit(options.__doc__)


def usage():
    """Usage: usbdev [-h] [-v] [-t [sec]]"""
    sys.exit(usage.__doc__)


def version():
    """ print version and exit """
    sys.exit('Version: {0}'.format(__version__))


def arguments():
    """ CLI control """
    args = sys.argv
    args.pop(0)
    if len(args) == 1 and args[0] in ['-h', '--help']:
        options()
    elif len(args) == 1 and args[0] in ['-v', '--version']:
        version()
    elif len(args) == 2 and args[0] in ['-t', '--time']:
        try:
            return int(args[1])
        except ValueError:
            print('{0}: Error: integer required'.format(__prog__))
            sys.exit()
    elif len(args) == 0:
        return 1
    else:
        usage()


def main():

    stb = arguments()
    found = daemon(stb)
    venLenght = 20
    for ven in findUSB(found).keys():
        if len(ven) > venLenght:
            venLenght = len(ven)
    print('')
    if found:
        count = 0
        print('Found: Vendor(s) {0} Device(s)'.format(' ' * (venLenght - 9)))
        for key, value, in findUSB(found).iteritems():
            count += 1
            print("{0}:     {1} {2} {3}".format(
                count, key, ' ' * (venLenght - len(key)), value))
    else:
        print('No device found')

if __name__ == '__main__':
    main()
