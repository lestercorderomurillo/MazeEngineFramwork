import pygame, math, Constantes

from BloqueAbstracto import BloqueAbstracto

class BloqueMetalico(BloqueAbstracto):
    """Clase para el bloque metálico del juego"""

    def __init__(self, x, y):
        """Constructor"""

        super().__init__(x, y)
        self.image = self.crearAnimacion(32*14, 32*1, 32, 32)
        self.vida = 4


    def update(self):

        if self.destruido:
            self.kill()

        elif self.vida == 2:#self.vida/2 :
            self.image = self.crearAnimacion(32*15, 32*1, 32, 32)