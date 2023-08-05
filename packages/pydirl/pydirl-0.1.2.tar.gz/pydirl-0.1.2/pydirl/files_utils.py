import os
import zipstream
import mimetypes
from logging import getLogger

logger = getLogger('pydirl')

def get_file_size(path):
    return os.path.getsize(path)


def get_folder_size(path):
    files_num = 0
    size = 0
    for root, dirs, files in os.walk(path):
        for name in files:
            files_num += 1
            fPath = os.path.join(root, name)
            #do not count size of link
            if not os.path.islink(fPath):
                try:
                    size += os.path.getsize(fPath)
                except OSError as e:
                    logger.exception(e)
    return size, files_num


def get_mtime(path):
    return os.path.getmtime(path)


def directory_to_zipstream(path):
    z = zipstream.ZipFile(mode='w', compression=zipstream.ZIP_DEFLATED)
    for root, dirs, files in os.walk(path):
        for file in files:
            absPath = os.path.join(root, file)
            if not os.path.exists(absPath):
                logger.debug('Skipping non existing element: {}'.format(absPath))
                continue
            if not (os.path.isfile(absPath) or os.path.isdir(absPath)):
                logger.debug('Skipping unknown element: {}'.format(absPath))
                continue
            z.write(absPath, os.path.relpath(absPath, path))
    return z

def get_file_mimetype(path):
    return mimetypes.guess_type(path)[0]
