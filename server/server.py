# HTTP request handler

import socket
import logging

from thread_pool.pool import ThreadPool
from file_system.helper import get_file
from protocol.response import HttpResponse
from protocol.request import parse_http_request
from config import RECV_BUFSIZ, THREAD_POOL_SIZE, SOCKET_BACKLOG_SIZE


log = logging.getLogger('httpy.server')


def handle_request(client_sock):
    data = client_sock.recv(RECV_BUFSIZ)

    log.debug('Request received: {}'.format(data))

    request = parse_http_request(data)
    file_data = get_file(request.request_uri)

    if file_data.exist and request.is_range_requested():
        response = HttpResponse(
            protocol=request.protocol,
            status=206,
            basic_range=request.get_range()
        )

        response.file_data = file_data

    elif file_data.exist:
        response = HttpResponse(protocol=request.protocol, status=200)

    else:
        response = HttpResponse(protocol=request.protocol, status=404)
        response.header['Content-Type'] = 'text/plain'
        response.content = 'This file does not exist!'

    log.info('GET {uri} {protoc} {basic_range} {status}'.format(
        uri=request.request_uri,
        protoc=request.protocol,
        basic_range=request.basic_range,
        status=request.status
    ))

    response.write_to(client_sock)
    client_sock.close()


def run_server(host, port):
    addr = (host, port)

    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind(addr)
    server_sock.listen(SOCKET_BACKLOG_SIZE)

    log.info('httpy started on {}:{}'.format(host, port))

    pool = ThreadPool(THREAD_POOL_SIZE)

    while True:
        log.debug('Waiting for connection..')

        client_sock, addr = server_sock.accept()

        log.debug('Connected from: {}'.format(addr))

        pool.add_task(handle_request, client_sock)
