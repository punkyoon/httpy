# HTTP respnose

import logging
from protocol.status_code import HTTP_STATUS_CODE


log = logging.getLogger('httpy.response')


class HttpResponse:
    def __init__(self, protocol, status, basic_range=None):
        assert status in HTTP_STATUS_CODE, 'Unknown status code'

        self.protocol = protocol
        self.status = status
        self.header = dict()
        self.basic_range = basic_range
        self.content = ''
        self.file_data = None

    def __str__(self):
        return 'HttpRequest - {protocol} / {status}'.format(
            protocol=self.protocol,
            status=self.status
        )

    def write_to(self, output):
        if self.file_data:
            self.header['Content-Type'] = self.file_data.mime_type
            self.header['Content-Length'] = self.file_data.file_size
            self.header['Accept-Ranges'] = 'bytes'

            if self.basic_range:
                range_start, range_end = self.file_data.calculate_range(
                    self.basic_range
                )

                self.header['Content-Range'] = 'bytes {}-{}/{}'.format(
                    range_start,
                    range_end,
                    self.file_data.file_size
                )

                self.header['Content-Length'] = range_end - range_start + 1

        response_msg = render_http_response(self)
        output.sendall(response_msg.encode('utf-8'))

        log.debug('Response: {}\n'.format(response_msg))

        if self.file_data:
            self.file_data.stream_to(
                output, basic_range=self.file_data.calculate_range(self.basic_range)
            )


def render_http_response(response):
    rtn = []

    response_line = '{} {} {}'.format(
        response.protocol,
        response.status,
        HTTP_STATUS_CODE[response.status][0]
    )

    rtn.append(response_line)

    for key, value in response.header.items():
        header_line = '{}: {}'.format(key, value)
        rtn.append(header_line)

    rtn.append('')

    if response.content:
        rtn.append(response.content)
    else:
        rtn.append('')

    return '\n'.join(rtn)
