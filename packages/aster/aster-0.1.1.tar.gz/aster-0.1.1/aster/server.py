from os import getcwd
from os.path import join
import sys
from twisted.web.server import Site
from twisted.web.static import File
from twisted.web.resource import Resource
from twisted.internet import reactor
from twisted.python import log
from aster.dispatcher import dispatch


class APIServer(Resource):
    def do_request(self, request):
        method = request.method
        api_name = request.path.replace('/api/', '', 1)
        request = {
            'headers': request.requestHeaders,
            'body':    request.content.getvalue,
            'params': request.args
        }

        return dispatch(method, api_name, request)

    def render_GET(self, request):
        return self.do_request(request)

    def render_POST(self, request):
        return self.do_request(request)

    def getChild(self, name, request):
        return APIServer()

def main():
    sys.path.insert(0, join(getcwd(), 'api'))

    port = 9000
    log.startLogging(sys.stdout)

    root = File('public')
    root.putChild('api', APIServer())
    reactor.listenTCP(port, Site(root))
    reactor.run()
