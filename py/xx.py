import pygame
from pygame.locals import *

class Car:
    def __init__(self, posx, posy):
        self._pos_x = posx;
        self._pos_y = posy;

    def m_y(self, delta):
        self._pos_y += delta

    def m_x(self, delta):
        self._pos_x += delta

    def car_square(self):
        return (self._pos_x - 5, self._pos_y - 5, self._pos_x + 5, self._pos_y + 5)

class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 1280, 800
        self._sq = Car(15, 15)

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True

    def on_key_down(self):
        delta = 0.1
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            self._sq.m_x(-delta)

        if keys[K_RIGHT]:
            self._sq.m_x(+delta)

        if keys[K_UP]:
            self._sq.m_y(-delta)

        if keys[K_DOWN]:
            self._sq.m_y(+delta)

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self):
        self.on_key_down()

    def on_render(self):
        self._display_surf.fill((0, 0, 0))
        pygame.draw.rect(self._display_surf, (255, 0, 0), self._sq.car_square(), 2)
        pygame.display.flip()
        pass

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while (self._running):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()

        self.on_cleanup()


if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()
