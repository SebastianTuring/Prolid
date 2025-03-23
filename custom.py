from Population import *
from biome import *
from FirstLayer import *

# Map color names to RGB values
color_map = {
    'sea': (0, 0, 255),
    'land': (0, 255, 0),
    'warm': (245, 222, 179),
    'ice': (240, 255, 255),
    'cold': (128, 128, 0),
    'temp': (50, 205, 50),
    'waste': (247,168,89),
    'desert': (245, 222, 179),
    'Iforest': (203,247,206),
    'tundra': (224,255,255),
    'Imountain': (194, 215, 215),
    'Cplains': (176,210,106),
    'Cforest': (85,107,47),
    'swamp': (95,158,160),
    'plains': (124,252,0),
    'forest': (84,168,0),
    'rocky': (162,162,162),
    'lake': (0,77,255),
    'sabana': (210,170,60),
    'river': (0, 154, 255),
    'ruins': (155,155,155),
    'village': (255,255,51),
    'city': (153,0,76),
    'coast': (245, 222, 179),
    'black': (0,0,0),
    'path': (234,210,162)
}

Changes = {"waste": "", "desert": "", "Iforest": "", "tundra": "",
           "Imountain": "", "Cplains": "", "Cforest": "", "swamp": "",
           "plains": "", "forest": "", "rocky": "", "lake": "",
           "sabana": "", "river": "black", "sea": "", "ruins": "",
           "village": "", "city": "", "coast": "", "path": ""}

def applyChanges(grid):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] in Changes:
                grid[i][j] = Changes[grid[i][j]]