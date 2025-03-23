from biome import *

def biomeMapFull():
    grid = biomeMap()
    #seeMap(grid)
    grid = biomeMapEnhance(grid)
    #seeMap(grid)
    grid = biomeMapAdd(grid)
    #seeMap(grid)
    grid = biomeMapEnhance(grid)
    #seeMap(grid)
    grid = biomeMapAdd(grid)
    #seeMap(grid)
    grid = biomeMapAdd(grid)
    #seeMap(grid)
    grid = biomeMapAdd(grid)
    #seeMap(grid)
    grid = biomeMapDry(grid)
    #seeMap(grid)
    grid = biomeMapAdd(grid)
    #seeMap(grid)
    grid = biomeMapTemp(grid)
    #seeMap(grid)
    grid = biomeMapCool(grid)
    #seeMap(grid)
    grid = biomeMapWarm(grid)
    #seeMap(grid)
    grid = biomeMapEnhance2(grid)
    #seeMap(grid)
    grid = biomeMapEnhance2(grid)
    #seeMap(grid)
    grid = biomeMapCool(grid)
    #seeMap(grid)
    grid = biomeMapWarm(grid)
    
    grid = biomeMapZone(grid)
    
    grid = biomeMapZone1(grid)
    
    grid = biomeMapEnhance2(grid, 0, 0)
    
    grid = biomeMapZone1(grid)
    
    grid = biomeMapSmooth(grid, iterations=2)
    
    grid = biomeMapZone1(grid)
    
    grid = biomeMapEnhance2(grid, 0, 0)
    
    grid = biomeMapSmooth(grid, iterations=3)
    
    grid = biomeMapRivers(grid, groups)
    
    grid = biomeMapEdge(grid)
    
    return grid
