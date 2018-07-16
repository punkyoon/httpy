# HTTP Request

import re
import logging
from protocol.exception import HttpParseException


log = logging.getLogger('httpy.server')


class HttpRequest:
    def __init__(self, method, request_uri, protocol, header):
        self.method = method
        self.request_uri = request_uri
        self.protocol = protocol
        self.header = header

    def __str__(self):
        return 'HttpRequest - {method} / {uri} / {protoc}'.format(
            method=self.method,
            uri=self.request_uri,
            protoc=self.protocol
        )

    def is_range_requested(self):
        return 'Range' in self.headers

    def get_range(self):
        range_header_value = None

        if self.is_range_requested():
            range_header_value = self.headers['Range']

        if range_header_value:
            range_start, range_end = None, None

            basic_range = re.findall(r'\d+', range_header_value)
            range_start= int(basic_range[0])

            if len(basic_range) > 1:
                range_end = int(range[1])

            print(basic_range)
            return range_start, range_end

        return None, None


def parse_http_request(data):
    if not data:
        err = 'Input params must be provided'
        Log.error(err)
        raise HttpParseException(err)

    data_lines = data.splitlines(False)
    request_line = data_lines[0]
    request_cmpt = request_line.split(' ')

    print(data_lines)

    if len(request_cmpt) != 3:
        err = 'Cannot parse HTTP request line: {}'.format(request_line)
        Log.error(err)
        raise HttpParseException(err)

    method = request_cmpt[0]
    request_uri = request_cmpt[1]
    protocol = request_cmpt[2]
    header = {}

    for line in data_lines[1:]:
        if not line:
            break

        line_cmpt = line.split(': ')
        if len(line_cmpt) != 2:
            err = 'Cannot parse HTTP header line: {}'.format(line)
            Log.error(err)
            raise HttpParseException(err)

        key, value = line_cmpt[0], line_cmpt[1]
        header[key] = value

    return HttpRequest(method, request_uri, protocol, header)
