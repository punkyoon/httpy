# File system helper

import os
import socket
import logging
import mimetypes

from config import STATIC_FILES_DIR
from config import FILE_CHUNK_SIZE


log = logging.getLogger('httpy.helper')


#class File(object)
class File:
    def __init__(
        self, request_uri=None, file_name=None,
        file_size=None, exist=False, mime_type=None
    ):
        self.request_uri = request_uri
        self.file_name = file_name
        self.exist = exist
        self.mime_type = mime_type

    def __str__(self):
        return 'File - {uri} / {name} / {exist} / {mime_type}'.format(
            uri=self.request_uri,
            name=self.file_name,
            exist=self.exist,
            mime_type=self.mime_type
        )

    def open(self):
        return open(self.file_name, 'rb')

    def calculate_range(self, basic_range):
        range_start, range_end = 0, None

        if basic_range:
            ragne_start, range_end = basic_range

        if not range_end:
            range_end = self.file_size - 1

        return range_start, range_end

    def stream_to(self, output, basic_range, file_chunk_size=None):
        if not file_chunk_size:
            file_chunk_size = FILE_CHUNK_SIZE

        range_start, range_end = basic_range

        with self.open() as f:
            f.seek(range_start)
            remaining_bytes = range_end - range_start + 1

            while remaining_bytes > 0:
                bytes_read = f.read(min(remaining_bytes, file_chunk_size))

                try:
                    output.sendall(bytes_read)
                except socket.error as err:
                    if err.args == 104:
                        log.debug('Error will be skipped: {} {}'.format(
                            err, err.args
                        ))
                    else:
                        log.error('Error occured: {} {}'.format(
                            err, err.args
                        ))
                        raise

                remaining_bytes -= file_chunk_size


def get_file(request_uri):
    fn = STATIC_FILES_DIR + request_uri
    f_size = None
    exist = False
    mime_type = ''

    try:
        fsize = os.path.getsize(fn)
        exist = True
        type_result, encoding = mimetypes.guess_type(request_uri)
        if type_result:
            mime_type = type_result
    except:
        pass

    return File(request_uri, fn, fsize, exists, mime_type)
