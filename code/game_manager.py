import pygame as pg
import constants as con
from color_buttons import ColorButton
from led_buttons import LEDButton
from menu_buttons import MenuButton
from player_name_manager import PlayerName
from result_manager import Result
import random
try:
    import RPi.GPIO as GPIO
except ImportError:
    from mock_gpio import MockGPIO as GPIO

class GameManager():
    def __init__(self) -> None:
        # init game
        pg.init()
        self.screen = pg.display.set_mode((con.SCREEN_WIDTH,con.SCREEN_HEIGHT))
        pg.display.set_caption("Color Game")
        self.clock = pg.time.Clock()
        self.round_font = pg.font.Font(None, 50)
        self.game_states = ["START", "WAITING", "INPUT", "GAME_OVER"]
        self.active_game_states = ["WAITING", "INPUT"]
        self.current_state = "START"
        self.game_type = None

        #music input
        self.start_music = pg.mixer.Sound("Audio/Music/menu_music.mp3")
        self.start_music.set_volume(0.3)
        self.waiting_music = pg.mixer.Sound("Audio/Music/waiting_music.mp3")
        self.waiting_music.set_volume(0.3)
        self.input_music =  pg.mixer.Sound("Audio/Music/input_music.mp3")
        self.input_music.set_volume(0.3)
        self.game_over_music = pg.mixer.Sound("Audio/Music/game-over-arcade-6435.mp3")
        pg.mixer.set_num_channels(8)
        self.start_channel = pg.mixer.Channel(0)
        self.waiting_channel = pg.mixer.Channel(1)
        self.input_channel = pg.mixer.Channel(2)
        self.game_over_channel = pg.mixer.Channel(3)


        #init buttons
        self.memory_start_button = MenuButton(self.screen,con.SCREEN_WIDTH/2,400,"memory",con.LIGHT_GREEN)
        self.reflex_start_button = MenuButton(self.screen,con.SCREEN_WIDTH/2,500,"reflex",con.LIGHT_GREEN)
        self.exit_button = MenuButton(self.screen,con.SCREEN_WIDTH/2, 600, "exit",con.LIGHT_GREEN)

        self.player_name = PlayerName(self.screen, con.SCREEN_WIDTH/2, con.SCREEN_HEIGHT/2-100)

        self.red_button = ColorButton(self.screen, con.SCREEN_WIDTH/2, 150, con.RED, con.LIGHT_RED, con.PORT_RED)
        self.blue_button = ColorButton(self.screen, con.SCREEN_WIDTH/2, con.SCREEN_HEIGHT-150, con.BLUE, con.LIGHT_BLUE, con.PORT_BLUE)
        self.yellow_button = ColorButton(self.screen, 150, con.SCREEN_HEIGHT/2, con.YELLOW, con.LIGHT_YELLOW, con.PORT_YELLOW)
        self.green_button = ColorButton(self.screen, con.SCREEN_WIDTH-150, con.SCREEN_HEIGHT/2, con.GREEN, con.LIGHT_GREEN ,con.PORT_GREEN)
        self.color_buttons = [self.red_button, self.blue_button, self.yellow_button, self.green_button]
        
        self.gpio = GPIO
        self.gpio.setmode(self.gpio.BCM)
        self.gpio.setup(con.PORT_GREEN, self.gpio.IN, pull_up_down=self.gpio.PUD_UP)
        self.gpio.setup(con.PORT_RED, self.gpio.IN, pull_up_down=self.gpio.PUD_UP)
        self.gpio.setup(con.PORT_YELLOW, self.gpio.IN, pull_up_down=self.gpio.PUD_UP)
        self.gpio.setup(con.PORT_BLUE, self.gpio.IN, pull_up_down=self.gpio.PUD_UP)
        
        self.led_button = LEDButton(self.screen, con.SCREEN_WIDTH/2, con.SCREEN_HEIGHT/2)

        #init round
        self.rounds = [random.choice(self.color_buttons)]
        self.current_round_number = 0
        self.input_round_number = 0
        self.cooldown = 50


    def update(self) -> None:
        #button update
        for color_button in self.color_buttons:
            color_button.update(self.cooldown)
        
        if self.game_type == "memory" and self.current_state in self.active_game_states:
            if self.cooldown <= 0:
                self.led_button.light_down()

        if self.current_state in ("START", "GAME_OVER"):
            self.cooldown -= 1

        #light up control
        if self.current_state == "WAITING":
            self.cooldown -= 1
            
            cooldown_threshold = -20 if self.game_type == "memory" else -5
    
            if self.cooldown < cooldown_threshold:
                if self.current_round_number >= len(self.rounds):
                    self.current_state = "INPUT"
                    self.current_round_number = 0
                    if self.game_type == "memory":
                        self.led_button.light_down()
                else:
                    target_round = self.current_round_number if self.game_type == "memory" else len(self.rounds) - 1
                    self.led_button.light_up(self.rounds[target_round].color)
                    
                    if self.game_type == "memory":
                        self.rounds[self.current_round_number].click()
                        self.cooldown = 50
                    
                    self.current_round_number += 1

        #check rounds and change to waiting phase
        if self.current_state == "INPUT":
            self.cooldown -= 1
            
            if self.cooldown <= 0:
                if self.input_round_number >= len(self.rounds):
                    self.current_state = "WAITING"
                    self.led_button.light_down()
                    self.rounds.append(random.choice(self.color_buttons)) #random
                    
                    if self.game_type == "memory":
                        self.input_round_number = 0
                        self.cooldown = 40
                    else:
                        self.cooldown = 80
                    
        if self.game_type == "reflex" and len(self.rounds) > 10:
            self._reset(self.game_type)

        self._update_music()
        


    def handle_event(self) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self._quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.current_state in ("START", "GAME_OVER"):
                    if self.memory_start_button.rect.collidepoint((pg.mouse.get_pos())):
                        self.current_state = "WAITING"
                        self.memory_start_button.click()
                        self.game_type = "memory"
                        self.led_button.light_down()
                        self.cooldown = 50
                    if self.reflex_start_button.rect.collidepoint((pg.mouse.get_pos())):
                        self.current_state = "WAITING"
                        self.memory_start_button.click()
                        self.game_type = "reflex"
                        self.led_button.light_down()
                        self.start_time = pg.time.get_ticks()
                        self.cooldown = 50
                    if self.exit_button.rect.collidepoint((pg.mouse.get_pos())):
                        self.exit_button.click()
                        self._quit()

                #input about color button
                if self.cooldown < 0 and self.current_state == "INPUT":
                    for color_button in self.color_buttons:
                        if (color_button.button_center.collidepoint((pg.mouse.get_pos()))):
                            self._handle_color_button_input(color_button)
                    
            if event.type == pg.KEYDOWN:
                if self.current_state == "START":
                    self.player_name.handle_input(event)

        if self.cooldown < 0 and self.current_state in ("START", "GAME_OVER"):
            if not self.gpio.input(con.PORT_BLUE):
                self.current_state = "WAITING"
                self.game_type = "memory"
                self.led_button.light_down()
                self.cooldown = 50
            if not self.gpio.input(con.PORT_RED):
                self.current_state = "WAITING"
                self.game_type = "reflex"
                self.led_button.light_down()
                self.start_time = pg.time.get_ticks()
                self.cooldown = 50
            
            
        if self.cooldown < 0 and self.current_state == "INPUT":
            for color_button in self.color_buttons:
                if not self.gpio.input(color_button.port_num):
                    self._handle_color_button_input(color_button)
    
    def draw(self) -> None:
        self.screen.fill(con.WHITE)

        if self.current_state == "START":
            self.memory_start_button.draw()
            self.reflex_start_button.draw()
            self.exit_button.draw()
            self.player_name.draw()

        if self.current_state == "GAME_OVER":
            self.memory_start_button.draw()
            self.reflex_start_button.draw()
            self.exit_button.draw()
            self.result.draw(self.game_type)

        if self.current_state in self.active_game_states:
            round_surf = self.round_font.render(f"round {len(self.rounds)}", 0, con.BLACK)
            self.screen.blit(round_surf, (10,10))

            for color_button in self.color_buttons:
                color_button.draw()
                
            self.led_button.draw()

        pg.display.update()
        self.clock.tick(60)


    def _reset(self, game_type: str) -> None:
        self.result = Result(self.screen,con.SCREEN_WIDTH/2,50, game_type)
        self.result.load(game_type)
        if game_type == "memory":
            self.result.save(len(self.rounds), self.player_name.get(), game_type)
        if game_type == "reflex":
            self.end_time = pg.time.get_ticks()
            self.time = self.end_time - self.start_time
            self.result.save(self.time/1000, self.player_name.get(), game_type)

        self.rank = self.result.get_rank(self.game_type)
        self.led_button.light_down()
        self.led_button.light_up_for_rank(self.rank)
        self.led_button.draw()
        self.current_state = "GAME_OVER"
        self.rounds = []
        self.current_round_number = 0
        self.input_round_number = 0
        self.cooldown = 50

    def _update_music(self):
        if self.current_state == "START":
            if self.start_channel.get_busy() == False:
                pg.mixer.fadeout(3)
                self.start_channel.play(self.start_music)
        if self.current_state == "WAITING":
            if self.waiting_channel.get_busy() == False:
                pg.mixer.fadeout(3)
                self.waiting_channel.play(self.waiting_music)
        if self.current_state == "INPUT" and len(self.rounds) >= 10:
            if self.input_channel.get_busy() == False:
                pg.mixer.fadeout(3)
                self.input_channel.play(self.input_music)
        if self.current_state == "GAME_OVER":
            if self.game_over_channel.get_busy() == False:
                pg.mixer.fadeout(3)
                self.game_over_channel.play(self.game_over_music)
                self.game_over_channel.fadeout(10000)
                
    def _handle_color_button_input(self, color_button: ColorButton) -> None:
        if color_button == self.rounds[self.input_round_number]:
            color_button.click()
            self.cooldown = 20
            self.input_round_number += 1
            if self.game_type == "memory":
                self.led_button.light_up(color_button.color)
        else:
            if self.game_type == "memory":
                self._reset(self.game_type)





    def _quit(self) -> None:
        self.gpio.cleanup()
        self.led_button.light_down()
        self.led_button.draw()
        pg.quit()
        exit()
