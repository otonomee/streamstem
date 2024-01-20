import asyncio

import websockets.handshake

from awsgi.websocket import WebSocketProtocol


async def application(environ, start_response):
    response_headers = []

    def get_request_header(key):
        return environ.get('HTTP_' + key.upper().replace('-', '_'), '')

    def set_response_header(key, value):
        response_headers.append((key, value))

    if get_request_header('Upgrade').lower() == 'websocket':

        websocket_key = websockets.handshake.check_request(get_request_header)
        websockets.handshake.build_response(set_response_header, websocket_key)

        start_response('101 Switching Protocols', response_headers)

        class EchoProtocol(WebSocketProtocol):

            async def message_received(self, message):
                await self.send(message)

        environ['wsgi.input'].set_websocket_protocol(EchoProtocol)

        return []

    response_headers.append(('Content-type', 'text/plain'))
    start_response('200 OK', response_headers)

    return [b'Hello async!\n']