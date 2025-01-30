# PyTamagotchi
Tamagotchi made using CircuitPython (and PyGame for PC display)

## Setup
### With Python (Windows PC)
1. Install [Python](https://www.python.org/downloads/)
2. Download the files from the [Github repository](https://github.com/EclipseShadow55/PyTamagotchi)
3. Run `dependencies.bat` to install dependencies
4. Run `tamagotchi.py`
5. Enjoy!
### With Python (Linux)
1. Install [Python](https://www.python.org/downloads/)
2. Download the files from the [Github repository](https://github.com/EclipseShadow55/PyTamagotchi)
3. Run `dependencies.sh` to install dependencies
4. Run `tamagotchi.py`
5. Enjoy!
### With CircuitPython (CircuitPython Compatible Board)
1. Install [CircuitPython](https://learn.adafruit.com/welcome-to-circuitpython/installing-circuitpython) on your board
2. Download the files from the [Github repository](https://github.com/EclipseShadow55/PyTamagotchi)
### With Executable (Windows PC)
1. Download the [latest stable Windows release](TBD)
2. Run `tamagotchi.exe`
3. Enjoy!
### With Executable (Linux)
1. Download the [latest stable Linux release](TBD)
2. Run `tamagotchi.bin`
3. Enjoy!
## Controls
### PC
Up Arrow Key: Action associated with the current screen
Left Arrow Key: Switch scenes to the left, move left in game
Right Arrow Key : Switch scenes to the right, move right in game
### CircuitPython
Up Button: Action associated with the current screen
Left Button: Switch scenes to the left, move left in game
Right Button: Switch scenes to the right, move right in game
## Screens
### Indoors (Started Screen)
- Pet to increase happiness
### Kitchen (1 To The Right)
- Feed pet to increase hunger (I know it doesn't make too much sense, but more hunger is a good thing)
### Outdoors (1 To The Left)
- Play with pet to increase happiness
## Customization
### Changing Pet
1. Replace any sprite in PNGs with your own pet sprites, making sure to keep the EXACT SAME NAMES
   1. I recommend using [Piskel](https://www.piskelapp.com/) to create your sprites
   2. Make sure to export your sprites as Sprite-Sheet PNGs
   3. Pick a dimension that is a multiple of 128x128 for the best results
   4. Make sure to keep the same dimensions for all of the pet sprites
2. Run `setup.py` to convert the sprites to the correct format
3. 