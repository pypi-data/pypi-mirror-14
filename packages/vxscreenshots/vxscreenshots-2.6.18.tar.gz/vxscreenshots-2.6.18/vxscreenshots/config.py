# -*- coding: UTF-8 -*-

import os
from os import makedirs
import logging
import ConfigParser
from os.path import dirname, join, expanduser, isdir, isfile
HOME = expanduser("~")


try:
    import pwd
except ImportError:
    import getpass
    pwd = None


def current_user():
    if pwd:
        return pwd.getpwuid(os.geteuid()).pw_name
    else:
        return getpass.getuser()


def get_template_config(cfg):
    dirconfig = dirname(cfg)
    content = '''[vxscreenshots]
database={dbconfig}
supervised={supervised}
folder={username}
bucket_name={bucket}
    '''.format(dbconfig=join(dirconfig, 'cache.db'),
               supervised=join(HOME, 'Pictures', 'screenshots'),
               username=current_user(),
               bucket='screenshots.yourdomain.com')
    return content


def read_config():
    cfg = join(HOME, '.vxscreenshots', 'vxscreenshots.ini')
    parser = ConfigParser.RawConfigParser()
    rv = {}
    if not isdir(dirname(cfg)):
        makedirs(dirname(cfg))
    if not isfile(cfg):
        logging.info('Creating config file %s' % cfg)
        with open(cfg, 'a+') as configfile:
            configfile.write(get_template_config(cfg))
    parser.read([cfg])
    logging.info('Reading config file %s' % cfg)
    for section in parser.sections():
        for key, value in parser.items(section):
            rv['%s.%s' % (section, key)] = value
    if not rv:
        logging.error('No Config file I will fail %s' % cfg)
        exit()
    return rv
