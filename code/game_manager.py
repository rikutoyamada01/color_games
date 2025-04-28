import pygame as pg
import constants as con
from resizable import Resizable
from color_buttons import ColorButton
from led_buttons import LEDButton
from menu_buttons import MenuButton
from controll_buttons import ControllButton
from player_name_manager import PlayerName
from video_player import VideoPlayer
from result_manager import Result, RankingTable
from round_counter import RoundCounter, GameTypeSurf
import random
try:
    print("imported GPIO")
    import RPi.GPIO as GPIO
except ImportError:
    print("error")
    from mock_gpio import MockGPIO as GPIO

class GameManager():
    def __init__(self) -> None:
        # init game
        pg.init()
        self.screen = pg.display.set_mode((0,0), pg.FULLSCREEN)
        pg.display.set_caption("Color Game")
        self.clock = pg.time.Clock()
        self.round_font = pg.font.Font(None, 50)
        self.game_states = [con.START, con.WAITING, con.INPUT, con.GAME_OVER]
        self.active_game_states = [con.WAITING, con.INPUT]
        self.current_state = con.START
        self.game_type = None
        self.screen_size = pg.display.get_window_size()

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


        #init player name
        self.player_name = PlayerName(screen=self.screen, offset=(0, 0), color=con.WHITE)

        #init buttons
        self.reflex_start_button = MenuButton(self.screen, "Reactiespel starten", (600, 150), (0, -100), con.MENU_RED, con.LIGHT_RED)
        self.memory_start_button = MenuButton(self.screen, "Geheugenspel starten", (600, 150), (0, 70), con.MENU_BLUE, con.LIGHT_BLUE)
        self.reflex_video_button = MenuButton(self.screen, "Reactiespel video", (600, 150), (0, 240), con.MENU_GREEN, con.LIGHT_GREEN)
        self.memory_video_button = MenuButton(self.screen, "Geheugenspel video", (600, 150), (0, 410), con.MENU_YELLOW, con.LIGHT_YELLOW)
        self.menu_buttons = [self.reflex_start_button, self.memory_start_button, self.reflex_video_button, self.memory_video_button]

        self.exit_button = ControllButton(self.screen, "Afsluiten", (100, 40), (-10, 10))
        self.stop_button = ControllButton(self.screen, "Stoppen", (100,40), (-10,10))
        self.new_profile_button = ControllButton(self.screen, "Nieuw Profiel", (150, 40), (-120, 10))


        memory_path = "video/memory_game_tutorial.mp4"
        reflex_path = "video/reflex_game_tutorial.mp4"
        self.video_player = VideoPlayer(self.screen, memory_path, reflex_path, size=(800, 800))

        self.round_counter = RoundCounter(self.screen, (400,400))
        self.game_type_surf = GameTypeSurf(self.screen, (600, 150))

        self.result = Result(self.screen)
        self.ranking_table = RankingTable(self.screen, self.screen_size, (600,700))

        self.objects: dict[str,list[Resizable]] = {
            con.START: [self.player_name, self.reflex_start_button, self.memory_start_button, self.reflex_video_button, self.memory_video_button, self.exit_button, self.video_player],
            con.WAITING: [self.stop_button, self.round_counter, self.game_type_surf],
            con.INPUT: [self.stop_button, self.round_counter, self.game_type_surf],
            con.GAME_OVER: [self.reflex_start_button, self.memory_start_button, self.reflex_video_button, self.memory_video_button, self.new_profile_button, self.exit_button, self.result, self.ranking_table, self.video_player],
        }
        for group in self.objects.values():
            for object in group:
                object.update_position(self.screen_size)

        self.red_button = ColorButton(self.screen, self.screen_size[0]/2, self.screen_size[1]/2 - 250, con.RED, con.LIGHT_RED, con.PORT_RED)
        self.blue_button = ColorButton(self.screen, self.screen_size[0]/2, self.screen_size[1]/2 + 250, con.BLUE, con.LIGHT_BLUE, con.PORT_BLUE)
        self.yellow_button = ColorButton(self.screen, self.screen_size[0]/2 - 250, self.screen_size[1]/2, con.YELLOW, con.LIGHT_YELLOW, con.PORT_YELLOW)
        self.green_button = ColorButton(self.screen, self.screen_size[0]/2 + 250, self.screen_size[1]/2, con.GREEN, con.LIGHT_GREEN ,con.PORT_GREEN)
        self.color_buttons = [self.red_button, self.blue_button, self.yellow_button, self.green_button]
        
        self.gpio = GPIO
        self.gpio.setmode(self.gpio.BCM)
        self.gpio.setup(con.PORT_GREEN, self.gpio.IN, pull_up_down=self.gpio.PUD_UP)
        self.gpio.setup(con.PORT_RED, self.gpio.IN, pull_up_down=self.gpio.PUD_UP)
        self.gpio.setup(con.PORT_YELLOW, self.gpio.IN, pull_up_down=self.gpio.PUD_UP)
        self.gpio.setup(con.PORT_BLUE, self.gpio.IN, pull_up_down=self.gpio.PUD_UP)
        
        self.led_button = LEDButton(self.screen, pg.display.get_window_size()[0]/2, pg.display.get_window_size()[1]/2)

        #init round
        self.rounds = [random.choice(self.color_buttons)]
        self.current_round_number = 0
        self.input_round_number = 0
        self.cooldown = 50


    def update(self) -> None:
        #button update
        for color_button in self.color_buttons:
            color_button.update(self.cooldown)
        
        if self.game_type == con.MEMORY and self.current_state in self.active_game_states:
            if self.cooldown <= 0:
                self.led_button.light_down()

        self.cooldown -= 1

        #light up control
        if self.current_state == con.WAITING:
            self.cooldown -= 1
            
            cooldown_threshold = -20 if self.game_type == con.MEMORY else -5

            if self.cooldown <= cooldown_threshold:
                if self.current_round_number >= len(self.rounds):
                    self.current_state = con.INPUT
                    self.current_round_number = 0
                else:
                    target_round = self.current_round_number if self.game_type == con.MEMORY else len(self.rounds) - 1
                    self.led_button.light_up(self.rounds[target_round].color)
                    
                    if self.game_type == con.MEMORY:
                        self.rounds[self.current_round_number].click()
                        self.cooldown = 50
                    
                    self.current_round_number += 1
                    if self.game_type == con.MEMORY:
                        self.round_counter.update(self.current_round_number)

        #check rounds and change to waiting phase
        if self.current_state == con.INPUT:
            self.cooldown -= 1
            
            if self.cooldown <= 0:
                if self.input_round_number >= len(self.rounds):
                    self.current_state = con.WAITING
                    self.led_button.light_down()
                    self.rounds.append(random.choice(self.color_buttons)) #random
                    if self.game_type == con.REFLEX:
                        self.round_counter.update(len(self.rounds))
                    
                    if self.game_type == con.MEMORY:
                        self.input_round_number = 0
                        self.cooldown = 40
                    else:
                        self.cooldown = 80
                    
        if self.game_type == con.REFLEX and len(self.rounds) > 10:
            self._reset(self.game_type)

        if self.current_state in (con.START, con.GAME_OVER):
            self.video_player.update()

        self._update_music()
        


    def handle_event(self) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self._quit()
            elif event.type == pg.VIDEORESIZE:
                self.screen_size = event.w, event.h
                self.screen = pg.display.set_mode(self.screen_size, pg.RESIZABLE)
                for group in self.objects.values():
                    for object in group:
                        object.update_position(self.screen_size)
                for color_button in self.color_buttons:
                    color_button.update(self.cooldown)
            elif event.type == pg.MOUSEBUTTONDOWN:
                if self.current_state in (con.START, con.GAME_OVER):
                    if self.memory_start_button.rect.collidepoint((pg.mouse.get_pos())):
                        self.current_state = con.WAITING
                        self.memory_start_button.click()
                        self.game_type = con.MEMORY
                        self.video_player.stop()
                        self.led_button.light_down()
                        self.game_type_surf.set_game_type(self.game_type)
                        self.cooldown = 50
                    elif self.reflex_start_button.rect.collidepoint((pg.mouse.get_pos())):
                        self.current_state = con.WAITING
                        self.memory_start_button.click()
                        self.game_type = con.REFLEX
                        self.video_player.stop()
                        self.led_button.light_down()
                        self.start_time = pg.time.get_ticks()
                        self.game_type_surf.set_game_type(self.game_type)
                        self.cooldown = 50
                    elif self.memory_video_button.rect.collidepoint((pg.mouse.get_pos())):
                        self.cooldown = 50
                        if self.video_player.get_state() == con.MEMORY:
                            self.video_player.stop()
                        else:
                            self.video_player.play_memory_tutorial()
                    elif self.reflex_video_button.rect.collidepoint((pg.mouse.get_pos())):
                        self.cooldown = 50
                        if self.video_player.get_state() == con.REFLEX:
                            self.video_player.stop()
                        else:
                            self.video_player.play_reflex_tutorial()
                    elif self.exit_button.rect.collidepoint((pg.mouse.get_pos())):
                        self.exit_button.click()
                        self._quit()
                    
                    if self.current_state == con.GAME_OVER:
                        if self.new_profile_button.rect.collidepoint((pg.mouse.get_pos())):
                            self.current_state = con.START
                            self.player_name.reset_name()
                            print("new profile button is pressed")


                if self.current_state in self.active_game_states:
                    if self.stop_button.rect.collidepoint((pg.mouse.get_pos())):
                        self.current_state = con.GAME_OVER
                        self.result.load(self.game_type)
                        self.result.set_stop_option()
                        self.ranking_table.load(self.result.get_data())
                        self.led_button.light_down()
                        self.led_button.draw()
                        self.current_state = con.GAME_OVER
                        self.rounds = []
                        self.current_round_number = 0
                        self.input_round_number = 0
                        self.cooldown = 100
                        print("stop button is pressed")

                #input about color button
                """if self.cooldown < 0 and self.current_state == con.INPUT:
                    for color_button in self.color_buttons:
                        if (color_button.button_center.collidepoint((pg.mouse.get_pos()))):
                            self._handle_color_button_input(color_button)"""
                    
            elif event.type == pg.KEYDOWN:
                if self.current_state == con.START:
                    self.player_name.handle_input(event)

        if self.cooldown < 0 and self.current_state in (con.START, con.GAME_OVER):
            if not self.gpio.input(con.PORT_BLUE):
                self.current_state = con.WAITING
                self.game_type = con.MEMORY
                self.led_button.light_down()
                self.game_type_surf.set_game_type(self.game_type)
                self.cooldown = 50
            if not self.gpio.input(con.PORT_RED):
                self.current_state = con.WAITING
                self.game_type = con.REFLEX
                self.led_button.light_down()
                self.start_time = pg.time.get_ticks()
                self.game_type_surf.set_game_type(self.game_type)
                self.cooldown = 50
            if not self.gpio.input(con.PORT_GREEN):
                self.cooldown = 50
                if self.video_player.get_state() == con.REFLEX:
                    self.video_player.stop()
                else:
                    self.video_player.play_reflex_tutorial()
            if not self.gpio.input(con.PORT_YELLOW):
                self.cooldown = 50
                if self.video_player.get_state() == con.MEMORY:
                    self.video_player.stop()
                else:
                    self.video_player.play_memory_tutorial()
            
            
        if self.cooldown < 0 and self.current_state == con.INPUT:
            for color_button in self.color_buttons:
                if not self.gpio.input(color_button.port_num):
                    print("color button pressed")
                    self._handle_color_button_input(color_button)
    
    def draw(self) -> None:
        self.screen.fill(con.WHITE)

        for object in self.objects[self.current_state]:
            object.draw()

        """if self.current_state in self.active_game_states:
            round_surf = self.round_font.render(f"round {len(self.rounds)}", 0, con.BLACK)
            self.screen.blit(round_surf, (10,10))

            for color_button in self.color_buttons:
                color_button.draw()
                
            self.led_button.draw()"""

        pg.display.update()
        self.clock.tick(30)


    def _reset(self, game_type: str) -> None:
        self.result.load(game_type)
        if game_type == con.MEMORY:
            self.result.save(len(self.rounds)-1, self.player_name.get(), game_type)
        if game_type == con.REFLEX:
            self.end_time = pg.time.get_ticks()
            self.time = self.end_time - self.start_time
            self.result.save(self.time/1000, self.player_name.get(), game_type)
        self.ranking_table.load(self.result.get_data())
        self.rank = self.result.get_rank()
        self.led_button.light_down()
        self.led_button.light_up_for_rank(self.rank)
        self.led_button.draw()
        self.current_state = con.GAME_OVER
        self.rounds = []
        self.current_round_number = 0
        self.round_counter.update(self.current_round_number)
        self.input_round_number = 0
        self.cooldown = 100

    def _update_music(self):
        if self.current_state == con.START:
            if self.start_channel.get_busy() == False:
                pg.mixer.fadeout(3)
                self.start_channel.play(self.start_music)
        if self.current_state == con.WAITING:
            if self.waiting_channel.get_busy() == False:
                pg.mixer.fadeout(3)
                self.waiting_channel.play(self.waiting_music)
        if self.current_state == con.INPUT and len(self.rounds) >= 10:
            if self.input_channel.get_busy() == False:
                pg.mixer.fadeout(3)
                self.input_channel.play(self.input_music)
        if self.current_state == con.GAME_OVER:
            if self.game_over_channel.get_busy() == False:
                pg.mixer.fadeout(3)
                self.game_over_channel.play(self.game_over_music)
                self.game_over_channel.fadeout(10000)
                
    def _handle_color_button_input(self, color_button: ColorButton) -> None:
        if color_button == self.rounds[self.input_round_number]:
            color_button.click()
            self.cooldown = 20
            self.input_round_number += 1
            if self.game_type == con.MEMORY:
                self.led_button.light_up(color_button.color)
        else:
            if self.game_type == con.MEMORY:
                self._reset(self.game_type)





    def _quit(self) -> None:
        self.gpio.cleanup()
        self.led_button.light_down()
        self.led_button.draw()
        pg.quit()
        exit()
