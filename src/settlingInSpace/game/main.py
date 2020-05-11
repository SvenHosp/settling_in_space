"""
game main module
"""
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import threading
import time
from pathlib import Path
import yaml
from settlingInSpace.model.gamemodel import GameModel

class SettlingMain():
    """Main class to start the game"""
    def __init__(self):
        """
        init method
        
        param servermode(boolean): switch to start a rpc server
        """
        self.game_engine = GameEngine()
        self.interface = GameEngine_Interface(gameEngine=self.game_engine)
    
    def start_rpc_server(self):
        self.api_server = RPCServer(self.interface)
        self.api_server.start()
        

class GameEngine_Interface():
    """Interface class for GameEngine"""
    
    def __init__(self, gameEngine=None):
        """
        init method
        """
        self.game_engine = gameEngine
    
    def configure(self):
        """
        configure game
        """
        self.game_engine.configure()
        return True
    
    def initialize(self):
        """
        initialize
        """
        self.game_engine.initialize()
        return True
    
    def start(self):
        """
        call to start game
        """
        self.game_engine.start()
        return True
        
        

class GameEngine():
    """
    class to control game technically
    
    starts thread etc.
    """
    def __init__(self):
        """
        init method
        
        init technical parameters
        """
        # TODO: read it from a config yaml
        self.heartbeat_sec = 1
        self.gamemodel = GameModel()
        
    def configure(self):
        """
        configure game engine
        """
        self.gamemodel.configure()
    
    def initialize(self):
        """
        initialize game engine
        """
        main_config = GameEngine.parse_main_conf_yaml()
        list_starnames, list_starsystemnames = GameEngine.parse_names_yaml()
        
        self.heartbeat_sec = main_config['technical']['heartbeatSec']
        
        self.gamemodel.initialize(
            main_config=main_config,
            list_starnames=list_starnames,
            list_starsystemnames=list_starsystemnames
        )
    
    def start(self):
        """start game engine"""
        self.startHeartBeat()
    
    def startHeartBeat(self):
        """creates heartbeat thread"""
        heartbeat_t = threading.Thread(name='heartbeat_t', target=GameEngine.heartbeat, args=(self,))
        heartbeat_t.start()
    
    @staticmethod
    def heartbeat(game_engine):
        """Heartbeat thread method"""
        while True:
            time.sleep(game_engine.heartbeat_sec)
            game_engine.beat()
    
    def beat(self):
        """method to run code every beat"""
        for system in self.gamemodel.dict_starsystems.values():
            system.move_natural_objects_through_system()
        pass
    
    @staticmethod
    def parse_main_conf_yaml(yaml_fqn=None):
        """parses main.yaml
        
        param: yaml_fqn(String): path to yaml
        """
        dict_from_yaml = {}
        if yaml_fqn is None:
            yaml_fqn = Path(Path(Path(__file__).parent).resolve()) / 'main.yaml'
        with open(str(yaml_fqn), 'r') as ymlfile:
            dict_from_yaml = yaml.safe_load(ymlfile)
        return dict_from_yaml
    
    @staticmethod
    def parse_names_yaml(yaml_fqn=None):
        """parses names.yaml
        
        param: yaml_fqn(String): path to yaml
        """
        list_starnames = []
        if yaml_fqn is None:
            yaml_fqn = Path(Path(Path(__file__).parent).resolve()) / 'names.yaml'
        with open(str(yaml_fqn), 'r') as ymlfile:
            dict_from_yaml = yaml.safe_load(ymlfile)
            # names taken from:
            # https://en.wikipedia.org/wiki/List_of_proper_names_of_stars
            list_starnames = dict_from_yaml['stars']
            # names taken from:
            # https://minorplanetcenter.net/iau/lists/MPNames.html
            list_starsystemnames = dict_from_yaml['starsystemobject']
        return list_starnames, list_starsystemnames

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


class RPCServer():
    def __init__(self, gameEngineInterface):
        '''init'''
        self.gameEngineInterface = gameEngineInterface

    def start(self):
        '''starts the server'''
        # Create server
        with SimpleXMLRPCServer(('0.0.0.0', 8082),
                                requestHandler=RequestHandler) as server:
            server.register_introspection_functions()

            server.register_instance(self.gameEngineInterface)

            # Run the server's main loop
            server.serve_forever()


if __name__ == '__main__':
    main = SettlingMain()
    main.start_rpc_server()