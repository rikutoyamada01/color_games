import pygame as pg
import constants as con
import re

class PlayerName():
    def __init__(self,screen: pg.surface.Surface, offset=(0,-200), color=con.WHITE) -> None:
        self.player_name = "Naam"
        self.font = pg.font.Font(None, 100)
        self.screen = screen
        self.size = (400, 110)
        self.offset = offset
        self.surface = pg.Surface(self.size , pg.SRCALPHA)
        self.rect = self.surface.get_rect()
        self.color = color
        self.sound = pg.mixer.Sound("Audio/SE/UI/keyboard_typing_sound.mp3.mp3")

    def update_position(self, screen_size) -> None:
        w, h = screen_size
        self.rect.center = (w // 4 + self.offset[0], h // 2 + self.offset[1])
        
    def draw(self) -> None:
        self.surface.fill((0, 0, 0, 0))

        text_surf = self.font.render(self.player_name, True, con.BLACK)
        text_rect = text_surf.get_rect(center=self.surface.get_rect().center)
        self.surface.blit(text_surf, text_rect)
        pg.draw.line(self.surface, con.BLACK, (text_rect.left, text_rect.bottom), (text_rect.right, text_rect.bottom), 2)
        self.screen.blit(self.surface, self.rect)

    def handle_input(self, event) -> None:
        self.sound.play()
        if event.key == pg.K_BACKSPACE:
            if self.player_name == "Naam":
                pass
            else:
                self.player_name = self.player_name[:-1]

                if self.player_name == "":
                    self.player_name = "Naam"
        
        if re.fullmatch(r"\w", event.unicode):
            if self.player_name == "Naam":
                self.player_name = ""
            self.player_name += event.unicode

        if event.unicode == " ":
            if self.player_name == ("Naam"):
                self.player_name = ""
            else:
                self.player_name += event.unicode

    def get(self) -> str:
        if self.player_name == "":
            self.player_name = "Naam"
        
        return self.player_name

def test():
    # Pygameの初期化
    pg.init()

    # ウィンドウのサイズとフォントを設定
    screen = pg.display.set_mode((600, 400))
    pg.display.set_caption("player_name_manager_test")
    player_name_manager = PlayerName(screen, offset=(0, 0), color=con.WHITE)
    player_name_manager.update_position((600, 400))
    clock = pg.time.Clock()
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                player_name_manager.handle_input(event)

        # 背景を白に設定
        screen.fill((255, 255, 255))

        # PlayerNameManagerを描画
        player_name_manager.draw()

        # 画面を更新
        pg.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    test()
