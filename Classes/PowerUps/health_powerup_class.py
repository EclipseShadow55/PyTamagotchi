from ..powerup_class import Powerup

class HealthPowerup(Powerup):
    def __init__(self, anim, sheet, anim_name, speed):
        super().__init__(anim, sheet, anim_name, speed, "Health Buff")

    def start(self):
        self.pet.health += 1