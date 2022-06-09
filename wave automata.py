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
            increment = 0.1 #makes random pixels turning into two teams happen faster or slower
            for neighbour in neighbours:
                cell_neighbour_diff = abs(cell - grid[neighbour])
                neighbour_value = grid[neighbour]
                if cell_neighbour_diff > 0.6:
                    eaters += 1
                    eater = neighbour_value
                elif cell_neighbour_diff > 0.5:
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
cell_neighbour_average = (cell_above + cell_below + cell_left + cell_right) / divisor
if cell < cell_neighbour_average:
    cell += .3
else:
    cell -= .1"""











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












def update_grid2(grid, x):
    grid_dimensions = grid.shape[:2]
    #grid_shuffled = list(zip(, grid))
    #shuffle(grid_shuffled)
    row_numbers = [idx for idx in range(grid_dimensions[0])]
    column_numbers = [idx1 for idx1 in range(grid_dimensions[1])]
    shuffle(row_numbers)
    
    for row_number in row_numbers:
        shuffle(column_numbers)
        
        #row_shuffled = list(zip([idx for idx in range(grid_dimensions[1])], row))
        #shuffle(row_shuffled)
        """row_unshuffled = enumerate(row)
        if randint(0,4) != 0:
            row_chosen = row_shuffled
        else:
            row_chosen = row_unshuffled"""
            
        for column_number in column_numbers:
            #if randint(0,25000) == 0:
            #    grid[row_number, column_number:randint(0,99-column_number)] = (grid[row_number, column_number][0],0)
            cell_above = 0
            cell_below = 0
            cell_left = 0
            cell_right = 0

            """if row_number == 0:
                cell_above = (row_number, column_number)
                friends -= 1
            else:"""
            cell_above = (row_number - 1, column_number) #negatives wraparound anyway
            """if column_number == 0:
                cell_left = (row_number, column_number)
                friends -= 1
            else:"""
            cell_left = (row_number, column_number - 1)

            if column_number != grid_dimensions[1] - 1: #if not end of row
                cell_right = (row_number, column_number + 1)
            else:
                cell_right = (row_number, 0)
                """cell_right = (row_number, column_number)
                friends -= 1"""

            if row_number != grid_dimensions[0] - 1: #wraparound only needed for overflow
                cell_below = (row_number + 1, column_number) #addition overflow
            else:
                cell_below = (0, column_number)
                """cell_below = (row_number, column_number)
                friends -= 1"""

            neighbours = [cell_above, cell_below, cell_left, cell_right]
            shuffle(neighbours)

            friends = 0
            cell_colour, cell_age = grid[row_number, column_number] #col and row number were backwards, cool y=x reflect wave pattern tho
            enemy_pos = (row_number, column_number)
            for neighbour_pos in neighbours:
                #neighbour = choice(neighbours)
                #cell_neighbour_diff = abs(cell - grid[neighbour])
                neighbour_colour, neighbour_age = grid[neighbour_pos]
                if cell_colour == neighbour_colour:#cell_neighbour_diff == 0:
                    friends += 1
                else:#if cell_neighbour_diff < 0.3 or cell_neighbour_diff > 0.8:
                    enemy_pos = neighbour_pos

            enemy_colour, enemy_age = grid[enemy_pos]
            if enemy_pos != (row_number, column_number):
                if friends >= 1:# and randint(0,4) != 0:
                    if enemy_age > cell_age: #enemy_age < cell_age creates a cool blood-cell looking pattern
                        if enemy_age - cell_age > 10:
                            enemy_colour = cell_colour
                            enemy_age = cell_age# + 1 #- 2#enemy_age - enemy_age/4
                        else:
                            enemy_colour = cell_colour # i can think of better rulesets now i just need to rewrite this entire block make it variable
                            enemy_age = cell_age - 1# + 1 #- 2#enemy_age - enemy_age/4
                    #elif enemy_age == cell_age:
                     #   enemy_age -= 
                        #enemy_age += 10
                        #cell_age -= 100
                        pass
                        """if randint(0,2)!=0:
                            enemy_colour = cell_colour
                            #cell_age -= 10
                            enemy_age = - enemy_age# - 10#cell_age
                        else:
                            pass
                            #enemy_age -= 30
                            #cell_colour = enemy_colour
                            #cell_age = enemy_age - 10"""

                    #elif randint(0,200000)==0:
                    #    pass
                        #cell_age += 2
                #elif friends < 2 and cell_age > 0:
                #    cell_colour = enemy_colour
                #    cell_age = 0
                elif randint(0,10000)==0:
                    cell_colour = enemy_colour
                    #cell_age = enemy_age - 10
            else: #no enemies
                """young_neighbour = False
                for neighbour_pos in neighbours:
                    neighbour_colour, neighbour_age = grid[neighbour_pos]
                    if abs(cell_age - neighbour_age) > 20: #already a young warrior around
                        young_neighbour = True
                        break
                if not young_neighbour:
                    cell_age -= 21"""
                #cell_age += 1

            if enemy_age != 200:
                enemy_age += 1
                    
            if cell_age != 200:
                cell_age += 1

            if cell_age<0:
                cell_age=0
            if enemy_age<0:
                enemy_age=0
                
            grid[row_number, column_number] = (cell_colour, cell_age)
            grid[enemy_pos] = (enemy_colour, enemy_age)
            
def generate_canvas2(grid, grid_dimensions):
    size = 1
    canvas = full([size*grid_dimensions[0],size*grid_dimensions[1], 4], [0,0,0,0])
    for row_no, row in enumerate(grid):
        for pixel_no, pixel in enumerate(row):
            colour, age = pixel
            canvas[(size*row_no):(size + size*row_no), (size*pixel_no):(size + size*pixel_no)] = [0, 0, colour*255, 255-age]
    return canvas

def main2():
    grid_dimensions=(80,80)
    #grid = rand(*grid_dimensions)
    grid = asarray([(rand(), 0) for _ in range(grid_dimensions[0]*grid_dimensions[1])])
    grid = grid.reshape(grid_dimensions[0],grid_dimensions[1],2)
    #grid = full((*grid_dimensions, 2), )
        
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    im = ax.imshow(generate_canvas2(grid, grid_dimensions), animated=True)
    x=0
    def update_image(image):
        update_grid2(grid, x)#randomise=1)
        canvas = generate_canvas2(grid, grid_dimensions)
        im.set_array(canvas)

    ani = animation.FuncAnimation(fig, update_image, interval=4)
    plt.show()#block = False)

if __name__=="__main__":
    from time import sleep
    if bool(input("Nothing for mode 0, anything for mode 1\nEnter input: ")):
        sleep(5)
        main()
    else:
        sleep(5)
        main1()

#this code is ungodly amounts of messy because its just freeflow building stuff, still I'll make it cleaner next time...
