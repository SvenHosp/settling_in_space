import threading
import time

class Game():
    heartbeat_sec = 1

    def game_initialize(self):
        # code for game initialization
        print('initialize game')
        pass

    def game_logic(self):
        # code to execute game logic
        print('game logic')
        pass

    def heartbeat(self):
        while True:
            self.game_logic()
            time.sleep(self.heartbeat_sec)

    def start(self):
        self.game_initialize()
        heartbeat_t = threading.Thread(name='heartbeat_t', target=self.heartbeat)
        heartbeat_t.start()