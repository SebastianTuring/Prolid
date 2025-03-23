from Population import *
from biome import *
from FirstLayer import *
from custom import *

def main():
    grid = biomeMapFull()
    seeMap(grid, "Map.jpg")
    
    
    #Map = grid.copy
    GameStart(grid)
    seeMap(grid, "MapPops.jpg")

    applyChanges(grid)
    seeMap(grid, "MapPops2.jpg")
    

if __name__ == '__main__':
    main()
