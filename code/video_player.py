import pygame as pg
import cv2
import numpy as np
from resizable import Resizable

class VideoPlayer(Resizable):
    def __init__(self, screen: pg.Surface, memory_path, reflex_path, size: tuple[int, int]):
        self.screen = screen
        self.memory_cap = cv2.VideoCapture(memory_path)
        self.reflex_cap = cv2.VideoCapture(reflex_path)
        if not self.memory_cap.isOpened():
            print("failed to open memory video")
        if not self.reflex_cap.isOpened():
            print("failed to open reflex video")
        self.size = size
        self.surf = pg.Surface(size, pg.SRCALPHA)
        self.rect = self.surf.get_rect()
        self.current_state = "stop"
        self.frame_counter = 0

    def update(self):
        if self.current_state == "stop":
            self.surf = pg.Surface(self.size, pg.SRCALPHA)
            return
        
        self.frame_counter += 1
        if self.frame_counter % 2 != 0:
            return
        
        if self.current_state == "memory":
            ret, frame = self.memory_cap.read()
        else:
            ret, frame = self.reflex_cap.read()
        if not ret:
            self.stop()
            return

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, self.size)

        frame = pg.surfarray.make_surface(frame.swapaxes(0, 1))
        self.surf.blit(frame, (0, 0))


    def update_position(self, screen_size):
        w, h = screen_size
        self.rect.center = (w * 3 // 4, h * 3 // 5)

    def draw(self):
        self.screen.blit(self.surf, self.rect)

    def play_memory_tutorial(self):
        self.current_state = "memory"
        self.memory_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    def play_reflex_tutorial(self):
        self.current_state = "reflex"
        self.reflex_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    def stop(self):
        self.current_state = "stop"
        self.surf = pg.Surface(self.size, pg.SRCALPHA)
        self.reflex_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        self.memory_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    def get_state(self) -> str:
        return self.current_state

    



import pygame as pg

def test_video_switch():
    pg.init()
    screen = pg.display.set_mode((800, 600))
    clock = pg.time.Clock()

    memory_path = "video/memory_game_tutorial.mp4"
    reflex_path = "video/reflex_game_tutorial.mp4"

    player = VideoPlayer(screen, memory_path, reflex_path, size=(400, 400))
    player.update_position((800, 600))

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    if player.current_state == "stop":
                        player.play_memory_tutorial()
                    elif player.current_state == "memory":
                        player.play_reflex_tutorial()
                    else:
                        player.stop()

        player.update()

        screen.fill((30, 30, 30))
        player.draw()

        pg.display.flip()
        clock.tick(60)

    pg.quit()


if __name__ == "__main__":
    test_video_switch()
