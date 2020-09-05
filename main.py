import pygame as pg
import random as rnd
from dataclasses import dataclass

# settings
screenResolution = 500
grid = 9
mines = 10
distance = screenResolution // grid
neighborFields = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

#initialize Screen and PNG's
pg.init()
screen = pg.display.set_mode([screenResolution, screenResolution])
cell_normal = pg.transform.scale(pg.image.load('normal.png'), (distance, distance))
cell_marked = pg.transform.scale(pg.image.load('flagged.png'), (distance, distance))
cell_mine = pg.transform.scale(pg.image.load('bomb.png'), (distance, distance))
cell_selected = []
for n in range(9):
    cell_selected.append(pg.transform.scale(pg.image.load(f'{n}.png'), (distance, distance)))
matrix = []

# Cell Class
@dataclass
class Cell:
    line: int
    column: int
    mine: bool = False
    selected: bool = False
    flagged: bool = False
    minesAround: int = 0

    def show(self):
        pos = (self.column * distance, self.line * distance)
        if self.selected:
            if self.mine:
                screen.blit(cell_mine, pos)
            else:
                screen.blit(cell_selected[self.minesAround], pos)
        else:
            if self.flagged:
                screen.blit(cell_marked, pos)
            else:
                screen.blit(cell_normal, pos)

    def determineMinesAround(self):
        for pos in neighborFields:
            newLine = self.line + pos[0]
            newColumn = self.column + pos[1]
            if newLine >= 0 and newLine < grid and newColumn >= 0 and newColumn < grid:
                if matrix[newLine * grid + newColumn].mine:
                    self.minesAround += 1


# Uncovers all cells without adjacent mines
def floodFill(line, column):
    for pos in neighborFields:
        newLine = line + pos[0]
        newColumn = column + pos[1]
        if newLine >= 0 and newLine < grid and newColumn >= 0 and newColumn < grid:
            cell = matrix[newLine * grid + newColumn]
            if cell.minesAround == 0 and not cell.selected:
                cell.selected = True
                floodFill(newLine, newColumn)
            else:
                cell.selected = True


for n in range(grid * grid):
    matrix.append(Cell(n // grid, n % grid))

while mines > 0:
    x = rnd.randrange(grid * grid)
    if not matrix[x].mine:
        matrix[x].mine = True
        mines -= 1

for object in matrix:
    object.determineMinesAround()

game = True
while game:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game = False
        if event.type == pg.MOUSEBUTTONDOWN:
            mouseX, mouseY = pg.mouse.get_pos()
            column = mouseX // distance
            line = mouseY // distance
            i = line * grid + column
            cell = matrix[i]
            if pg.mouse.get_pressed()[2]:
                cell.flagged = not cell.flagged
            if pg.mouse.get_pressed()[0]:
                cell.selected = True
                if cell.minesAround == 0 and not cell.mine:
                    floodFill(line, column)
                if cell.mine:
                    for object in matrix:
                        object.selected = True

    for object in matrix:
        object.show()
    pg.display.flip()

pg.quit()
