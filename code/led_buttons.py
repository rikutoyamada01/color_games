import constants as con
import pygame as pg
try:
    import RPi.GPIO as GPIO
    from rpi_ws281x import PixelStrip, Color
except ImportError:
    from mock_gpio import MockGPIO as GPIO
    from mock_ws281x import PixelStrip, Color


class LEDButton(pg.sprite.Sprite):
    def __init__(self, screen, x: int, y: int):
        super().__init__()
        self.screen = screen
        self.pos = (x,y)
        self.color = con.BLACK
        self.radius = 125
        
        self.num_leds =16
        self.pin = con.PORT_LIGHT
        self.strip = PixelStrip(self.num_leds, self.pin)
        self.strip.begin()
        self.is_lighting = False
        self.sound = pg.mixer.Sound("Audio/SE/UI/menu_button_click_sound.mp3")

    def draw(self):
        self.button_center = pg.draw.circle(self.screen,self.color,self.pos,self.radius,0)
        self.button_trim = pg.draw.circle(self.screen,con.BLACK,self.pos,self.radius + 10,12)

    def _set_color_on_all(self, color):
        for i in range(self.num_leds):
            self.strip.setPixelColor(i, Color(color[0], color[1], color[2]))

    def light_up(self, color):
        self.color = color
        self._set_color_on_all(color)
        self.strip.show()

    def light_up_for_rank(self, rank):
        if rank == 1:
            self._set_color_on_all(con.GOLD)
        elif rank == 2:
            self._set_color_on_all(con.SILVER)
        else:
            for i in range(rank):
                self.strip.setPixelColor(i, Color(con.BRONZE[0], con.BRONZE[1], con.BRONZE[2]))
            for i in range(rank, self.num_leds):
                self.strip.setPixelColor(i, Color(0, 0, 0))
        self.strip.show()

    def light_down(self):
        if self.color == con.BLACK:
            return
        self.color = con.BLACK
        self._set_color_on_all(self.color)
        self.strip.show()
