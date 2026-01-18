from abc import ABC, abstractmethod
class Zombie(ABC):
    def __init__(self):
        super().__init__()
    @abstractmethod
    def draw(self, screen):
        pass
    def update(self):
        pass
    def change_state(self, new_state):
        pass