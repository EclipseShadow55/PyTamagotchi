import os
import json

with open("data.json", "r") as f:
    data = json.load(f)
    timings = data.get("timings", None)
    colors = data.get("colors", None)
    name = data.get("name", None)
files = os.listdir("Pet") + os.listdir("Extras") + os.listdir("Backdrops")
pngs = [file for file in files if file.endswith(".png")]
bmps = [file for file in files if file.endswith(".bmp")]
if pngs.sort() != bmps.sort() or None in [name, timings, colors]:
    print("Please run setup.py before you run this one. This program will not work without the necessary setup. Also run setup.py if you have changed any sprites in the Extras folder")

screen_width = 128
base_obj_speed = 50
pet_speed = 10

os.environ["TIMINGS"] = json.dumps(timings)
os.environ["SCREEN_WIDTH"] = json.dumps(screen_width)
os.environ["BASE_OBJ_SPEED"] = json.dumps(base_obj_speed)

import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import time
from Classes.pet_class import Pet
from Classes.game_class import Game
import pygame

pygame.init()

#TO-DO: fix
def load_bmp(file_path):
    bmp = displayio.OnDiskBitmap(file_path)
    try:
        file_colors = colors[file_path[5:-4]]
        palette = displayio.Palette(len(file_colors["colors"]) + 1)
        palette[0] = file_colors["t_color"]
        palette.make_transparent(0)
        for ind in range(1, len(file_colors["colors"]) + 1):
            print(f"{ind}: {file_colors['colors'][ind - 1]}")
            palette[ind] = file_colors["colors"][ind - 1]
    except KeyError as e:
        palette = None
    return bmp, palette

display = PyGameDisplay(width=128, height=128)
splash = displayio.Group()
display.show(splash)

intro_sheet, intro_palette = load_bmp("Backdrops/Intro.bmp")
happy_idle_sheet, happy_idle_palette = load_bmp("Pet/HappyIdle.bmp")
open_back_sheet, open_back_palette = load_bmp("Backdrops/OpenBack.bmp")
neutral_idle_sheet, neutral_idle_palette = load_bmp("Pet/NeutralIdle.bmp")
sad_idle_sheet, sad_idle_palette = load_bmp("Pet/SadIdle.bmp")


intro_animation = displayio.TileGrid(
    bitmap=intro_sheet,
    pixel_shader=intro_palette,
    width=1,
    height=1,
    tile_width=128,
    tile_height=128,
    default_tile=0,
    x=0,
    y=0
)

happy_idle_animation = displayio.TileGrid(
    happy_idle_sheet,
    pixel_shader=happy_idle_palette,
    width=1,
    height=1,
    tile_width=128,
    tile_height=128,
    default_tile=0,
    x=0,
    y=0
)

neutral_idle_animation = displayio.TileGrid(
    neutral_idle_sheet,
    pixel_shader=neutral_idle_palette,
    width=1,
    height=1,
    tile_width=128,
    tile_height=128,
    default_tile=0,
    x=0,
    y=0
)

sad_idle_animation = displayio.TileGrid(
    neutral_idle_sheet,
    pixel_shader=neutral_idle_palette,
    width=1,
    height=1,
    tile_width=128,
    tile_height=128,
    default_tile=0,
    x=0,
    y=0
)

open_background = displayio.TileGrid(open_back_sheet, pixel_shader=open_back_palette)

splash.append(intro_animation)
display.refresh()
for item in splash:
    print(item)
for i in range(intro_sheet.width // screen_width):
    print("intro", i)
    intro_animation[0] = i
    display.refresh()
    time.sleep(timings["intro"][i % len(timings["intro"])])

splash.remove(intro_animation)
splash.append(open_background)
display.refresh()

settings = {"game": [open_background, open_back_sheet], "inside": [open_background, open_back_sheet], "fridge": [open_background, open_back_sheet]}
setting = 1
#TO-DO: make eating, petting, and playing animations
anims = {"eating": [happy_idle_animation, happy_idle_sheet], "petting": [sad_idle_animation, sad_idle_sheet], "playing": [happy_idle_animation, happy_idle_sheet], "ko": [sad_idle_animation, sad_idle_sheet]}
busy = False
total_time = 0
timer = 0
game = None
idles = {"sad": [sad_idle_animation, sad_idle_sheet, "sad_idle"], "neutral": [neutral_idle_animation, neutral_idle_sheet, "neutral_idle"], "happy": [happy_idle_animation, happy_idle_sheet, "happy_idle"]}
pet = Pet(idles, splash, input("Enter a name for your pet (or enter for default name): "), pet_speed)

while True:
    up = False
    left = False
    right = False
    time_dif, timer = pet.run_frame(timer)
    total_time += time_dif
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_LEFT:
                    left = True
                case pygame.K_RIGHT:
                    right = True
                case pygame.K_UP:
                    up = True

    if right and setting < 2:
        if not busy:
            setting += 1
            splash.remove(pet.anim)
            splash.remove(settings[list(settings.keys())[setting - 1]][0])
            splash.append(settings[list(settings.keys())[setting]][0])
            splash.append(pet.anim)
    elif left and setting > 0:
        if not busy:
            setting -= 1
            splash.remove(pet.anim)
            splash.remove(settings[list(settings.keys())[setting + 1]][0])
            splash.append(settings[list(settings.keys())[setting]][0])
            splash.append(pet.anim)
    match setting:
        case 0:
            if up:
                if not busy:
                    busy = True
                    #TO-DO: make game_background and ko_animation
                    game = Game(pet, settings["game"][0], settings["game"][1], anims["playing"][0], anims["playing"][1], anims["ko"][0], anims["ko"][1])
            if busy:
                game.run(time_dif, left, right)
        case 1:
            if not busy and up:
                busy = True
                pet.set_anim(idles["happy"][0], idles["happy"][1], "petting", True)
                pet.happiness += 20
            if (not pet.oneTime) and busy:
                print("busy off")
                busy = False
        case 2:
            if not busy and up:
                busy = True
                pet.set_anim(idles["sad"][0], idles["sad"][1], "feeding", True)
                pet.hunger += 60
            if (not pet.oneTime) and busy:
                print("busy off")
                busy = False
    display.refresh()
    time.sleep(time_dif)