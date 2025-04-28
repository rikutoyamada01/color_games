from resizable import Resizable
import pygame as pg
import constants as con

class RoundCounter(Resizable):
    def __init__(self, screen: pg.Surface, size: tuple[int, int]):
        super().__init__()
        self.screen = screen
        self.size = size
        self.current_round = 0
        self.surf = pg.Surface(size, pg.SRCALPHA)
        self.rect = self.surf.get_rect()
        self.font = pg.font.Font(None, size[1])

    def update_position(self, screen_size: tuple[int, int]):
        self.rect.center = (screen_size[0]//2, screen_size[1]//2)

    def update(self, current_round: int):
        self.current_round = current_round

    def draw(self):
        self.surf.fill((0,0,0,0))
        text_surf = self.font.render(str(self.current_round), True, con.BLACK)
        text_rect = text_surf.get_rect(center=(self.size[0]//2, self.size[1]//2))
        self.surf.blit(text_surf,text_rect)
        self.screen.blit(self.surf, self.rect)


class GameTypeSurf(Resizable):
    def __init__(self, screen: pg.Surface, size: tuple[int, int]):
        super().__init__()
        self.screen = screen
        self.gametype = None
        self.size = size
        self.surf = pg.Surface(size, pg.SRCALPHA)
        self.rect = self.surf.get_rect()
        self.font = pg.font.Font(None, size[1])

    def update_position(self, screen_size):
        self.rect.center = (screen_size[0]//2, self.size[1]//2)


    def set_game_type(self, gametype: str):
        self.gametype = gametype
        self.text = self.gametype.upper()

    def draw(self):
        self.surf.fill((0,0,0,0))
        text_surf = self.font.render(self.text, True, con.BLACK)
        text_rect = text_surf.get_rect(center=(self.size[0]//2, self.size[1]//2))
        self.surf.blit(text_surf, text_rect)
        self.screen.blit(self.surf, self.rect)



def round_counter_test():
    pg.init()
    screen_size = (640, 480)
    screen = pg.display.set_mode(screen_size)
    clock = pg.time.Clock()

    round_counter = RoundCounter(screen, size=(400, 400))
    round_counter.update_position(screen_size)

    running = True
    current_round = 0

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    current_round += 1
                    round_counter.update(current_round)

        screen.fill((220, 220, 220))  # 背景灰色
        round_counter.draw()

        pg.display.flip()
        clock.tick(60)

    pg.quit()




def game_type_surf_test():
    pg.init()
    screen_size = (640, 480)
    screen = pg.display.set_mode(screen_size, pg.RESIZABLE)
    clock = pg.time.Clock()

    game_type_surf = GameTypeSurf(screen, size=(400, 100))
    game_type_surf.set_game_type("memory")
    game_type_surf.update_position(screen_size)

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.type == pg.K_SPACE:
                    game_type_surf.set_game_type("reflex")
            elif event.type == pg.VIDEORESIZE:
                screen_size = event.w, event.h
                screen = pg.display.set_mode(screen_size, pg.RESIZABLE)
                game_type_surf.update_position(screen_size)


        screen.fill((200, 200, 200))
        game_type_surf.draw()

        pg.display.flip()
        clock.tick(60)

    pg.quit()

if __name__ == "__main__":
    round_counter_test()
    game_type_surf_test()
