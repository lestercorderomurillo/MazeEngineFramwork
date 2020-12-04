from ME_Framework.Entidad.ME_Entidad import ME_Entidad

class Medalla(ME_Entidad):
    """Clase para la entidad medalla"""

    def __init__(self, x, y, bando):
        """Constructor"""

        super().__init__(x, y)

        self.rescadasRestantes = 3

        self.tomada = False
        self.bando = bando
        self.destruida = False

        self.xInicial = x
        self.yInicial = y

        if(self.bando == 1):
            self.imageSrc = self.crearAnimacion(32*9,32*3, 32, 32)
        else:
            self.imageSrc = self.crearAnimacion(32*8,32*4, 32, 32)

        self.image = self.imageSrc

        #self.sonidoEntregarMedalla = pygame.mixer.Sound(Constantes.S_BANDERA)
        #self.sonidoEntregarMedalla.set_volume(Constantes.VOLUMEN)

    def update(self, jugador):
        """Método para actualizar el estado de la entidad medalla"""

        if(self.bando == 1):
            if (self.tomada):
                if nivel.tanqueJugador.muerto == True:
                    self.rect.x = self.xInicial
                    self.rect.y = self.yInicial
                    self.tomada = False
                else:
                    if (jugador.direccion == 1):
                        self.rect.x = jugador.rect.x + 16
                        self.rect.y = jugador.rect.y - 2
                        self.image = pygame.transform.flip(self.imageSrc, False, False)
                    if (jugador.direccion == 3):
                        self.rect.x = jugador.rect.x + 16
                        self.rect.y = jugador.rect.y - 31
                        self.image = pygame.transform.flip(self.imageSrc, False, False)
                    if (jugador.direccion == 2):
                        self.rect.x = jugador.rect.x + 3
                        self.rect.y = jugador.rect.y - 16
                        self.image = pygame.transform.flip(self.imageSrc, False, False)
                    if (jugador.direccion == 4):
                        self.rect.x = jugador.rect.x - 3
                        self.rect.y = jugador.rect.y - 16 
                        self.image = pygame.transform.flip(self.imageSrc, True, False)
                    if (self.rect.colliderect(nivel.depositoMedalla)):
                        self.tomada = False
                        self.rescadasRestantes -= 1
                        #self.sonidoEntregarMedalla.play()
            else:
                self.rect.x = self.x_inicial
                self.rect.y = self.y_inicial
                if (self.rect.colliderect(jugador)):
                    self.tomada = True