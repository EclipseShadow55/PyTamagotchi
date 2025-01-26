import os
import json

timings = json.loads(os.environ["TIMINGS"])

class Obj:
	def __init__(self, anim, sheet, anim_name, type, splash):
		self.anim = anim
		self.sheet = sheet
		self.anim_name = anim_name
		self.type = type
		self.splash = splash
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