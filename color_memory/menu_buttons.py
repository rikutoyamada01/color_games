import constants as con
import pygame as pg

pg.mixer.init()

class MenuButton(pg.sprite.Sprite):
    def __init__(self, screen: pg.surface.Surface, x: int, y: int, text: str='', color=con.WHITE, hover_color=(150, 255, 150), text_color=con.BLACK) -> None:
        self.screen = screen
        self.width = 150
        self.rect = pg.Rect(x-self.width/2, y, self.width, 50)
        self.color = color
        self.hover_color = hover_color
        self.text = text
        self.text_color = text_color
        self.font = pg.font.Font(None, 36)
        self.sound = pg.mixer.Sound("Audio/SE/UI/menu_button_click_sound.mp3")

    def draw(self) -> None:
        mouse_pos = pg.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pg.draw.rect(self.screen, self.hover_color, self.rect)
        else:
            pg.draw.rect(self.screen, self.color, self.rect)

        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        self.screen.blit(text_surf, text_rect)

    def click(self) -> None:
        self.sound.play()