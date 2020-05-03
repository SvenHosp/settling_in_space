from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import logging
from subprocess import Popen
import psutil

class RPC_functions():
    def start_webpageserver():
        for process in psutil.process_iter():
            if process.cmdline() == ['python', '/app/src/app.py']:
                logging.info('terminating webpage server')
                process.terminate()
                
        logging.info('starting webpage server')
        Popen(['python', '/app/src/app.py'])
        
        return True
    
    def stop_webpageserver():
        for process in psutil.process_iter():
            if process.cmdline() == ['python', '/app/src/app.py']:
                logging.info('terminating webpage server')
                process.terminate()
                break
        return True

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

            server.register_instance(RPC_functions)

            # Run the server's main loop
            server.serve_forever()


if __name__ == '__main__':
    main = RPCServer()
    main.start()