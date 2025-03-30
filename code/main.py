from game_manager import GameManager

def main():
    game_manager = GameManager()

    while True:
        game_manager.handle_event()

        game_manager.update()

        game_manager.draw()


if __name__ == "__main__":
    main()