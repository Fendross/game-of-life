'''
GAME OF LIFE, a basic implementation using pygame and numpy.
RULES: - an alive cell will remain alive if it has either 2 or 3 neighbors, and it will die if it has less than 2 or more than 3.
       - a dead cell will remain dead if it has less or more than 3 neighbors, else it will come to life.

@author: Fendross, github page: https://github.com/Fendross
'''

import time
import pygame as pg
import numpy as np

# Game Parameters
WIDTH = 80
HEIGHT = 60
SCALE_FACTOR = 10 # to account for the 2D array initialisation
BG_COLOR = (20, 20, 20) # black-ish
GRID_COLOR = (20, 200, 20) # bright green
DYING_CELL_COLOR = (170, 170, 170) # gray
ALIVE_CELL_COLOR = (255, 255, 255) # white
CELL_SIZE = 10 # TODO: game not optimal for other values, fix it
SLEEP_TIME = 0.01


def apply_rules(current_cell_value, number_of_alive_neighbors, is_simulation_active):
    '''
    @notice: applies the rules of the Game of Life to the cell, based on the current state of the simulation toggle
    @param current_cell_value: int, the value of the cell to be considered.
    @param number_of_alive_neighbors: int, the number of alive neighbors the cell has
    @param is_simulation_on: the current state of the simulation toggle.
    @return: (color, updated_cell_value), a tuple containing the color of the cell in the next game iteration and the
                                          corresponding value for the grid.
    '''
    # Get the color of the current cell, and assume the next value of the cell will be zero
    color = BG_COLOR if current_cell_value == 0 else ALIVE_CELL_COLOR
    updated_cell_value = 0

    # If the simulation is active, applies the game rules and changes the color of the cell accordingly
    if is_simulation_active:
        # If the cell is currently 'alive'
        if current_cell_value == 1:
            if number_of_alive_neighbors < 2 or number_of_alive_neighbors > 3:
                color = DYING_CELL_COLOR
            elif 2 <= number_of_alive_neighbors <= 3:
                updated_cell_value = 1
                color = ALIVE_CELL_COLOR
        # If the cell is currently 'dead'
        else:
            if number_of_alive_neighbors == 3:
                updated_cell_value = 1
                color = ALIVE_CELL_COLOR
    # If the simulation is paused, saves the latest configuration of the grid without visualising it
    else:
        # If the cell is currently 'alive'
        if current_cell_value == 1:
            if 2 <= number_of_alive_neighbors <= 3:
                updated_cell_value = 1
        # If the cell is currently 'dead'
        else:
            if number_of_alive_neighbors == 3:
                updated_cell_value = 1
    
    return (color, updated_cell_value)


def update(screen, cells, size, is_simulation_active=False):
    '''
    @notice: the core of the simulation, it updates the state of the cells in the grid by flipping it or maintaining the same, based on
             the Game of Life rules.
             Case alive: if less than 2 or more than 3 alive neighbors, the cell dies. If either 2 or 3 alive neighbors, no change.
             Case dead: if exactly 3 alive neighbors, the cell comes to life.
    
    @param screen: the screen object of pygame.
    @param cells: a 2D numpy array object, used to keep track of the cells state.
    @param size: int, the size of the cells.
    @param is_simulation_active: bool, gives the option to proceed with the simulation or stop it. If not explicit, set to False.
    @return: updated_cells, a 2D array of updated cells.
    '''
    # An array of the same shape of the cells one filled with 0. (float type)
    updated_cells = np.zeros((cells.shape[0], cells.shape[1]))

    # Iterates over every row and col of cells
    for row, col in np.ndindex(cells.shape):
        # Calculates the number of alive neighbor cells and subtract the contribution of the current cell, it doesn't count as a neighbor
        number_of_alive_neighbors = np.sum(cells[row - 1 : row + 2, col - 1 : col + 2]) - cells[row, col]

        # Applies the Game of Life rules, getting the color of the cell and its value in the next iteration of the game
        (color, updated_cells[row, col]) = apply_rules(cells[row, col], number_of_alive_neighbors, is_simulation_active)
        
        # Draws the current cell with the updated color
        pg.draw.rect(screen, color, (col * size, row * size, size - 1, size - 1))

    return updated_cells


def main():
    '''
    @notice: the main game program. It includes the pygame module initialisation and the game loop.
    '''
    # Initialises the pygame window and sets the correct caption
    pg.init()
    screen = pg.display.set_mode((WIDTH*CELL_SIZE, HEIGHT*CELL_SIZE))
    pg.display.set_caption('Game of Life')

    # Initialises the cells 2D array, fills the screen with the GRID_COLOR and shows the initial state of the simulation
    cells = np.zeros(((HEIGHT // SCALE_FACTOR) * CELL_SIZE, (WIDTH // SCALE_FACTOR) * CELL_SIZE))
    screen.fill(GRID_COLOR)
    update(screen, cells, CELL_SIZE)

    # Update the content of the whole screen
    pg.display.flip()
    pg.display.update()

    '''
    A boolean switch: 
        if it's True, then the simulation is running and the rules apply for each iteration
        else, the simulation is paused and none of the rules apply
    '''
    is_simulation_active = False

    while True:
        # Checking for events s.a. quitting or pressing a key
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return
            elif event.type == pg.KEYDOWN:
                # Checks for space bar presses
                if event.key == pg.K_SPACE:
                    # Toggles the simulation switch
                    is_simulation_active = not is_simulation_active

                    # Updates the grid and the screen
                    update(screen, cells, CELL_SIZE)
                    pg.display.update()

            # Activate the cell with a mouse press, by getting the position of the mouse (only if the simulation switch is falsy)
            if pg.mouse.get_pressed()[0] and not is_simulation_active:
                pos = pg.mouse.get_pos()
                cells[pos[1] // CELL_SIZE, pos[0] // CELL_SIZE] = 1
                update(screen, cells, 10)
                pg.display.update()

        # Simulation of the Game of Life (only if the simulation switch is truthy)
        if is_simulation_active:
            cells = update(screen, cells, CELL_SIZE, is_simulation_active)
            pg.display.update()
        
        # Delay for each loop iteration
        time.sleep(SLEEP_TIME)


if __name__ == '__main__':
    main()
