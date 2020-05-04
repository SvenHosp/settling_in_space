from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import logging
from subprocess import Popen
import psutil
from pathlib import Path
import yaml
import os

scope = os.environ['SCOPE']

yaml_fqn = Path(Path(Path(__file__).parent).resolve()) / 'config.yaml'
with open(str(yaml_fqn), 'r') as ymlfile:
    dict_from_yaml = yaml.safe_load(ymlfile)
    path = dict_from_yaml[scope]['path_fqn']
    servername = dict_from_yaml[scope]['servername']
    port = dict_from_yaml[scope]['port']
    

class RPC_functions():
    def start_server():
        for process in psutil.process_iter():
            if process.cmdline() == ['python', path]:
                logging.info('terminating rpc game server')
                process.terminate()
                
        logging.info('starting rpc server')
        Popen(['python', path])
        
        return True
    
    def stop_server():
        for process in psutil.process_iter():
            if process.cmdline() == ['python', path]:
                logging.info('terminating rpc server')
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
        if scope == 'gameserver':
            Popen(['pip', 'install', '-e', '/app/src'])
        # Create server
        with SimpleXMLRPCServer(('0.0.0.0', port),
                                requestHandler=RequestHandler) as server:
            server.register_introspection_functions()

            server.register_instance(RPC_functions)

            # Run the server's main loop
            server.serve_forever()


if __name__ == '__main__':
    main = RPCServer()
    main.start()