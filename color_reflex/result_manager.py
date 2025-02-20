import constants as con
import pygame as pg
import json
import os

class Result():
    def __init__(self, screen: pg.surface.Surface, x: int, y: int) -> None:
        self.screen = screen
        self.width = 400
        self.whole_result_rect = pg.Rect(x-self.width/2, y, self.width, 50)
        self.your_result_rect = pg. Rect(x-self.width/2, y+75, self.width, 50)
        self.new_result_rect = pg.Rect(x-self.width/2, y+150, self.width, 50)
        self.color = con.RED
        self.hover_color = con.LIGHT_RED
        self.font = pg.font.Font(None, 36)
        self.new_score = 1000000
        self.your_highscore = 10000000
        self.your_name = "No Name"
        self.highscore = 100000000
        self.top_player = "No Name"


    def draw(self) -> None:
        self._draw(self.whole_result_rect, f"{self.top_player}'s highscore : {self.highscore} ms")
        self._draw(self.your_result_rect, f"Your best score : {self.your_highscore} ms")
        self._draw(self.new_result_rect, f"new score : {self.new_score} ms")


    def load(self) -> None:
        self._check_file_exists()

        with open('result.json', 'r', encoding='utf-8') as fp:
            data: dict = json.load(fp)
            self.top_player = data.get("name")
            self.highscore = data.get("score")


    def save(self, new_score: int, name: str) -> None:
        self._check_file_exists()
        self.new_score = new_score

        if new_score < self.your_highscore:
            self.your_highscore = new_score

        if new_score < self.highscore:
            self.highscore = new_score
            self.top_player = name

            with open('result.json', 'w', encoding='utf-8') as fp:
                json.dump({"name":name,"score":new_score}, fp, ensure_ascii=False, indent=4)
            return True
        return False


    def _draw(self, rect: pg.rect.Rect, text:str) -> None:
        mouse_pos = pg.mouse.get_pos()
        if rect.collidepoint(mouse_pos):
            pg.draw.rect(self.screen, self.hover_color, rect)
        else:
            pg.draw.rect(self.screen, self.color, rect)

        text_surf = self.font.render(text, True, con.BLACK)
        text_rect = text_surf.get_rect(center=rect.center)
        self.screen.blit(text_surf, text_rect)

    def _check_file_exists(self):
        if os.path.isfile('result.json') == False:
            with open('result.json', 'w', encoding='utf-8') as fp:
                json.dump({"name":"No Name","score":100000000}, fp, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    with open('result.json', 'r', encoding='utf-8') as fp:
        data: dict = json.load(fp)
        print(data)