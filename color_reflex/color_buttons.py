import constants as con
import pygame as pg
#from random import randint

pg.mixer.init()

class ColorButton(pg.sprite.Sprite):
    def __init__(self, screen, x: int, y: int, color=con.WHITE , light_color=con.WHITE, port_num=0):
        super().__init__()
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


    def click(self):
        self.is_clicked = True
        self.sound.play()

    
    def update(self,cooldown):
        if cooldown <= 0:
            self.is_clicked = False

def test():
    pg.init()
    screen = pg.display.set_mode((con.SCREEN_WIDTH,con.SCREEN_HEIGHT))
    pg.display.set_caption("Color Game")
    cooldown = 0
    clock=pg.time.Clock()

    red_button = ColorButton(screen,(con.SCREEN_WIDTH/2,150),con.RED, con.LIGHT_RED)
    blue_button = ColorButton(screen,(con.SCREEN_WIDTH/2,con.SCREEN_HEIGHT-150),con.BLUE, con.LIGHT_BLUE)
    yellow_button = ColorButton(screen,(150, con.SCREEN_HEIGHT/2),con.YELLOW, con.LIGHT_YELLOW)
    green_button = ColorButton(screen,(con.SCREEN_WIDTH-150, con.SCREEN_HEIGHT/2),con.GREEN, con.LIGHT_GREEN)
    color_buttons = [red_button, blue_button, yellow_button, green_button]

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                pg.quit()
                exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if cooldown <= 0:
                    for color_button in color_buttons:
                        if color_button.button_center.collidepoint(pg.mouse.get_pos()):
                            color_button.click()
                            cooldown = 50

        screen.fill(con.WHITE)
        cooldown -= 1
        for color_button in color_buttons:
            color_button.update(cooldown)
            color_button.draw()
        
        pg.display.update()
        clock.tick(60)

if __name__ == "__main__":
    test()