import constants as con
import pygame as pg
from resizable import Resizable


class ControllButton(Resizable):
    def __init__(self, screen: pg.surface.Surface, text: str, size: tuple[int]=(100,40) ,offset: tuple[int]=(-25,25) ,color=con.MENU_GREEN, hover_color=con.LIGHT_GREEN, text_color=con.BLACK) -> None:
        self.screen = screen
        self.size = size
        self.border_radius = size[1] // 2
        self.surface = pg.Surface(size)
        self.rect = self.surface.get_rect()
        self.offset = offset
        self.color = color
        self.hover_color = hover_color
        self.text = text
        self.text_color = text_color
        self.font = pg.font.Font(None, 24)
        self.sound = pg.mixer.Sound("Audio/SE/UI/menu_button_click_sound.mp3")

    def draw(self):
        self.surface.fill(con.BLACK)
        color = self.hover_color if self.rect.collidepoint(pg.mouse.get_pos()) else self.color
        pg.draw.rect(self.surface, color, (2, 2, self.size[0] - 4, self.size[1] - 4))

        # 中央にテキスト
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=(self.size[0] // 2, self.size[1] // 2))
        self.surface.blit(text_surf, text_rect)

        self.screen.blit(self.surface, self.rect)

    def update_position(self, screen_size) -> None:
        w, h = screen_size
        self.rect.topright = (w + self.offset[0], 0 + self.offset[1])

    def click(self) -> None:
        self.sound.play()
