import os
import json

timings = json.loads(os.environ["TIMINGS"])

class Pet:
	def __init__(self, idles, splash, speed, name="Pet"):
		self.idles = idles
		self.resetAnim()
		self.splash = splash
		self.name = name
		self.frame = 0
		self.happiness = 50
		self.hunger = 50
		self.exercise = 50
		self.oneTime = False
		self.time_dif = 0.1
		self.speed = speed
		self.powerUps = {}
		self.health = 0
        
	def setAnim(self, anim, sheet, animName, oneTime=False):
		self.splash.remove(self.anim)
		self.splash.append(anim)
		self.anim = anim
		self.animName = animName
		self.sheet = sheet
		self.oneTime = oneTime
	
	def addPowerup(self, powerUp, duration):
		self.powerUps[powerUp] = duration
		powerUp.start()
	
	def clearPowerups(self):
		for powerUp in self.powerUps:
			powerUp.end()
        
	def runFrame(self, time):
		time += self.time_dif
		time_set = timings[self.animName]
		if time >= time_set[frame % len(time_set)]:
			self.frame += 1
			if frame == self.sheet.width // self.anim.tile_width:
				if self.oneTime:
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
		self.splash.remove(self.anim)
		self.anim, self.sheet, self.animName = self.idles[self.state]
		self.splash.append(self.anim)
        
	def move(self, x, y):
		self.anim.x += x
		self.anim.y += y

	def moveTo(self, x, y):
		self.anim.x = x
		self.anim.y = y