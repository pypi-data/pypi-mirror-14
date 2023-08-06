#! /usr/bin/env python
# -*- coding: UTF-8 -*-

from os import makedirs
from os.path import isdir, isfile, dirname, splitext, basename
import time
import logging
import boto3
import click
import sqlite3
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from .config import read_config
from contextlib import closing

__version__ = '2.6.19'

config = read_config()


class S3Element(LoggingEventHandler):

    def __init__(self, bucket, folder):
        super(LoggingEventHandler, self).__init__()
        self.folder = folder
        self.bucket = bucket
        self.url = ''
        self.db = config.get('vxscreenshots.database')
        self.format_logging()
        self.valid_ext = ['.png', '.jpg', '.gif', '.jpeg']
        if not isdir(dirname(self.db)):
            makedirs(dirname(self.db))
        self.logger.info('Cache dbname: %s' % self.db)
        self.logger.info('Bucket name: %s' % self.bucket)
        self.logger.info('Folder name: %s' % self.folder)

    def format_logging(self, log_level='INFO'):
        root = logging.getLogger()
        if root.handlers:
            for handler in root.handlers:
                root.removeHandler(handler)
                logging.basicConfig(format='%(asctime)s: %(name)s: '
                                    '%(levelname)s: %(message)s',
                                    level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def get_path(self, src_path):
        return '{}/{}'.format(self.folder, src_path)

    def get_url(self, fname):
        return "http://{bucket}/{fname}".format(bucket=self.bucket,
                                                fname=fname)

    def on_modified(self, event):
        what = 'directory' if event.is_directory else 'file'
        self.send_to_s3(what, event)

    def send_to_s3(self, what, event):
        def db_insert_new(images):
            conn = sqlite3.connect(self.db)
            with closing(conn.cursor()) as cursor:
                cursor.executemany('''INSERT INTO
                                        stock_images VALUES
                                    (?,?,?,CURRENT_TIMESTAMP)''',
                                   images)
                conn.commit()
                self.logger.warning('Inserted on db %s %s' % (event.src_path,
                                                              self.url))
        self.logger.info("Screenshot was Modified %s: %s", what,
                         event.src_path)
        name, ext = splitext(event.src_path)
        if what != 'directory' and \
           isfile(event.src_path) and \
           ext in self.valid_ext:
            try:
                s3 = boto3.resource('s3')
                data = open(event.src_path, 'rb')
                fname = self.get_path(basename(data.name))
                db_insert_new([(event.src_path, self.url, True)])
                bucket = s3.Bucket(self.bucket)
                bucket.put_object(Key=fname, Body=data, ACL='public-read',
                                  ContentType='image/%s' % ext[1:])
                self.url = self.get_url(fname)
                self.logger.info("Screenshot was pushed to %s" % self.url)
            except Exception, e:
                self.logger.warning('I could not save %s' % e)


def start_watcher(path, handler):
    observer = Observer()
    if not isdir(path):
        makedirs(path)
    observer.schedule(handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except IOError:
        handler.logger.info('A crazy file changed')
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(__version__)
    ctx.exit()


@click.command()
@click.option('--path', default=config.get('vxscreenshots.supervised'),
              help='Path to be supervised')
@click.option('--bucket', default=config.get('vxscreenshots.bucket_name'),
              help='Bucket where things will be saved to')
@click.option('--folder', default=config.get('vxscreenshots.folder'),
              help='Inside the bucket how the folder will be named')
@click.option('--version', is_flag=True, callback=print_version,
              expose_value=False, is_eager=True)
def cli(path, bucket, folder):
    '''Watch a folder and push images automatically to amazon S3'''
    event_handler = S3Element(bucket, folder)
    msg = 'Sending to this bucket %s %s %s' % (bucket, folder, path)
    event_handler.logger.info(msg)
    start_watcher(path, event_handler)
if __name__ == "__main__":
    cli()
