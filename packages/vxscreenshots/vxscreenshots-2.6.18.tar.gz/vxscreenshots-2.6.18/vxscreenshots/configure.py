# -*- coding: UTF-8 -*-
'''Following this strategy_ we simply go to the 

.. _strategy: http://askubuntu.com/questions/48321/how-do-i-start-applications-automatically-on-login  # noqa
'''
from os.path import dirname, join, expanduser, isfile
from os import listdir
from shutil import copy2

HOME = expanduser("~")


class Configure(object):

    def __init__(self):
        self.shutter = False
        self.vxssicon = False
        self.vxsswatcher = False

    def set_startup(self):
        origin = join(dirname(__file__), 'config', 'autostart')
        dest = join(HOME, '.config', 'autostart')
        overwrite = False
        for o in listdir(origin):
            if isfile(join(dest, o)):
                overwrite = raw_input('File %s already exists do you want '
                                      'everwrite it? [Yy/Nn]' % join(dest, o))
                if overwrite in ('Y', 'y', 'yes', 'YES'):
                    overwrite = True
                else:
                    overwrite = False
                if not overwrite:
                    print('Ignoring file %s' % join(dest, o))
                if overwrite:
                    print('Overwriting file %s' % join(dest, o))
                    copy2(join(origin, o), join(dest, o))
                    overwrite = False
            if isfile(join(origin, o)) and not isfile(join(dest, o)):
                copy2(join(origin, o), join(dest, o))
                print('Copying file %s' % join(dest, o))
