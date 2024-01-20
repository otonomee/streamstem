def application(environ, start_response):
    response_headers = [('Content-type', 'text/plain')]
    start_response('200 OK', response_headers)
    return [b'Hello world!\n']
