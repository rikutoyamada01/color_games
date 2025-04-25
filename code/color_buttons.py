import constants as con
import pygame as pg
from resizable import Resizable

pg.mixer.init()

class ColorButton(Resizable):
    def __init__(self, screen, x: int, y: int, color=con.WHITE , light_color=con.WHITE, port_num=0):
        self.screen = screen
        self.pos = (x,y)
        self.color = color
        self.light_color = light_color
        self.port_num = port_num
        self.radius = 125
        self.is_clicked = False
        self.sound = pg.mixer.Sound("Audio/SE/UI/menu_button_click_sound.mp3")

    def draw(self):
        self.button_center = pg.draw.circle(self.screen,self.color,self.pos,self.radius,0)
        self.button_trim = pg.draw.circle(self.screen,con.BLACK,self.pos,self.radius + 10,12)

        if self.is_clicked:
            self.button_light = pg.draw.circle(self.screen, self.light_color, self.pos, self.radius + 24, 20)

    def update_position(self, screen_size):
        return super().update_position(screen_size)


    def click(self):
        self.is_clicked = True
        self.sound.play()

    
    def update(self,cooldown):
        if cooldown <= 5:
            self.is_clicked = False
