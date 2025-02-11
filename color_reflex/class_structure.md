```mermaid
classDiagram
    class GameManager{
        -game_state: START,WAITING,INPUT,GAME_OVER
        -current_state
        -rounds: list[ColorButton]
        -current_round_number
        -input_current_number
        -cooldown

        +draw()
        +update()
        +handle_event()
    }

    class ColorButton{
        -x -y
        -color
        -light_color
        -is_clicked

        +click()
        +update()
        +draw()
    }

    class LEDButton{
        
    }

    class MenuButton{
        -x -y
        -text
        -color
        -hover_color

        +draw()
        +update()
    }

    class Result{
        -x -y
        -highscore
        -top_player
        -your_highscore
        -your_name

        +draw()
        +load()
        +save(new_score: int, name: str)
    }

    class PlayerName{
        -x -y
        -color

        +draw()
        +handle_input(event)
        +get() name:str
    }

    GameManager --> ColorButton : own
    GameManager --> MenuButton : own
    GameManager --> Result : own
    GameManager --> PlayerName : own
    note for GameManager "main"