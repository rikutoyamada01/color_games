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

def test():
    pg.init()
    screen = pg.display.set_mode((con.SCREEN_WIDTH,con.SCREEN_HEIGHT))
    pg.display.set_caption("Color Game")
    cooldown = 0
    clock=pg.time.Clock()

    led_button = LEDButton(screen,con.SCREEN_WIDTH/2,150)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                pg.quit()
                exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if cooldown <= 0:
                    if led_button.button_center.collidepoint(pg.mouse.get_pos()):
                        led_button.light_up(con.GREEN)
                        cooldown = 50

        if cooldown < 0:
            led_button.light_down()

        screen.fill(con.WHITE)
        cooldown -= 1
        led_button.update(cooldown)
        led_button.draw()
        
        pg.display.update()
        clock.tick(60)

if __name__ == "__main__":
    test()
