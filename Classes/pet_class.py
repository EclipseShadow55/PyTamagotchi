import os
import json

timings = json.loads(os.environ["TIMINGS"])

class Pet:
	def __init__(self, idles, splash, speed, name="Pet"):
		self.idles = idles
		self.state = "neutral"
		self.anim = None
		self.anim_name = None
		self.sheet = None
		self.splash = splash
		self.name = name
		self.frame = 0
		self.happiness = 50
		self.hunger = 50
		self.exercise = 50
		self.oneTime = False
		self.time_dif = 0.1
		self.speed = speed
		self.power_ups = []
		self.health = 0
		if self.happiness < 30 or self.hunger < 30 or self.exercise < 30:
			self.state = "sad"
		elif self.happiness < 70 or self.hunger < 70 or self.exercise < 70:
			self.state = "neutral"
		else:
			self.state = "happy"
		self.anim, self.sheet, self.anim_name = self.idles[self.state]
		self.splash.append(self.anim)
        
	def set_anim(self, anim, sheet, anim_name, one_time=False):
		self.splash.remove(self.anim)
		self.splash.append(anim)
		self.anim = anim
		self.anim_name = anim_name
		self.sheet = sheet
		self.oneTime = one_time
	
	def add_powerup(self, power_up, duration):
		self.power_ups.append([power_up])
		power_up.start()

	def rem_powerup(self, power_up):
		self.power_ups.remove(power_up)
		power_up.stop()
	
	def clear_powerups(self):
		for power_up in self.power_ups:
			self.rem_powerup(power_up)
        
	def run_frame(self, time):
		time += self.time_dif
		time_set = timings.get(self.anim_name, [0.3])
		if time >= time_set[self.frame % len(time_set)]:
			self.frame += 1
			if self.frame == self.sheet.width // self.anim.tile_width:
				if self.oneTime:
					self.reset_anim()
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
		for power_up in self.power_ups:
			power_up.run(self.time_dif)
		return self.time_dif, time
        
	def reset_anim(self):
		if self.happiness < 30 or self.hunger < 30 or self.exercise < 30:
			self.state = "sad"
		elif self.happiness < 70 or self.hunger < 70 or self.exercise < 70:
			self.state = "neutral"
		else:
			self.state = "happy"
		self.splash.remove(self.anim)
		self.anim, self.sheet, self.anim_name = self.idles[self.state]
		self.splash.append(self.anim)
        
	def move(self, x, y):
		self.anim.x += x
		self.anim.y += y

	def move_to(self, x, y):
		self.anim.x = x
		self.anim.y = y