from obj_class import Obj

class Obstacle(Obj):
    def __init__(self, anim, sheet, anim_name, speed):
        super().__init__(anim, sheet, anim_name, "Obstacle", speed)

    def on_collide(self, pet, game):
        pet.health -= 1