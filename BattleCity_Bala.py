## @package Bala
# Clase para bala, el proyectil arma que usa los tanques
from ME_Arma import ArmaMarda
from ME_Entidad import Direccion
from ME_Entidad import Bando

from BattleCity_BloqueAgua import BloqueAgua
from BattleCity_BloqueHojas import BloqueHojas
from BattleCity_BloqueIndestructible import BloqueIndestructible
from BattleCity_BloqueLadrillo import BloqueLadrillo
from BattleCity_BloqueMetalico import BloqueMetalico

import pygame, math

class Bala(ArmaMarda):
    """Clase hija de la entidad proyectil"""

## Constructor de la clase Bala
#\details El constructor inicializa los valores de la bala, como dirección o velocidad de la misma. Asimismo, agregaa animaciones y sonidos para la misma
#\param No recibe parametros
#\return No retorna
    def __init__(self,x, y, direccion, tamanio, bando):
        """Constructor"""

        if (direccion == Direccion.Arriba):
            x += tamanio/2.6666
            y += tamanio/4
        elif (direccion == Direccion.Abajo):
            x += tamanio/2.6666
            y += tamanio/1.92
        elif (direccion == Direccion.Derecha):
            x += tamanio/1.92
            y += tamanio/2.6666
        elif (direccion == Direccion.Izquierda):
            x += tamanio/4
            y += tamanio/2.6666
        
        super().__init__(x, y, direccion, tamanio)

        escala = (math.floor(tamanio/4), math.floor(tamanio/4))

        self.bando = bando
        self.ataque = 1
        self.animacionArriba.append(    pygame.transform.scale(self.crearAnimacion(32*13+0 , 0, 8, 8), escala))
        self.animacionDerecha.append(   pygame.transform.scale(self.crearAnimacion(32*13+8 , 0, 8, 8), escala))
        self.animacionAbajo.append(     pygame.transform.scale(self.crearAnimacion(32*13+16, 0, 8, 8), escala))
        self.animacionIzquierda.append( pygame.transform.scale(self.crearAnimacion(32*13+24, 0, 8, 8), escala))
        self.animacionExplosion.append( pygame.transform.scale(self.crearAnimacion(32*12, 0, 32, 32), escala))
        self.image = self.animacionArriba[0]
        self.velocidadActualX = 0
        self.velocidadActualY = 0

        self.rect = pygame.Rect(x, y, tamanio/4, tamanio/4)

        self.sonidoMorir = pygame.mixer.Sound("./Recursos/Sonidos/DestruirEnemigo.ogg")
        self.sonidoArmadura = pygame.mixer.Sound("./Recursos/Sonidos/Armadura.ogg")
        self.sonidoDestruirBloque = pygame.mixer.Sound("./Recursos/Sonidos/DestruirPared.ogg")

        self.sonidoArmadura.set_volume(0.5)
        self.sonidoMorir.set_volume(0.5)
        self.sonidoDestruirBloque.set_volume(0.5)
        
        if(self.bando == Bando.Aliado):
            pygame.mixer.Sound("./Recursos/Sonidos/Disparo.ogg").play()

## Metodo para que la bala actualice su estado
#\details La bala se actualiza de acuerdo a la direccion que tome y la velocidad que tenga fijada
#\param recibe grupos como parametros para poder pasarlos a al metodo calcularColisiones
#\return No retorna
    def update(self, grupoBloques, grupoJugador, grupoEnemigos, grupoBalas, grupoMedallas):
        """Método para actualizar el estado de la entidad proyectil"""

        super().update()        

        if(self.direccion == Direccion.Abajo):
            self.image = self.animacionAbajo[self.imagenAnimacion]
            self.velocidadActualY = 20

        elif(self.direccion == Direccion.Derecha):
            self.image = self.animacionDerecha[self.imagenAnimacion]
            self.velocidadActualX = 20

        elif(self.direccion == Direccion.Arriba):
            self.image = self.animacionArriba[self.imagenAnimacion]
            self.velocidadActualY = -20

        elif(self.direccion == Direccion.Izquierda):
            self.image = self.animacionIzquierda[self.imagenAnimacion]
            self.velocidadActualX = -20
            
        self.rect.x += self.velocidadActualX
        self.rect.y += self.velocidadActualY

        self.calcularColisiones(grupoBloques, grupoJugador, grupoEnemigos, grupoBalas, grupoMedallas)

## Metodo para determinar si existen choques entre elementos de distintos grupos 
#\details El metodo invoca a otros metodos que sirven especificamente para casos especificos
#\param grupos de objetos
#\return No retorna
    def calcularColisiones(self, grupoBloques, grupoJugador, grupoEnemigos, grupoBalas, grupoMedallas):
        """"""
        colisionBloques     = pygame.sprite.spritecollide(self, grupoBloques, False, pygame.sprite.collide_rect)
        colisionMedallas    = pygame.sprite.spritecollide(self, grupoMedallas, False, pygame.sprite.collide_rect)
        colisionJugador     = pygame.sprite.spritecollide(self, grupoJugador, False, pygame.sprite.collide_rect)
        colisionEnemigos    = pygame.sprite.spritecollide(self, grupoEnemigos, False, pygame.sprite.collide_rect)
        colisionBalas       = pygame.sprite.spritecollide(self, grupoBalas, False, pygame.sprite.collide_rect)

        if(not self.destruida):
            if colisionBloques:
                self.colisionarBloques(colisionBloques)

            if colisionMedallas:
                self.colisionarMedallas(colisionMedallas)

            if colisionJugador:
                self.colisionarTanques(colisionJugador, grupoJugador)

            if colisionEnemigos:
                self.colisionarTanques(colisionEnemigos, grupoJugador)

            if colisionBalas:
                self.colisionarBalas(colisionBalas)

## Metodo para activar reacciones en los bloques afectados por una colisión 
#\details -
#\param listaColision
#\return No retorna
    def colisionarBloques(self, listaColision):
        """Método para detectar las colisiones de balas con bloques"""

        for entidad in listaColision:
            if not isinstance(entidad, BloqueAgua):
                self.image = self.animacionExplosion[0]
                self.destruida = True

                if isinstance(entidad, BloqueLadrillo) or  isinstance(entidad, BloqueMetalico):
                    entidad.vidas -= self.ataque

                    if entidad.vidas <= 0:
                        self.sonidoDestruirBloque.play()
                        entidad.destruido = True
                        entidad.kill()

## Metodo para activar reacciones en medallas afectados por una colisión 
#\details -
#\param listaColision
#\return No retorna
    def colisionarMedallas(self, listaColision):
            """Método para detectar las colisiones de balas con medallas"""

            for entidad in listaColision:
                if entidad.bando == Bando.Aliado and entidad.bando != self.bando:
                    self.sonidoMorir.play()
                    entidad.image = entidad.crearAnimacion(32*12, 32*0, 32, 32)
                    entidad.destruida = True

## Metodo para activar reacciones en tanques afectados por una colisión 
#\details -
#\param listaColision, grupoJugador
#\return No retorna
    def colisionarTanques(self, listaColision, grupoJugador):
        """Método para detectar las colisiones de balas con tanques"""

        puntos = 0
        for entidad in listaColision:
            if( self.bando != entidad.bando and entidad.vivo and not self.destruida):
                self.destruida = True
                if entidad.armadura <= 0:
                    self.sonidoMorir.play()
                    entidad.vivo = False
                    if(entidad.bando == Bando.Aliado):
                        entidad.vidas  -= self.ataque
                    if self.bando == Bando.Aliado:
                        if entidad.tipoTanqueActual == 1:
                            puntos += 100
                        elif entidad.tipoTanqueActual == 2:
                            puntos += 200
                        elif entidad.tipoTanqueActual == 3:
                            puntos += 300
                        elif entidad.tipoTanqueActual == 4:
                            puntos += 400
                else:
                    self.sonidoArmadura.play()
                    self.image = self.animacionExplosion[0]
                    entidad.armadura -= self.ataque
        for jugador in grupoJugador:
            jugador.puntuacion += puntos

## Metodo para activar reacciones en balas afectados por una colisión 
#\details -
#\param listaColision
#\return No retorna
    def colisionarBalas(self, listaColision):
        """Método para detectar las colisiones de balas con balas"""

        for entidad in listaColision:
            if entidad.bando != self.bando:
                self.sonidoArmadura.play()
                self.image = self.animacionExplosion[0]
                self.destruida = True
                entidad.destruida = True
