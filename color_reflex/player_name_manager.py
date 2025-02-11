import pygame as pg
import constants as con
import re

class PlayerName():
    def __init__(self,screen: pg.surface.Surface, x: int, y: int, color=con.WHITE) -> None:
        self.player_name = "No Name"
        self.font = pg.font.Font(None, 48)
        self.screen = screen
        self.width = 100
        self.rect = pg.Rect(x-self.width/2, y, self.width, 50)
        self.color = color
        self.sound = pg.mixer.Sound("Audio/SE/UI/keyboard_typing_sound.mp3.mp3")
        
    def draw(self) -> None:
        pg.draw.rect(self.screen, self.color, self.rect)
        text_surf = self.font.render(self.player_name, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=self.rect.center)
        self.screen.blit(text_surf, text_rect)

        
        pg.draw.line(self.screen, con.BLACK,(text_rect.x, text_rect.y+35),(text_rect.right , text_rect.y+35))

    def handle_input(self, event) -> None:
        self.sound.play()
        if event.key == pg.K_BACKSPACE:
            if self.player_name == "No Name":
                pass
            else:
                self.player_name = self.player_name[:-1]

                if self.player_name == "":
                    self.player_name = "No Name"
        
        if re.fullmatch(r"\w", event.unicode):
            if self.player_name == "No Name":
                self.player_name = ""
            self.player_name += event.unicode

        if event.unicode == " ":
            if self.player_name == ("No Name"):
                self.player_name = ""
            else:
                self.player_name += event.unicode

    def get(self) -> str:
        if self.player_name == "":
            self.player_name = "No Name"
        
        return self.player_name

def test():
    # Pygameの初期化
    pg.init()

    # ウィンドウのサイズとフォントを設定
    screen = pg.display.set_mode((600, 400))
    pg.display.set_caption("player_name_manager_test")
    player_name = PlayerName(screen, 300, 200)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            if event.type == pg.KEYDOWN:
                player_name.handle_input(event)
                
        screen.fill(con.WHITE)
        player_name.draw()
        pg.display.update()
        pg.display.flip()

if __name__ == "__main__":
    test()