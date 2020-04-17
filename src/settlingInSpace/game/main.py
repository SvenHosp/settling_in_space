"""
game main module
"""
import threading
import time
from pathlib import Path
import yaml
from settlingInSpace.model.gamemodel import GameModel

class SettlingMain():
    """Main class to start the game"""
    def __init__(self, servermode=False):
        """
        init method
        
        param servermode(boolean): switch to start a rpc server
        """
        self.game_engine = GameEngine()
    
    def configure(self):
        """
        configure game
        """
        self.game_engine.configure()
    
    def initialize(self):
        """
        initialize
        """
        self.game_engine.initialize()
    
    def start(self):
        """
        call to start game
        """
        self.game_engine.start()
        

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
        list_starnames = GameEngine.parse_names_yaml()
        self.gamemodel.initialize(
            list_starnames=list_starnames
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
        #print('play')
        pass
    
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
            list_starnames = dict_from_yaml['stars']
        return list_starnames
        