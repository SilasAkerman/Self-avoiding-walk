import pygame
import sys
import random

class Walker:
    allOptions = [
        (1, 0),
        (-1, 0),
        (0, 1),
        (0, -1)
    ]
    def create_grid(self, spacing, win):
        self.spacing = spacing
        self.rows = win.get_height()//spacing
        self.cols = win.get_width()//spacing
        self.grid = [[False for _ in range(self.cols)] for _ in range(self.rows)]

    def run(self, win, fps, spacing):
        self.create_grid(spacing, win)
        self.Clock = pygame.time.Clock()
        self.points = []
        self.stop = False
        self.one_step = False
        self.grid_display = False

        return self.evaluate(random.randint(0, self.rows-1), random.randint(0, self.cols-1), fps, win)
        # return self.evaluate(0, 0, fps, win)

    def evaluate(self, row, col, fps, win):
        self.Clock.tick(fps)
        self.display(win)
        self.check_events()

        if self.done() or self.one_step:
            self.paus()

        if self.stop:
            return False

        if self.is_available(row, col):
            self.walk_space(row, col)
            allOptions = self.allOptions.copy()

            random.shuffle(allOptions)

            for option in allOptions:
                self.evaluate(row+option[0], col+option[1], fps, win)
            self.undo_walk_space(row, col)
        
        return not self.stop
        


    def walk_space(self, row, col):
        self.grid[row][col] = True
        self.points.append((row, col))

    def undo_walk_space(self, row, col):
        self.grid[row][col] = False
        self.points.pop()

    def is_available(self, row, col):
        if row >= self.rows or row < 0 or col >= self.cols or col < 0:
            return False
        return not self.grid[row][col]


    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.paus()
                if event.key == pygame.K_BACKSPACE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_r:
                    self.stop = True
                if event.key == pygame.K_g:
                    self.grid_display = not self.grid_display

    def paus(self):
        paus = True
        self.one_step = False
        while paus:
            self.Clock.tick(10)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        paus = False
                    if event.key == pygame.K_BACKSPACE:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_c:
                        self.one_step = True
                        paus = False
                    if event.key == pygame.K_r:
                        self.stop = True
                        paus = False
        
    def done(self):
        for row in self.grid:
            for spot in row:
                if not spot:
                    return False
        return True


    def display(self, win):
        win.fill((0, 0, 0))
        if self.grid_display:
            self.display_grid(win)
        self.display_points(win)
        pygame.display.update()

    def display_grid(self, win):
        for col in range(self.cols + 1):
            pygame.draw.line(win, (100, 100, 100), (col*self.spacing, 0), (col*self.spacing, win.get_height()), int(self.spacing*0.1))
        for row in range(self.rows + 1):
            pygame.draw.line(win, (100, 100, 100), (0, row*self.spacing), (win.get_width(), row*self.spacing), int(self.spacing*0.1))

    def display_points(self, win):
        if len(self.points) > 1:
            point_cords = tuple(map(lambda point: (point[1]*self.spacing + self.spacing/2, point[0]*self.spacing + self.spacing/2), self.points))
            pygame.draw.lines(win, (255, 255, 255), False, point_cords, int(self.spacing*0.2))
        if len(self.points) > 0:
            pygame.draw.circle(win, (255, 255, 255), (int(self.points[-1][1]*self.spacing + self.spacing/2), int(self.points[-1][0]*self.spacing + self.spacing/2)), int(self.spacing*0.4))