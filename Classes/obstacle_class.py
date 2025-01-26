from obj_class import Obj

class Obstacle(Obj):
    def onColide(self, pet, game):
        pet.change("health", -1)