import os
import json

timings = json.loads(os.environ["TIMINGS"])

class Obj:
	def __init__(self, anim, sheet, anim_name, type, speed):
		self.anim = anim
		self.sheet = sheet
		self.anim_name = anim_name
		self.type = type
		self.speed = speed
		self.time = 0
		self.frame = 0
	
	def resetAnim(self):
		self.anim[0] = 0
        
	def runFrame(self, time_dif):
		self.time += time_dif
		if self.time >= timings:
			frame = (frame + 1) % (self.sheet.width // self.anim.tile_width)
			self.time = 0
			self.anim[0] = frame
	
	def move(self, x, y):
		self.anim.x += x
		self.anim.y += y
	
	def moveTo(self, x, y):
		self.anim.x = x
		self.anim.y = y
	
	def onColide(self, pet, game):
		pass