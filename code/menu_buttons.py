import constants as con
import pygame as pg

pg.mixer.init()

class MenuButton():
    def __init__(self, screen: pg.surface.Surface, text: str, size: tuple[int]=(200,100) ,offset: tuple[int]=(0,0) ,color=con.WHITE, hover_color=(150, 255, 150), text_color=con.BLACK) -> None:
        self.screen = screen
        self.size = size
        self.border_radius = size[1] // 2
        self.surface = pg.Surface(size , pg.SRCALPHA)  # 透明度を持つサーフェスを作成
        self.rect = self.surface.get_rect()
        self.offset = offset
        self.color = color
        self.hover_color = hover_color
        self.text = text
        self.text_color = text_color
        self.font = pg.font.Font(None, 36)
        self.sound = pg.mixer.Sound("Audio/SE/UI/menu_button_click_sound.mp3")

    def draw(self):
        self.surface.fill((0, 0, 0, 0))  # 透明クリア

        # 背景（角丸四角）
        color = self.hover_color if self.rect.collidepoint(pg.mouse.get_pos()) else self.color
        pg.draw.rect(self.surface, self.color, (0, 0, *self.size), border_radius=self.border_radius)

        # 左にアイコン（円）
        pg.draw.circle(self.surface, con.BLACK, (self.border_radius, self.size[1] // 2), self.border_radius)
        pg.draw.circle(self.surface, color, (self.border_radius, self.size[1] // 2), self.border_radius - 10)

        # 中央にテキスト
        text_surf = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=(self.size[0] // 2 + 50, self.size[1] // 2))
        self.surface.blit(text_surf, text_rect)

        self.screen.blit(self.surface, self.rect)

    def update_position(self, screen_size) -> None:
        w, h = screen_size
        self.rect.center = (w // 4 + self.offset[0], h // 2 + self.offset[1])

    def click(self) -> None:
        self.sound.play()
