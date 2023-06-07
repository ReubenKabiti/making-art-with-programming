import pygame
import math
import sys
import os

class Ball:

    def __init__(self, x, y, start_time, path, color):
        self.x = x
        self.y = y
        self.color = color
        self.start_time = start_time
        self.v = 0
        self.g = 980
        self.r = 8
        self.sound = pygame.mixer.Sound(path)

    def draw(self):
        pygame.draw.circle(pygame.display.get_surface(), self.color, pygame.math.Vector2(self.x, self.y), self.r)

class Game:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("bouncyness")

        self.balls = []

        self.create_balls(20)
        self.clock = pygame.time.Clock()
        self.delta = 0
        self.time = 0


    def create_balls(self, n):
        count_sounds = 0
        for _, _, files in os.walk("data"):
            for file in files:
                if file.endswith(".wav"):
                    count_sounds +=1


        padding = 40

        spacing = (pygame.display.get_surface().get_rect().width - 2*padding)/n
        x = 2*padding
        y = pygame.display.get_surface().get_rect().height*0.1

        start_time = 1
        end_time = 10

        start_g = 0.4
        end_g = 1

        start_color = pygame.math.Vector3(200, 100, 0)
        end_color = pygame.math.Vector3(100, 200, 100)
        for i in range(n):
            t = i/n
            time = pygame.math.lerp(start_time, end_time, t)
            path = os.path.join("data", str(i%count_sounds)+".wav")
            color = start_color.lerp(end_color, t)
            self.balls.append(Ball(x, y, time, path, color))
            g = pygame.math.lerp(start_g, end_g, t)
            self.balls[-1].g *= g
            x += spacing

    def update_balls(self):

        highest = pygame.display.get_surface().get_rect().height*0.1
        for ball in self.balls:
            if ball.start_time > self.time:
                continue
            h = pygame.display.get_surface().get_rect().height
            if ball.y >= h - ball.r:
                ball.y = h - ball.r
                ball.v = -math.fabs(ball.v)
                ball.sound.play(maxtime=1000)
            elif ball.y <= highest:
                ball.y = highest
                ball.v = math.fabs(ball.v)

            ball.v += ball.g*self.delta
            ball.y += ball.v*self.delta

    def draw_balls(self):
        for ball in self.balls:
            ball.draw()

    def run(self):

        while True:
            self.screen.fill((0, 0, 0))
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.update_balls()
            self.draw_balls()
            pygame.display.update()
            self.clock.tick()
            fps = self.clock.get_fps()
            if fps:
                self.delta = 1/fps
            self.time += self.delta
Game().run()
