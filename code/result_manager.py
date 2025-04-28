import constants as con
import pygame as pg
import json
import os
import bisect
from resizable import Resizable

class Result(Resizable):
    def __init__(self, screen: pg.surface.Surface) -> None:
        self.screen = screen
        self.box_size = (600, 150)
        self.border_radius = self.box_size[1]//2
        self.color = con.WHITE
        self.text_color = con.BLACK
        self.font = pg.font.Font(None, 100)
        self.sub_font = pg.font.Font(None, 52)
        self.memory_score = 0
        self.reflex_score = 9999999
        self.your_name = "No Name"
        self.surface = pg.Surface((600,150) , pg.SRCALPHA)
        self.rect = self.surface.get_rect()
        self.rank = 0
        self.text = "Geen score"



    def draw(self) -> None:
        self.surface.fill((0, 0, 0, 0))  # Surface clear

        color = con.GOLD if self.rank == 1 else con.WHITE
        sub_text = "Nieuw record!!" if self.rank == 1 else "Goed bezig!"
        sub_text_surf = self.sub_font.render(sub_text, True, self.text_color)
        sub_text_rect = sub_text_surf.get_rect(
            center=(self.rect.centerx, self.rect.top - 20)
        )
        self.screen.blit(sub_text_surf, sub_text_rect)

        pg.draw.rect(self.surface, con.BLACK, (0, 0, *self.box_size), 2, border_radius=self.border_radius)
        pg.draw.circle(self.surface, con.BLACK, (self.border_radius, self.box_size[1] // 2), self.border_radius)
        pg.draw.circle(self.surface, color, (self.border_radius, self.box_size[1] // 2), self.border_radius - 10)

        rank_surf = self.font.render(str(self.rank), True, self.text_color)
        rank_rect = rank_surf.get_rect(center=(self.border_radius, self.box_size[1] // 2))
        self.surface.blit(rank_surf, rank_rect)

        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=(self.box_size[0] // 2 + 50, self.box_size[1] // 2))
        self.surface.blit(text_surf, text_rect)

        self.screen.blit(self.surface, self.rect)

    def update_position(self, screen_size) -> None:
        w, h = screen_size
        self.rect.center = (w // 4, h // 4)


    def load(self, game_type: str) -> None:
        self._check_file_exists(game_type)
        self.game_type = game_type

        try:
            with open(f'code/{game_type}_result.json', 'r', encoding='utf-8') as fp:
                self.data: list[dict] = json.load(fp)
                index = self._initialize_index(game_type)
                self.top_player = self.data[index].get("name")
                self.highscore = self.data[index].get("score")
                self.scores = [entry["score"] for entry in self.data]
                if game_type == con.MEMORY:
                    self.data.sort(key=lambda x: x["score"], reverse=True)
                else:
                    self.data.sort(key=lambda x: x["score"])
        except:
            self.data = []
            self.scores = []



    def save(self, new_score: int, name: str, game_type: str) -> None:
        self._check_file_exists(game_type)
        if game_type == con.MEMORY:
            self.text = f"{new_score} punten"
        else:
            self.text = f"{new_score:.3f} s"

        existing_index = next((i for i, item in enumerate(self.data) if item["name"] == name), None)
        if game_type == con.MEMORY:
            self.index = bisect.bisect_right([-entry["score"] for entry in self.data], -new_score)
        else:
            self.index = bisect.bisect_right([entry["score"] for entry in self.data], new_score)
        self.rank = self.get_rank()

        should_replace = True
        if existing_index is not None:
            existing_score = self.data[existing_index]["score"]
            if game_type == con.MEMORY and new_score <= existing_score:
                should_replace = False
            elif game_type != con.MEMORY and new_score >= existing_score:
                should_replace = False

            if should_replace:
                self.data.pop(existing_index)

        if should_replace:
            self.data.insert(self.index, {"name": name, "score": new_score})

            with open(f'code/{game_type}_result.json', 'w', encoding='utf-8') as fp:
                json.dump(self.data, fp, ensure_ascii=False, indent=4)

    def get_data(self) -> list[dict]:
        return self.data
        


    def get_rank(self) -> int:
        return self.index + 1
    
    def set_stop_option(self) -> None:
        self.rank = 0
        self.text = "Geen score"
    
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

    def _check_file_exists(self, game_type: str = "memory") -> None:
        if os.path.isfile(f'code/{game_type}_result.json') == False:
            with open(f'code/{game_type}_result.json', 'w', encoding='utf-8') as fp:
                json.dump([], fp, ensure_ascii=False, indent=4)


class RankingRow(Resizable):
    def __init__(self, screen: pg.Surface, rank: int, name: str, score: int, row_size: tuple[int, int], font: pg.font.Font):
        self.screen = screen
        self.rank = rank
        self.name = name
        self.score = score
        self.row_size = row_size
        self.surface = pg.Surface(row_size, pg.SRCALPHA)
        self.rect = self.surface.get_rect()
        self.font = font


    def update_position(self, screen_size):
        row_h = self.row_size[1]
        self.rect.center = (screen_size[0] * 3 // 4, screen_size[1] // 4 + (self.rank) * row_h)

    def draw(self) -> None:
        if self.rank == 0:
            self.surface.fill((200, 200, 200, 128))
            rank = "rang"
        else:
            self.surface.fill((0, 0, 0, 0))
            rank = str(self.rank)
        # render three columns: rank, name, score
        w, h = self.row_size
        # define column positions
        x_rank = w * 0.1
        x_name = w * 0.4
        x_score = w * 0.8
        y_center = h // 2
       
        # text surfaces
        rank_surf = self.font.render(str(rank), True, (0, 0, 0))
        name_surf = self.font.render(self.name, True, (0, 0, 0))
        score_surf = self.font.render(str(self.score), True, (0, 0, 0))

        # blit centered on each column x
        for surf, x in [(rank_surf, x_rank), (name_surf, x_name), (score_surf, x_score)]:
            rect = surf.get_rect(center=(x, y_center))
            self.surface.blit(surf, rect)

        self.screen.blit(self.surface, self.rect)


class RankingTable(Resizable):
    def __init__(self, screen: pg.Surface, screen_size:tuple[int,int],size: tuple[int,int]) -> None:
        self.screen = screen
        self.screen_size = screen_size
        self.size = size
        self.surf = pg.Surface(size)
        data = []
        for i in range(10):
            data.append({"name": "---", "score": "---"})
        self.data = data[:10]  # take top 10
        self.font = pg.font.Font(None, 36)
        # pre-create rows
        self.row_h = size[1] // 11  # 1 for header + 10 rows
        self.table_w = size[0]
        self.rows = [RankingRow(screen, 0, "naam", "score", (self.table_w,self.row_h), self.font)]
        for i, entry in enumerate(self.data, start=1):
            row = RankingRow(screen, i, entry['name'], entry['score'], (self.table_w, self.row_h), self.font)
            self.rows.append(row)

    def update_position(self, screen_size: tuple[int, int]) -> None:
        for row in self.rows:
            row.update_position(screen_size)
        self.screen_size = screen_size

    def draw(self) -> None:
        # draw each row
        for row in self.rows:
            row.draw()

    def load(self, data: list[dict]):
        for i in range(10-len(data)):
            data.append({"name": "---", "score": "---"})
        self.data = data[:10]  # take top 10
        self.rows = [RankingRow(self.screen, 0, "naam", "score", (self.table_w,self.row_h), self.font)]
        for i, entry in enumerate(self.data, start=1):
            row = RankingRow(self.screen, i, entry['name'], entry['score'], (self.table_w, self.row_h), self.font)
            self.rows.append(row)

        self.update_position(self.screen_size)



def rankingtable_test():
    pg.init()
    screen = pg.display.set_mode((600, 600), pg.RESIZABLE)
    pg.display.set_caption("Ranking Table Test")
    clock = pg.time.Clock()

    dummy_data = [
        {"name": f"Player{i+1}", "score": 100 - i * 5}
        for i in range(8)
    ]

    font = pg.font.Font(None, 32)

    table = RankingTable(
        screen=screen,
        screen_size=pg.display.get_window_size(),
        size=(400, 550),
    )

    table.load(dummy_data)

    running = True
    while running:
        screen.fill((255, 255, 255))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.VIDEORESIZE:
                screen = pg.display.set_mode(event.size, pg.RESIZABLE)

        table.update_position(screen.get_size())
        table.draw()

        pg.display.flip()
        clock.tick(60)

    pg.quit()

if __name__ == "__main__":
    with open('code/memory_result.json', 'r', encoding='utf-8') as fp:
        data: dict = json.load(fp)
        print(data)

    rankingtable_test()
