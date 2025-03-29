import constants as con
import pygame as pg
import json
import os
import bisect

class Result():
    def __init__(self, screen: pg.surface.Surface, x: int, y: int, game_type: str = "memory") -> None:
        self.screen = screen
        self.width = 300
        self.whole_result_rect = pg.Rect(x-self.width/2, y, self.width, 50)
        self.your_result_rect = pg. Rect(x-self.width/2, y+75, self.width, 50)
        self.color = con.RED
        self.hover_color = con.LIGHT_RED
        self.font = pg.font.Font(None, 36)
        self.your_highscore = self._initialize_score(game_type)
        self.highscore = self._initialize_score(game_type)
        self.your_name = "No Name"
        self.top_player = "No Name"


    def draw(self) -> None:
        self._draw(self.whole_result_rect, f"{self.top_player}'s highscore : {self.highscore}")
        self._draw(self.your_result_rect, f"Your best score : {self.your_highscore}")


    def load(self, game_type: str = "memory") -> None:
        self._check_file_exists()

        try:
            with open(f'code/{game_type}_result.json', 'r', encoding='utf-8') as fp:
                self.data: list[dict] = json.load(fp)
                index = self._initialize_index(game_type)
                self.top_player = self.data[index].get("name")
                self.highscore = self.data[index].get("score")
                self.scores = [entry["score"] for entry in self.data]
        except:
            self.data = []
            self.top_player = "No Name"
            self.highscore = self._initialize_score(game_type)
            self.scores = [self._initialize_score(game_type)]



    def save(self, new_score: int, name: str, game_type: str = "memory") -> None:
        self._check_file_exists()
        self.index = bisect.bisect_left(self.scores, new_score)

        self.data.insert(self.index, {"name":name, "score":new_score})

        self._update_highscores(new_score, name, game_type)

        with open(f'code/{game_type}_result.json', 'w', encoding='utf-8') as fp:
                json.dump(self.data, fp, ensure_ascii=False, indent=4)
    
    def _initialize_score (self,game_type: str) -> int:
        if game_type == "memory":
            return 0
        else:
            return 9999999
        
    def _initialize_index(self, game_type: str) -> int:
        if game_type == "memory":
            return -1
        else:
            return 0
        
    def _update_highscores(self,new_score, name,game_type: str) -> None:
        if game_type == "memory":
            if new_score > self.your_highscore:
                self.your_highscore = new_score

            if new_score > self.highscore:
                self.highscore = new_score
                self.top_player = name
        else:
            if new_score < self.your_highscore:
                self.your_highscore = new_score
            
            if new_score < self.highscore:
                self.highscore = new_score
                self.top_player = name

    def _draw(self, rect: pg.rect.Rect, text:str) -> None:
        mouse_pos = pg.mouse.get_pos()
        if rect.collidepoint(mouse_pos):
            pg.draw.rect(self.screen, self.hover_color, rect)
        else:
            pg.draw.rect(self.screen, self.color, rect)

        text_surf = self.font.render(text, True, con.BLACK)
        text_rect = text_surf.get_rect(center=rect.center)
        self.screen.blit(text_surf, text_rect)

    def _check_file_exists(self, game_type: str = "memory") -> None:
        if os.path.isfile(f'code/{game_type}_result.json') == False:
            with open(f'code/{game_type}_result.json', 'w', encoding='utf-8') as fp:
                json.dump([], fp, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    with open('code/memory_result.json', 'r', encoding='utf-8') as fp:
        data: dict = json.load(fp)
        print(data)
