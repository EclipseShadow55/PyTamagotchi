import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import pygame
import time
import json

pygame.init()

with open("data.json", "r") as f:
    timings = json.load(f)["timings"]
    t_colors = json.load(f)["t_colors"]

def load_bmp(file_path):
    back_color = t_colors.get(file_path[file_path.findLast("/") + 1:], None)
    bmp = displayio.OnDiskBitmap(file_path)
    palette = displayio.Palette(256)
    for i in range(256):
        palette[i] = bmp.pixel_shader[i]
    if back_color is not None:
        palette.make_transparent(back_color)
    return bmp, palette

display = PyGameDisplay(width=128, height=128)
splash = displayio.Group()
display.show(splash)


tile_width = 128
tile_height = 128

intro_sheet, intro_palette = load_bmp("BMPs/Intro.bmp")
happpy_idle_sheet, happpy_idle_palette = load_bmp("BMPs/HappyIdle.bmp")
open_back_sheet, open_back_palette = load_bmp("BMPs/OpenBack.bmp")


intro_animation = displayio.TileGrid(
    bitmap=intro_sheet,
    pixel_shader=intro_palette,
    width=1,
    height=1,
    tile_width=tile_width,
    tile_height=tile_height,
    default_tile=0,
    x=0,
    y=0
)

happpy_idle_animation = displayio.TileGrid(
    happpy_idle_sheet,
    pixel_shader=happpy_idle_sheet.pixel_shader,
    width=1,
    height=1,
    tile_width=tile_width,
    tile_height=tile_height,
    default_tile=0,
    x=0,
    y=0
)

open_background = displayio.TileGrid(open_back_sheet, pixel_shader=open_back_sheet.pixel_shader)

splash.append(intro_animation)
display.refresh()
for i in range(intro_sheet.width // tile_width):
    intro_animation[0] = i
    display.refresh()
    time.sleep(timings["intro"][i % len(timings["intro"])])


state = ["idle", "happy"]
frame = 0
max_frame = happpy_idle_sheet.width // tile_width
#Main Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    happpy_idle_animation[0] = frame
    display.refresh()
    time.sleep(timings[state[1] + "_" + state[0]][i % len(timings[state[1] + "_" + state[0]])])
    frame = (frame + 1) % max_frame