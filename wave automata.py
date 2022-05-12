from numpy import array, arange, reshape, full
from numpy.random import rand
from random import randint, shuffle
import matplotlib.pyplot as plt
from matplotlib import animation
    
def update_grid(grid, randomise=False, diagonal_interaction=False):
    grid_dimensions = grid.shape
    for row_number, row in enumerate(grid):
        for column_number, cell in enumerate(row):
            cell_above = 0
            cell_below = 0
            cell_left = 0
            cell_right = 0

            cell_above = (row_number - 1, column_number) #negatives wraparound anyway
            cell_upleft = (row_number - 1, column_number - 1)
            cell_left = (row_number, column_number - 1)

            col = column_number #column_number + 1 used below so use this if to fix it
            if column_number != grid_dimensions[1] - 1: #if not end of row
                cell_right = (row_number, column_number + 1)
                cell_upright = (row_number - 1, column_number + 1)
            else:
                cell_right = (row_number, 0)
                cell_upright = (row_number - 1, 0)
                col = -1

            if row_number != grid_dimensions[0] - 1: #wraparound only needed for overflow
                cell_below = (row_number + 1, column_number) #addition overflow
                cell_downleft = (row_number + 1, column_number - 1)
                cell_downright = (row_number + 1, col + 1) #col, -1+1=0 if wraparound
            else:
                cell_below = (0, column_number)
                cell_downleft = (0, column_number - 1)
                cell_downright = (0, col + 1)

            neighbours = [cell_above, cell_below, cell_left, cell_right]
            if diagonal_interaction:
                neighbours.extend([cell_upleft, cell_downleft, cell_upright, cell_downright])
            shuffle(neighbours)
            
            eaters_needed = 2
            eaters = 0
            eater = 0
            increment = 0.05 #makes random pixels turning into two teams happen faster or slower
            for neighbour in neighbours:
                cell_neighbour_diff = abs(cell - grid[neighbour])
                neighbour_value = grid[neighbour]
                if cell_neighbour_diff > 0.5:
                    eaters += 1 #If over difference threshold (0.5), neighbour becomes hostile
                    eater = neighbour_value 
                else:
                    boost = 0.2 * (randint(0,100)==0) #if surrounded by equal high and low values
                    #the cell doesnt go up or down so we must randomly boost out
                    if cell < neighbour_value: #if difference not big enough, get bigger
                        cell -= increment + boost
                    elif cell > neighbour_value:
                        cell += increment + boost
                        
            if eaters >= eaters_needed: #if surrounded by more hostile cells than threshold eaters_needed, get eaten
                cell = eater
            elif eaters == eaters_needed-1 and randint(0,100) == 0: #sometimes it goes stale like if
                #(eaters_needed = 2) meets a straight edge, only one ever touches, so must randomly eat out
                cell = eater
                
            if cell > 1:
                cell = 1
            elif cell < 0:
                cell = 0
            grid[row_number, column_number] = cell
            
def generate_canvas(grid, grid_dimensions):
    canvas = full([30*grid_dimensions[0],30*grid_dimensions[1]], 0)
    for row_no, row in enumerate(grid):
        for pixel_no, pixel in enumerate(row):
            canvas[(30*row_no):(30 + 30*row_no), (30*pixel_no):(30 + 30*pixel_no)] = pixel*255
    return canvas

def main():
    grid_dimensions=(50,50)
    grid = rand(*grid_dimensions)
        
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    im = ax.imshow(generate_canvas(grid, grid_dimensions), animated=True)
    def update_image(image):
        update_grid(grid)#randomise=1)
        canvas = generate_canvas(grid, grid_dimensions)
        im.set_array(canvas)

    ani = animation.FuncAnimation(fig, update_image, interval=4)
    plt.show()#block = False

"""
class point():
    def __init__(self):
        self."""

"""
cell_neighbour_average = (cell_above + cell_below + cell_left + cell_right) / divisor
if cell < cell_neighbour_average:
    cell += .3
else:
    cell -= .1"""

#Other rulesets
"""
if randint(0,5000) == 0:
    if randint(0,1) == 0:
        cell -= 0.1
    else:
        cell += 0.1"""

"""
if cell > neighbour:
    lowers += 1
elif cell < neighbour:
    highers += 1
else:
    pass"""

"""
if randint(0,1) == 0:
    highers += 1
else:
    lower += 1"""

"""if lowers > highers:
    cell -= 0.3
elif lowers < highers:
        cell += 0.3"""

"""if cell < neighbour:
    cell += .001
else:
    cell -= .001"""

#print(abs(cell-neighbour))
"""if abs(cell - neighbour) > 0.01:
    if cell < neighbour:
        cell += .002
    else:
        cell -= .001"""

#so the name of this app was after quantum fields idea with a wave being a plane, trying to make that in an cellular automata
#now its kinda a wave function thing, obviously, but I didn't think that until having wavefunction collapse come to mind
#from some youtube video, googled this https://robertheaton.com/2018/12/17/wavefunction-collapse-algorithm/
#not really a wavefunction collapse but ideas

#main()

#(type,life,attack)
def battle(grid):
    grid_dimensions = grid.shape #same code as above
    for row_number, row in enumerate(grid):
        for column_number, cell in enumerate(row):
            cell = deepcopy(cell)
            cell_above = 0
            cell_below = 0
            cell_left = 0
            cell_right = 0

            cell_above = (row_number - 1, column_number) #negatives wraparound anyway
            cell_left = (row_number, column_number - 1)
            
            if row_number != grid_dimensions[0] - 1: #if not end of row
                cell_below = (row_number + 1, column_number) 
            else:
                cell_below = (0, column_number)

            if column_number != grid_dimensions[1] - 1: #wraparound only needed for overflow
                cell_right = (row_number, column_number + 1) #addition overflow
            else:
                cell_right = (row_number, 0)

            neighbours = [cell_above, cell_below, cell_left, cell_right]
            neighbour_pos = choice(neighbours)
            neighbour = deepcopy(grid[neighbour_pos])
            if cell[0] == 1 or cell[0] == 2:
                if neighbour[0] == 0 and (randint(0,4)==0):
                    if cell[3] == 0:
                        neighbour, cell = cell, neighbour
                    else:
                        if cell[1] > 1:
                            neighbour = (cell[0], cell[1]-1, 10, 1)
                            cell[1] = 1
                        else:
                            neighbour,cell = cell,neighbour
                elif (neighbour[0] == 1 and cell[0] == 2) or (neighbour[0] == 2 and cell[0] == 1):
                    neighbour[1] -= randint(0, cell[2])
                    cell[1] -= randint(0, neighbour[2])
                    if neighbour[1] < 0:
                        neighbour = (0,0,0,0)
                    if cell[1] < 0:
                        cell = (0,0,0,0)
                        #neighbour, cell = cell, neighbour
                elif (neighbour[0] == 1 and cell[0] == 1) or (neighbour[0] == 2 and cell[0] == 2):
                    cell[3] = 1
                    neighbour[3] = 1

            grid[row_number, column_number] = cell
            grid[neighbour_pos] = neighbour
            #row[column_number] = cell
            #row[neighbour_pos[1]] = neighbour
            #print(row_number, column_number, neighbour_pos)

    return grid

def generate_canvas1(grid, grid_dimensions):
    canvas = full([30*grid_dimensions[0],30*grid_dimensions[1], 3], [0,0,0])
    for row_no, row in enumerate(grid):
        for pixel_no, pixel in enumerate(row):
            pixel_value = [0,0,0]
            if pixel[0] == 1:
                pixel_value = [pixel[1]*25,0,0]
            elif pixel[0] == 2:
                pixel_value = [0,pixel[1]*25,0]
            canvas[(30*row_no):(30 + 30*row_no), (30*pixel_no):(30 + 30*pixel_no)] = pixel_value
    return canvas

from random import choice
from copy import deepcopy
from numpy import asarray
from numpy.random import shuffle
def main1():
    multiplier = 2
    grid_dimensions=(10*multiplier,10*multiplier)
    grid = asarray([*[(0,0,0,0)]*50*multiplier*2,*[(1,10,2,0)]*25*multiplier*2,*[(2,10,2,0)]*25*multiplier*2], dtype=object)
    shuffle(grid)
    grid = grid.reshape(10*multiplier,10*multiplier,4)
        
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    im = ax.imshow(generate_canvas1(grid, grid_dimensions), animated=True)
    def update_image(image):
        battle(grid)#randomise=1)
        canvas = generate_canvas1(grid, grid_dimensions)
        im.set_array(canvas)

    ani = animation.FuncAnimation(fig, update_image, interval=4)
    plt.show()#block = False

if __name__=="__main__":
    if bool(input("Nothing for mode 0, anything for mode 1\nEnter input: ")):
        main1()
    else:
        main()
