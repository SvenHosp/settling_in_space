"""
game main module
"""
import threading
import time
from settlingInSpace.model.gamemodel import GameModel

class SettlingMain():
    """Main class to start the game"""
    def __init__(self):
        """init method"""
        pass
    
    def start(self, servermode=False):
        """
        call to start game
        
        servermode(boolean): switch to start a rpc server
        """
        self.game_engine = GameEngine()
        self.start_gameengine()
        
    def start_gameengine(self):
        """
        start gameengine
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
    
    def start(self):
        """start game engine"""
        self.gamemodel.initialize()
        
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