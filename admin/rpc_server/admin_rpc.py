from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import psutil
from subprocess import Popen

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


class RPCServer():
    def __init__(self):
        '''init'''

    def start(self):
        '''starts the server'''
        Popen(['pip', 'install', '-e', '/app/src'])
        # Create server
        with SimpleXMLRPCServer(('0.0.0.0', 8088),
                                requestHandler=RequestHandler) as server:
            server.register_introspection_functions()

            server.register_instance(RPCServer.restart_gameserver)

            # Run the server's main loop
            server.serve_forever()
    
    def restart_gameserver():
        for process in psutil.process_iter():
            if process.cmdline() == ['python', '/app/src/settlingInSpace/game/main.py']:
                print('terminating rpc game server')
                process.terminate()
                break
            else:
                print('starting rpc game server')
                Popen(['python', '/app/src/settlingInSpace/game/main.py'])


if __name__ == '__main__':
    main = RPCServer()
    main.start()