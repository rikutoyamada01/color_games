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
        self.color = con.WHITE
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
        
        for i in range(self.num_leds):
            self.strip.setPixelColor(i, Color(self.color[0], self.color[1], self.color[2])) 
        self.strip.show()

    def light_up(self, color):
        self.color = color


    def light_down(self):
        self.color = con.WHITE
