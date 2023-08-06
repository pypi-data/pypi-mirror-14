import shutil
import os
import glob
import tempfile
import datetime
import pytz
import logging

log = logging.getLogger(__name__)

from pyunpack import Archive

def unpack(archive_path, output_dir, auto_create_dir=True):
    archive = Archive(archive_path)
    archive.extractall(output_dir, auto_create_dir=auto_create_dir)

class Unpack(object):

    def __init__(self, archive_file, tempdir=None):
        self.archive_file = archive_file
        if tempdir is not None:
            self.tempdir = tempdir
        else:
            self.tempdir = tempfile.mkdtemp()
        self.output_dir = os.path.join(self.tempdir, os.path.basename(archive_file))
        self.unpack()

    def unpack(self):
        unpack(self.archive_file, self.output_dir)

    def get_file(self, filepattern):
        filepath = os.path.join(self.output_dir, filepattern)
        filepathes = glob.glob(filepath)
        if len(filepathes) > 1:
            log.warning('Files with pattern "{}" > 1'.format(filepattern))
        if filepathes:
            filepath = filepathes[0]
        else:
            raise ValueError('File with pattern {} not found'.format(filepattern))
        with open(filepath) as f:
            return f.read()

    def get_file_stat(self, filename):
        return os.stat(os.path.join(self.output_dir, filename))

    def get_file_modify_datetime(self, filename, tz=pytz.utc):
        stat = self.get_file_stat(filename)
        return datetime.datetime.fromtimestamp(stat.st_mtime, tz=tz)

    def __del__(self):
        shutil.rmtree(self.tempdir, ignore_errors=True)
