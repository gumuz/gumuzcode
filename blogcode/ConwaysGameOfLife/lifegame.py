# 2006 Guyon Moree ( http://gumuz.looze.net/ )

# python implementation of Conway's game of life using pygame ( http://www.pygame.org )

# controls:
#   space       = start/stop evolution
#   +/-         = faster/slower evolution
#   r           = seed the grid random
#   c           = clear grid
#   mouseclick  = paint cell

import sys, pygame
import random, time



pygame.init()

size = width, height = 800, 600
black = 0, 0, 0
blocksize = 20


screen = pygame.display.set_mode(size)

def startagegrid(grid):
    agegrid = []
    for r in grid:
        row = []
        for c in r:
            row.append(0)
        agegrid.append(row)
    return agegrid


def startgrid(rnd=False):
    """ generate emtpy or randomly filled grid """
    grid = []
    for y in range(height/blocksize):
        row = []
        for x in range(width/blocksize):
            if rnd:
                row.append(random.choice([0,1]))
            else:
                row.append(0)
        grid.append(row)
    return grid

def getneighbours(grid, x,y):
    """ find all 8 possible neigbours """
    offsets = ((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1))
    count = 0
    for a,b in offsets:
        ny,nx = (y+a)%len(grid), (x+b)%len(grid[y])
        count += grid[ny][nx]
    return count

def evolvegrid(grid, agegrid=None):
    """ evolve grid to next generation """
    dupe = []
    for row in grid:
        dupe.append(row[:])
    for y in range(height/blocksize):
        for x in range(width/blocksize):
            pop = grid[y][x]
            neighbours = getneighbours(grid, x, y)
            # next step?
            if pop:
                if neighbours < 2 or neighbours > 3:
                    dupe[y][x] = 0
            else:
                if neighbours == 3:
                    dupe[y][x] = 1
            if agegrid:
                if pop and dupe[y][x] and agegrid[y][x] < 250:
                    agegrid[y][x] += 15
                elif not dupe[y][x]:
                    agegrid[y][x] = 0
    return dupe

def paintgrid(surface, grid, agegrid=None):
    """ paint grid to screen """
    for y in range(height/blocksize):
        for x in range(width/blocksize):
            if grid[y][x]:
                if agegrid:
                    color = (255-agegrid[y][x],255-agegrid[y][x],255)
                else:
                    color = (255,255,255)
                surface.fill(color, pygame.Rect((x*blocksize,y*blocksize), (blocksize, blocksize)))

def paintcell(grid, pos, brush):
    """ paint a cell in the gid """
    x,y = pos
    grid[y/blocksize][x/blocksize] = brush
    return grid

# init the grid
grid = startgrid()
agegrid = startagegrid(grid)

# init some vars
evolve = False
mousedown = False
interval = 0
brush = 1
step = False

# eps (evolutions per second)
ecount = 0
etime = time.time()


# main loop
while 1:
    for event in pygame.event.get():
        """ handle events """
        # escape
        if event.type == pygame.QUIT: sys.exit()

        # space play/pause
        if event.type == pygame.KEYDOWN and event.key == 32:
             evolve = not evolve
        # step 1 generation
        if event.type == pygame.KEYDOWN and event.key == 115:
             step = True

        # randomise/reset grid
        if event.type == pygame.KEYDOWN and event.key == 114:
            grid = startgrid(True)
        if event.type == pygame.KEYDOWN and event.key == 99:
             grid = startgrid()

        # speed control
        if event.type == pygame.KEYDOWN and event.key == 270:
            if interval > 0: interval -= .1
            if interval < 0: interval = 0
        if event.type == pygame.KEYDOWN and event.key == 269:
            interval += .1

        # mouse paint
        if event.type == pygame.MOUSEBUTTONDOWN:
             mousedown = True
             x,y = event.pos
             brush = not grid[y/blocksize][x/blocksize]
             grid = paintcell(grid, event.pos, brush)

        if event.type == pygame.MOUSEBUTTONUP:
             mousedown = False
        if event.type == pygame.MOUSEMOTION and mousedown:
             grid = paintcell(grid, event.pos, brush)


    # reset screen 
    screen.fill(black)
    # paint the grid
    paintgrid(screen, grid, agegrid)
    # if not paused or 'step' was pressed and no mousedown, evolve the grid
    if (evolve or step) and not mousedown:
        grid = evolvegrid(grid, agegrid)
        ecount += 1
        if (time.time() - etime) > 1.0:
            print "eps", ecount
            etime = time.time()
            ecount = 0

        time.sleep(interval)
        step = False
    # display to screen
    pygame.display.flip()