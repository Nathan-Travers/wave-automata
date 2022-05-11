from numpy import array, arange, reshape, full
from numpy.random import rand
from random import randint, shuffle
grid_dimensions=(30,30)
#grid = arange(0,1,.1)[:9].reshape([3,3])
grid = rand(*grid_dimensions)

def update_grid(randomise=False):
    for row_number, row in enumerate(grid):
        for column_number, cell in enumerate(row):
            cell_above = 0
            cell_below = 0
            cell_left = 0
            cell_right = 0
            divisor = 0
            if row_number != 0:
                cell_above = grid[row_number - 1, column_number]
                divisor += 1
            else:
                cell_above = grid[-1, column_number]
                divisor +=1
            if row_number != grid_dimensions[0] - 1:
                cell_below = grid[row_number + 1, column_number]
                divisor += 1
            else:
                cell_below = grid[0, column_number]
                divisor += 1
            if column_number != 0:
                cell_left = row[column_number - 1]
                divisor += 1
            else:
                cell_left = row[-1]
                divisor = 1
            if column_number != grid_dimensions[1] - 1:
                cell_right = row[column_number + 1]
                divisor += 1
            else:
                cell_right = row[0]
                divisor += 1
                
            """cell_neighbour_average = (cell_above + cell_below + cell_left + cell_right) / divisor
            if cell < cell_neighbour_average:
                cell += .3
            else:
                cell -= .1"""

            neighbours = [cell_above, cell_below, cell_left, cell_right]
            shuffle(neighbours)
            lowers = 0
            highers = 0
            eaters = 0
            eater = 0
            for neighbour in neighbours:
                if abs(cell - neighbour) > 0.6:
                    eaters += 1
                    eater = neighbour
                else:
                    boost = .1 * (randint(0,10)==0)
                    if cell < neighbour:
                        cell -= 0.01 + boost
                    elif cell > neighbour:
                        cell += 0.01 + boost
            if eaters > 1:
                cell = eater
            elif eaters == 1 and randint(0,1000) == 0:
                cell = eater
            '''
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
"""                cell_neighbour_diff = abs(cell - neighbour)
                if cell_neighbour_diff < 0.3:
                    friends += 1
                elif cell_neighbour_diff > 0.6:
                    enemies += 1
            if friends > enemies:"""    '''
                
            if randint(0,1000) == 0 and randomise:
                if randint(0,1) == 0:
                    #cell += .2
                    cell = 1
                else:
                    cell = 0
                    #cell -= .2
            if cell > 1:
                cell = 1
            elif cell < 0:
                cell = 0
            grid[row_number, column_number] = cell
            
def generate_canvas():
    canvas = full([30*grid_dimensions[0],30*grid_dimensions[1]], 0)
    for row_no, row in enumerate(grid):
        for pixel_no, pixel in enumerate(row):
            canvas[(30*row_no):(30 + 30*row_no), (30*pixel_no):(30 + 30*pixel_no)] = pixel*255
    return canvas

import matplotlib.pyplot as plt
from matplotlib import animation
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
im = ax.imshow(generate_canvas(), animated=True)

def update_image(image):
    update_grid()#randomise=1)
    canvas = generate_canvas()
    im.set_array(canvas)

ani = animation.FuncAnimation(fig, update_image, interval=10)
plt.show(block = False)


"""
from numpy import full, concatenate
corner1 = full((30,30),[0,0,0])
corner2 = full((30,30),[0,0,0])

fin = Image.fromarray(concatenate((corner1, corner2)))
fin.show()
"""
            


"""
class point():
    def __init__(self):
        self."""


#Other rulesets
'''
                    """if randint(0,5000) == 0:
                        if randint(0,1) == 0:
                            cell -= 0.1
                        else:
                            cell += 0.1"""
                """if cell > neighbour:
                    lowers += 1
                elif cell < neighbour:
                    highers += 1
                else:
                    pass"""
                """if randint(0,1) == 0:
                        highers += 1
                    else:
                        lower += 1
                    #pass"""
                """cell += .001
                    else:
                        cell -= .001"""
                #    cell += .001
            """if lowers > highers:
                cell -= 0.3
            elif lowers < highers:
                cell += 0.3"""
'''
