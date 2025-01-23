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

splash.remove(intro_animation)
splash.append(open_background)
splash.append(


class Pet:
	def __init__(self, idles, splash, name="Pet"):
		self.idles = idles
		self.resetAnim()
		self.splash = splash
		self.ko_anim self.ko_anim = ko_anim
		self.name = pet
		self.frame = 0
		self.happiness = 50
		self.hunger = 50
		self.exercise = 50
		self.oneTime = False
		self.time_dif = 0.1
        
	def setAnim(self, anim, animName, sheet, oneTime):
		splash.remove(self.anim)
		splash.append(anim)
		self.anim = anim
		self.animName = animName
		self.sheet = sheet
		self.oneTime = oneTime
        
	def get(self, query):
		rets = []
		for item in query.lower().split():
			match item:
				case "anim":
					rets.append(self.anim)
				case "sheet":
					rets.append(self.sheet)
				case "splash":
					rets.append(self.splash)
				case "frame":
					rets.append(self.frame)
				case "happiness":
					rets.append(self.happiness)
				case "hunger":
					rets.append(self.hunger)
				case "exercise":
					rets.append(self.exercise)
				case "onetime":
					rets.append(self.oneTime)
				case "animname":
					rets.append(self.animName)
				case "name":
					rets.append(self.name)
				case "idles":
					rets.append(self.idles)
				case "state":
					rets.append(self.state)
		return rets
        
	def runFrame(self, time):
		time += self.time_dif
		time_set = timings[self.animName]
		if time == time_set[frame % len(time_set)]:
			self.frame += 1
			if frame == self.sheet.width // tile_width:
				if oneTime:
					self.resetAnim()
				else:
					frame = 0
			time = 0
		self.happiness -= 0.05
		self.hunger -= 0.05
		self.exercise -= 0.05
		if self.happiness < 0:
			self.happiness = 0
		if self.hunger < 0:
			self.hunger = 0
		if self.exercise < 0:
			self.exercise = 0
		return self.time_dif, time
        
	def resetAnim(self):
		if self.happiness < 30 or self.hunger < 30 or self.exercise < 30:
			self.state = "sad"
		elif self.happiness < 70 or self.hunger < 70 or self.exercise < 70:
			self.state = "neutral"
		else:
			self.state = "happy"
		self.anim, self.sheet, self.animName = *self.idles[self.state]
        
	def move(self, x, y):
		self.anim.x += x
		self.anim.y += y
		
			

settings = {"backyard": backyard_scene, "inside": inside_scene, "fridge": kitchen_scene}
setting = 1
anims = {"eating": eating_sheet, "petting": petting_sheet, "game": game_sheet}
busy = False
total_time = 0
time = 0
game = None
pet = Pet(neutral_idle_animation, neutral_idle_sheet, splash)

while True:
	action = False
	left = False
	right = False
	if right_pressed and setting < 2:
		if not busy:
			setting += 1
			splash.remove(pet.get("anim")[0])
			splash.remove(setting[settings.keys()[setting - 1]])
			splash.append(setting[settings.keys()[setting]])
			splash.append(pet.get("anim")[0])
		else:
			left = True
	elif left_pressed and setting > 0:
		if not busy:
			setting -= 1
			splash.remove(pet.get("anim")[0])
			splash.remove(setting[settings.keys()[setting + 1]])
			splash.append(setting[settings.keys()[setting]])
			splash.append(pet.get("anim")[0])
	elif up_pressed:
		action = True
	match setting:
		case 0:
			if action:
				if not busy:
					busy = True
					game = Game(pet)
				else:
					game.jump()
			if busy:
				game.run()
		case 1:
			if not busy and action
				busy = True
				start_petting(pet)
		case 2:
			if not busy and action:
				busy = True
				start_eating(pet)
	time_dif, time = pet.runFrame(time)
	total_time += time_dif
	time.sleep(time_dif)
