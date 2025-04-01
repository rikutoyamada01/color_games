# color_games
For STEM lesson to make the games that are good for elder people

## 1. Installation

### Clone the repo
```sh
git clone https://github.com/rikutoyamada01/color_games
```

### Navigate to the project folder
```sh
cd color_games
```

### Install dependencies
(Optional: using virtual environment)
```sh
python3 -m venv venv
```

#### Activate virtual environment
**For Windows:**
```sh
venv\Scripts\Activate
```
**For macOS/Linux:**
```sh
source venv/bin/activate
```

#### Install required packages
```sh
pip install -r requirements.txt
```

## 2. Usage
#### Run the game:
**For Rasberry Pi**
```sh
sudo python code/main.py
```
("sudo" is for using rpi_ws281x)

**For Windows**
```command prompt
python code/main.py
```

#### Deactivate virtual environment
(If using virtual environment, deactivate when done:)
```sh
deactivate
```

## 3. License
This project is not licensed.
