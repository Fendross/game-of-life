'''
GAME OF LIFE, a basic implementation using pygame and numpy.

@author: Fendross, github page: https://github.com/Fendross
'''

import time
import pygame as pg
import numpy as np

# Game Parameters
BG_COLOR = (20, 20, 20) # black-ish
GRID_COLOR = (20, 200, 20) # bright green
DEAD_CELL_COLOR = (170, 170, 170) # gray
ALIVE_CELL_COLOR = (255, 255, 255) # white
CELL_SIZE = 10 # TODO: game not optimal for other values, fix it
SLEEP_TIME = 0.01


def update(screen, cells, size, with_progress=False):
    '''
    @notice: the core of the simulation, it updates the state of the cells in the grid by flipping it or maintaining the same, based on
             the Game of Life rules.
             Case alive: if less than 2 or more than 3 alive neighbors, the cell dies. If either 2 or 3 alive neighbors, no change.
             Case dead: if exactly 3 alive neighbors, the cell comes to life.
    
    @param screen: the screen object of pygame.
    @param cells: a 2D numpy array object, used to keep track of the cells state.
    @param size: the size of the cells.
    @param with_progress: gives the option to proceed with the simulation or stop it. If not explicit, set to False.
    @return: a 2D array of updated cells, updated_cells.
    '''
    # An array of shape cells filled with 0.
    updated_cells = np.zeros((cells.shape[0], cells.shape[1]))

    # Iterating over every row and col of cells
    for row, col in np.ndindex(cells.shape):
        # Calculate the number of alive neighbor cells and subtract the contribution of the current cell, it doesn't count as a neighbor
        alive = np.sum(cells[row - 1 : row + 2, col - 1 : col + 2]) - cells[row, col]

        # Get the color of the current cell
        if cells[row, col] == 0:
            color = BG_COLOR
        else:
            color = ALIVE_CELL_COLOR

        # Game of Life rules
        if cells[row, col] == 1:
            if alive < 2 or alive > 3:
                if with_progress:
                    color = DEAD_CELL_COLOR
            elif 2 <= alive <= 3:
                updated_cells[row, col] = 1
                if with_progress:
                    color = ALIVE_CELL_COLOR
        else:
            if alive == 3:
                updated_cells[row, col] = 1
                if with_progress:
                    color = ALIVE_CELL_COLOR
        
        # Draws the current cell with the updated color
        pg.draw.rect(screen, color, (col * size, row * size, size - 1, size - 1))

    return updated_cells


def main():
    '''
    @notice: the main game program. It includes the pygame module initialisation and the game loop.
    '''
    # Initialises the pygame window and sets a caption
    pg.init()
    screen = pg.display.set_mode((80*CELL_SIZE, 60*CELL_SIZE))
    pg.display.set_caption('Game of Life')

    # Initialises the cells 2D array, fills the screen with the GRID_COLOR and shows the initial state of the simulation
    cells = np.zeros((6*CELL_SIZE, 8*CELL_SIZE))
    screen.fill(GRID_COLOR)
    update(screen, cells, CELL_SIZE)

    # Update the content of all the screen
    pg.display.flip()
    pg.display.update()

    is_running = False
    while True:
        # Checking for events s.a. quitting or pressing a key
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return
            elif event.type == pg.KEYDOWN:
                # If space is pressed, reverts the state of the simulation and updates the screen
                if event.key == pg.K_SPACE:
                    is_running = not is_running
                    update(screen, cells, CELL_SIZE)
                    pg.display.update()

            # Activate the cell with a mouse press, by getting the position of the mouse
            # TODO: make it possible to flip an alive cell as well
            if pg.mouse.get_pressed()[0] and not is_running:
                pos = pg.mouse.get_pos()
                cells[pos[1] // CELL_SIZE, pos[0] // 10] = 1
                update(screen, cells, 10)
                pg.display.update()

        # Simulation of the Game of Life
        if is_running:
            cells = update(screen, cells, CELL_SIZE, with_progress=True)
            pg.display.update()
        
        # Delay for each loop iteration
        time.sleep(SLEEP_TIME)


if __name__ == '__main__':
    main()
