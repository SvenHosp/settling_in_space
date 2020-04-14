import threading
import time

class SettlingMain():
    def __init__(self):
        pass
    
    def start(self, servermode=False):
        self.game_engine = GameEngine()
        
    def start_gameengine(self):
        self.game_engine.start()

class GameEngine():
    def __init__(self):
        # TODO: read it from a config yaml
        self.heartbeat_sec = 1
    
    def start(self):
        self.startHeartBeat()
    
    def startHeartBeat(self):
        heartbeat_t = threading.Thread(name='heartbeat_t', target=GameEngine.heartbeat, args=(self,))
        heartbeat_t.start()
    
    @staticmethod
    def heartbeat(game_engine):
        while True:
            time.sleep(game_engine.heartbeat_sec)
            game_engine.beat()
    
    def beat(self):
        print('play')
        pass