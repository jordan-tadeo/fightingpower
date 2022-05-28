class Character:
    def __init__(self, health, xpos, ypos, zpos):
        self._health = health
        self._xpos = xpos
        self._ypos = ypos

# Getters/Setters
    def get_health(self): 
        return self._health
    def set_health(self, health): 
        self._health = health
    def get_xpos(self):
        return self._xpos
    def set_xpos(self, xpos):
        self._xpos = xpos
    def get_ypos(self):
        return self._ypos
    def set_ypos(self, ypos):
        self._ypos = ypos

#functions
    #Check if alive
    def isAlive(self):
        return max(0, self.get_health())

    #inflict injury
    def injure(self, anatomic):
        match anatomic:
            case "head":
                self.set_health(self.get_health-20)
            case "body":
                self.set_health(self.get_health-10)
            case "arm":
                self.set_health(self.get_health-5)
            case "leg":
                self.set_health(self.get_health-5)