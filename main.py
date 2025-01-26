import os
import json

with open("data.json", "r") as f:
    data = json.load(f)
    timings = data["timings"]
    t_colors = data["t_colors"]
screen_width = 128
base_obj_speed = 50
pet_speed = 10

os.environ["TIMINGS"] = json.dumps(timings)
os.environ["SCREEN_WIDTH"] = json.dumps(screen_width)
os.environ["BASE_OBJ_SPEED"] = json.dumps(base_obj_speed)

import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import pygame
import time
import misc
from Classes.pet_class import Pet
from Classes.game_class import Game

misc.convertAll()
pygame.init()

#TO-DO: fix
def load_bmp(file_path):
    back_color = t_colors.get(file_path[file_path.rfind("/") + 1:], None)
    if back_color is not None:
        back_color = (back_color[0] << 16) | (back_color[1] << 8) | back_color[2]
    bmp = displayio.OnDiskBitmap(file_path)
    palette = displayio.Palette(256)
    if bmp.pixel_shader is None:
        palette[0] = back_color #Doesn't like this line
    else:
        for i in range(256):
            palette[i] = bmp.pixel_shader[i]
    if back_color is not None:
        palette.make_transparent(back_color)
    return bmp, palette

display = PyGameDisplay(width=128, height=128)
splash = displayio.Group()
display.show(splash)

intro_sheet, intro_palette = load_bmp("BMPs/Intro.bmp")
happy_idle_sheet, happy_idle_palette = load_bmp("BMPs/HappyIdle.bmp")
open_back_sheet, open_back_palette = load_bmp("BMPs/OpenBack.bmp")
neutral_idle_sheet, neutral_idle_palette = load_bmp("BMPs/NeutralIdle.bmp")
sad_idle_sheet, sad_idle_palette = load_bmp("BMPs/SadIdle.bmp")


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
for i in range(intro_sheet.width // screen_width):

    intro_animation[0] = i
    display.refresh()
    time.sleep(timings["intro"][i % len(timings["intro"])])

splash.remove(intro_animation)
splash.append(open_background)
display.refresh()

settings = {"backyard": open_background, "inside": open_background, "fridge": open_background}
setting = 1
#TO-DO: make eating, petting, and playing animations
anims = {"eating": [eating_animation, eating_sheet], "petting": [petting_animation, petting_sheet], "playing": [playing_animation, playing_sheet]}
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
            splash.remove(setting[list(settings.keys())[setting - 1]])
            splash.append(setting[list(settings.keys())[setting]])
            splash.append(pet.anim)
    elif left and setting > 0:
        if not busy:
            setting -= 1
            splash.remove(pet.anim)
            splash.remove(setting[list(settings.keys())[setting + 1]])
            splash.append(setting[list(settings.keys())[setting]])
            splash.append(pet.anim)
    match setting:
        case 0:
            if up:
                if not busy:
                    busy = True
                    #TO-DO: make game_background and ko_animation
                    game = Game(pet, game_background_animation, game_background_sheet, anims["playing"][0], anims["playing"][1], ko_animation, ko_sheet)
            if busy:
                game.run()
        case 1:
            if not busy and up:
                busy = True
                pet.set_anim(idles["happy"], True)
                pet.happiness += 20
        case 2:
            if not busy and up:
                busy = True
                pet.set_anim(idles["sad"], True)
                pet.hunger += 60
    display.refresh()
    time.sleep(time_dif)