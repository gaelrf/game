import sys
from random import randint

import pygame

from enemigoA import EnemigoA
from jugador import Jugador


class Juego:
    def __init__(self):
        icono_jugador = Jugador((ancho_pantalla/2,alto_pantalla),alto_pantalla,5)
        self.jugador = pygame.sprite.GroupSingle(icono_jugador)

        self.enemigos = pygame.sprite.Group()
        self.alien_lasers = pygame.sprite.Group()
        self.preparar_enemigos(filas=1, columnas=8)
        self.alien_direccion = 1


    def preparar_enemigos(self, filas, columnas, distancia_x=60, distancia_y=48, x_offset=70, y_offset=100):
        for indice_filas, fila in enumerate(range(filas)):
            for indice_columnas, columna in enumerate(range(columnas)):
                x = indice_columnas * distancia_x + x_offset
                y = indice_filas * distancia_y + y_offset

                icono_enemigo = EnemigoA('red', x, y)
                self.enemigos.add(icono_enemigo)

    def fin(self):
        if not self.enemigos.sprites():
            pygame.quit()

    def fin_pantalla_enemigos(self):
        todos_enemigos = self.enemigos.sprites()
        for enemigo in todos_enemigos:
            if enemigo.rect.right >= ancho_pantalla:
                self.alien_direccion = -1
                self.enemigo_abajo(2)
            elif enemigo.rect.left <= 0:
                self.alien_direccion = 1
                self.enemigo_abajo(2)

    def enemigo_abajo(self, distance):
        if self.enemigos:
            for enemigo in self.enemigos.sprites():
                enemigo.rect.y += distance

    def correr(self):
        self.jugador.update()
        self.enemigos.update(self.alien_direccion)
        self.fin_pantalla_enemigos()
        self.jugador.draw(screen)
        self.enemigos.draw(screen)


class Control:

    def __init__(self):
        self.tv = pygame.image.load('graphics/tv.png').convert_alpha()
        self.tv = pygame.transform.scale(self.tv, (ancho_pantalla, alto_pantalla))

    def create_crt_lines(self):
        alti_linea = 3
        line_amount = int(ancho_pantalla / alti_linea)
        for linea in range(line_amount):
            y_pos = linea * alti_linea
            pygame.draw.line(self.tv, 'black', (0, y_pos), (ancho_pantalla, y_pos), 1)

    def draw(self):
        self.tv.set_alpha(randint(75, 90))
        self.create_crt_lines()
        screen.blit(self.tv, (0, 0))


if __name__ == '__main__':
    pygame.init()
    ancho_pantalla = 600
    alto_pantalla = 600
    screen = pygame.display.set_mode((ancho_pantalla, alto_pantalla))
    reloj = pygame.time.Clock()
    juego = Juego()
    controlador = Control()

    ALIENLASER = pygame.USEREVENT + 1
    pygame.time.set_timer(ALIENLASER, 800)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((30, 30, 30))
        juego.correr()
        # crt.draw()

        pygame.display.flip()
        reloj.tick(60)
