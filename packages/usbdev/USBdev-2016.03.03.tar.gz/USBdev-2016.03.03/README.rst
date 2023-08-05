.. image:: https://img.shields.io/github/release/dslackw/USBdev.svg
    :target: https://github.com/dslackw/USBdev/releases
.. image:: https://travis-ci.org/dslackw/USBdev.svg?branch=master
    :target: https://travis-ci.org/dslackw/USBdev
.. image:: https://landscape.io/github/dslackw/USBdev/master/landscape.png
    :target: https://landscape.io/github/dslackw/USBdev/master
.. image:: https://img.shields.io/codacy/050af4c8f1574e29b7382dfc2635a1a4.svg
    :target: https://www.codacy.com/public/dzlatanidis/USBdev/dashboard
.. image:: https://img.shields.io/pypi/dm/USBdev.svg
    :target: https://pypi.python.org/pypi/USBdev
.. image:: https://img.shields.io/badge/license-GPLv3-blue.svg
    :target: https://github.com/dslackw/USBdev
.. image:: https://img.shields.io/github/stars/dslackw/USBdev.svg
    :target: https://github.com/dslackw/USBdev
.. image:: https://img.shields.io/github/forks/dslackw/USBdev.svg
    :target: https://github.com/dslackw/USBdev
.. image:: https://img.shields.io/github/issues/dslackw/USBdev.svg
    :target: https://github.com/dslackw/USBdev/issues

.. contents:: Table of Contents:

About
-----

USBdev is a USB devices recognition tool on Linux.

How works
---------

The tool compares the USB devices that is connected before and after once you 
connect to the further doors USB.
USBdev use `linux-usb.org <http://www.linux-usb.org/usb-ids.html>`_ repository to get
data devices.

 
Install
-------

.. code-block:: bash

    $ pip install USBdev
    
    or

    $ pip install USBdev-<version>.tar.gz


Uninstall
---------

.. code-block:: bash

    $ pip uninstall USBdev


Usage
-----

.. code-block:: bash

    $ usbdev
    Plugin USB device(s) now .......Done
    Found: Vendor(s)                    Device(s)
    1:     Kingston Technology (0951)   DataTraveler 100 (1607)

    
    
    Using the time to connect and recognize multiple devices.
    
    $ usbdev --time 10
    Plugin USB device(s) now .......Done
    Found: Vendor(s)                   Device(s)
    1:     Kingston Technology (0951)  DataTraveler 100 (1607)
    2:     Logitech, Inc. (046d)       Unifying Receiver (c52b)
    3:     Alcor Micro Corp. (058f)    Flash Drive (1234)

Asciicast
---------

.. image:: https://raw.githubusercontent.com/dslackw/images/master/USBdev/usbdev_asciicast.png
    :target: http://asciinema.org/a/18905
   
CLI
---

.. code-block:: bash

    USBdev is a tool recognition of USB devices

    Optional  arguments:
      -h, --help               display this help and exit
      -v, --version            print program version and exit
      -t, --time [sec]         waiting time before plugin


Copyright 
---------

- Copyright © Dimitris Zlatanidis
- Linux is a Registered Trademark of Linus Torvalds.
