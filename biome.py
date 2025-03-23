import random
import numpy as np
import math
from PIL import Image, ImageDraw
from collections import Counter

warmG = ['desert', 'waste']
coldG = ['Cplains', 'rocky', 'Cforest','tundra', 'Iforest', 'Imountain', 'swamp']
tempG = ['plains', 'forest', 'sabana']
groups = [coldG, tempG, warmG]

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

def biomeMap(water=[0.9, 0.1]):
    '''
    This function creates a 4x4 grid where every element is either land or sea with a 10% chance of being land
    '''
    # Set up the grid, we start with it being 4x4
    rows, cols = 4, 4
    grid = [[random.choices(['sea', 'land'], water)[0] for _ in range(cols)] for _ in range(rows)]

    # Return the grid for further processing
    return np.array(grid)

def count_land_neighbors(arr, x, y):
    '''
    This functions counts how many elements around an element are land
    '''
    rows, cols = arr.shape
    neighbors = [
        (x - 1, y), (x + 1, y),  # Up, Down
        (x, y - 1), (x, y + 1),  # Left, Right
        (x - 1, y - 1), (x - 1, y + 1),  # Top-left, Top-right
        (x + 1, y - 1), (x + 1, y + 1)   # Bottom-left, Bottom-right
    ]
    return sum(1 for nx, ny in neighbors if 0 <= nx < rows and 0 <= ny < cols and arr[nx, ny] == 'land')

def biomeMapEnhance(grid, prob_island=0.20, prob_flood=0.1):
    """
    Enhances a biome map using stochastic cellular automata rules.

    Takes as arguments a grid and the probability of an island and the probability of flood, and returns the enhanced and scaled grid
    """
    # Convert grid to numpy array
    grid_array = np.array(grid, dtype='<U11')

    # Scale the grid to double its size by repeating rows and columns
    scaled_grid = np.repeat(np.repeat(grid_array, 2, axis=0), 2, axis=1)

    # Apply cellular automata rules
    updated_grid = scaled_grid.copy()
    rows, cols = scaled_grid.shape
    for i in range(rows):
        for j in range(cols):
            land_neighbors = count_land_neighbors(scaled_grid, i, j)
            if scaled_grid[i, j] == 'sea' and land_neighbors > 0:
                # Stochastic transition from sea to land (An Island formed)
                if random.random() < prob_island:
                    updated_grid[i, j] = 'land'
            elif scaled_grid[i, j] == 'land':
                # Stochastic transition from land to sea (There was a flood)
                if random.random() < prob_flood:
                    updated_grid[i, j] = 'sea'

    return updated_grid

def biomeMapAdd(grid, prob_island=0.33, prob_flood=0.1):
    """
    Has a 33% chance by default of adding an island and a 10% chance of flooding one.

    Does the same as biomeMapEnhance without increasing the size of the grid and with different default values
    """
    # Convert grid to numpy array
    scaled_grid = np.array(grid, dtype='<U11')

    # Apply cellular automata rules
    updated_grid = scaled_grid.copy()
    rows, cols = scaled_grid.shape
    for i in range(rows):
        for j in range(cols):
            land_neighbors = count_land_neighbors(scaled_grid, i, j)
            if scaled_grid[i, j] == 'sea' and land_neighbors > 0:
                # Stochastic transition from sea to land
                if random.random() < prob_island:
                    updated_grid[i, j] = 'land'
            elif scaled_grid[i, j] == 'land':
                # Stochastic transition from land to sea
                if random.random() < prob_flood:
                    updated_grid[i, j] = 'sea'

    return updated_grid

def is_surrounded_by_sea(arr, x, y):
    '''
    This helper function checks if there is sea above, bellow, left and right from an element
    '''
    rows, cols = arr.shape
    neighbors = [
        (x - 1, y),  # Up
        (x + 1, y),  # Down
        (x, y - 1),  # Left
        (x, y + 1)   # Right
    ]
    return all(0 <= nx < rows and 0 <= ny < cols and arr[nx, ny] == 'sea' for nx, ny in neighbors)

def biomeMapDry(grid, prob_island=0.5, prob_flood=0, prob_islandSurge=0.5):
    """
    This function is used to increase the proportion of land. Works similar to biomeMapAdd with the probability for an island being 50% 
    and the probability of flood being 0. It also has a 50% chance or turning any sea element surrounded by sea to land
    """
    # Convert grid to numpy array
    scaled_grid = np.array(grid, dtype='<U11')

    # Apply cellular automata rules
    updated_grid = scaled_grid.copy()
    rows, cols = scaled_grid.shape
    for i in range(rows):
        for j in range(cols):
            if scaled_grid[i, j] == 'sea':
                if is_surrounded_by_sea(scaled_grid, i, j):
                    # Fully surrounded sea cell has a 50% chance to become land
                    if random.random() < prob_islandSurge:
                        updated_grid[i, j] = 'land'
                else:
                    # Stochastic transition from sea to land based on land neighbors
                    land_neighbors = count_land_neighbors(scaled_grid, i, j)
                    if land_neighbors > 0 and random.random() < prob_island:
                        updated_grid[i, j] = 'land'
            elif scaled_grid[i, j] == 'land':
                # Stochastic transition from land to sea
                if random.random() < prob_flood:
                    updated_grid[i, j] = 'sea'

    return updated_grid

def biomeMapTemp(grid):
    '''
    This function turns every land element into either warm (66%), cold(17%) or ice(17%)
    '''
    scaled_grid = np.array(grid, dtype='<U11')

    # Apply cellular automata rules
    updated_grid = scaled_grid.copy()
    rows, cols = scaled_grid.shape
    for i in range(rows):
        for j in range(cols):
            if scaled_grid[i, j] == 'land':
                if random.random() < 0.36:
                    updated_grid[i, j] = 'warm'
                elif random.random() < 0.67:
                    updated_grid[i, j] = 'cold'
                else:
                    updated_grid[i, j] = 'ice'
                

    return updated_grid

def has_neighbor(arr, x, y, target_values):
    '''
    This helper function checks wether the neighbours of an element are within the 
    target values which is an argument the function takes
    '''
    rows, cols = arr.shape
    neighbors = [
        (x - 1, y),  # Up
        (x + 1, y),  # Down
        (x, y - 1),  # Left
        (x, y + 1)   # Right
    ]
    return any(0 <= nx < rows and 0 <= ny < cols and arr[nx, ny] in target_values for nx, ny in neighbors)

def biomeMapCool(grid):
    '''
    This function checks if a warm element is adjacent to a cold or ice element and turns it into temp
    '''
    # Convert grid to numpy array 
    scaled_grid = np.array(grid, dtype='<U11')
    # Apply cellular automata rules
    updated_grid = scaled_grid.copy()
    rows, cols = scaled_grid.shape
    for i in range(rows):
        for j in range(cols):
            if scaled_grid[i, j] == 'warm':
                # Check if "warm" has "cold" or "ice" neighbors
                if has_neighbor(scaled_grid, i, j, {'cold', 'ice'}):
                    updated_grid[i, j] = 'temp'
    return updated_grid

def biomeMapWarm(grid):
    '''
    This function checks if an ice element is adjacent to a warm or temp element and turns it into cold
    '''
    # Convert grid to numpy array 
    scaled_grid = np.array(grid, dtype='<U11')
    # Apply cellular automata rules
    updated_grid = scaled_grid.copy()
    rows, cols = scaled_grid.shape
    for i in range(rows):
        for j in range(cols):
            if scaled_grid[i, j] == 'ice':
                if has_neighbor(scaled_grid, i, j, {'warm', 'temp'}):
                    updated_grid[i, j] = 'cold'

    return updated_grid

def biomeMapEnhance2(grid, prob_island=0.25, prob_flood=0): 
    """
    Does the same as biomeMapEnhance but it is adapted to work with the new elements instead of just land and sea
    """
    # Convert grid to numpy array
    grid_array = np.array(grid, dtype='<U11')

    # Double the grid size by repeating rows and columns
    scaled_grid = np.repeat(np.repeat(grid_array, 2, axis=0), 2, axis=1)

    # Apply cellular automata rules
    updated_grid = scaled_grid.copy()
    rows, cols = scaled_grid.shape
    new_elements = {'warm', 'ice', 'cold', 'temp'}
    
    # Helper function to find nearest non-sea element
    def find_nearest_non_sea(arr, x, y):
        for distance in range(1, max(rows, cols)):
            neighbors = [
                (x - distance, y), (x + distance, y),  # Vertical
                (x, y - distance), (x, y + distance)   # Horizontal
            ]
            for nx, ny in neighbors:
                if 0 <= nx < rows and 0 <= ny < cols and arr[nx, ny] != 'sea':
                    return nx, ny
        return None

    for i in range(rows):
        for j in range(cols):
            if scaled_grid[i, j] == 'sea':
                # Try to add an island
                nearest = find_nearest_non_sea(scaled_grid, i, j)
                if nearest and random.random() < prob_island:
                    nearest_value = scaled_grid[nearest]  # Value of the nearest cell
                    updated_grid[i, j] = nearest_value  # Use nearest cell's value for the new cell
                    nx, ny = nearest
                    # Add an adjacent cell with the same or another value
                    possible_neighbors = [
                        (i - 1, j), (i + 1, j),  # Vertical
                        (i, j - 1), (i, j + 1)   # Horizontal
                    ]
                    for px, py in possible_neighbors:
                        if 0 <= px < rows and 0 <= py < cols and updated_grid[px, py] == 'sea':
                            updated_grid[px, py] = random.choice(list(new_elements))
                            break
            elif scaled_grid[i, j] in new_elements:
                # Stochastic transition from new elements to sea
                if random.random() < prob_flood:
                    updated_grid[i, j] = 'sea'

    return updated_grid

def biomeMapZone(grid):
    '''
    This function turns every temperature element into a valid zone
    '''
    scaled_grid = np.array(grid, dtype='<U11')

    # Apply cellular automata rules
    updated_grid = scaled_grid.copy()
    rows, cols = scaled_grid.shape
    for i in range(rows):
        for j in range(cols):
            if scaled_grid[i, j] == 'warm':
                updated_grid[i, j] = 'desert'
            if scaled_grid[i, j] == 'ice':
                updated_grid[i, j] = 'tundra'
            if scaled_grid[i, j] == 'cold':
                if random.random() < 0.4:
                    updated_grid[i, j] = 'rocky'
                else:
                    updated_grid[i, j] = 'Cplains'
            if scaled_grid[i, j] == 'temp':
                if random.random() < 0.7:
                    updated_grid[i, j] = 'plains'
                else:
                    updated_grid[i, j] = 'sabana'

    return updated_grid

def is_surrounded_by_X(arr, x, y, Element):
    '''
    This helper function checks if there is X surrounding the element
    '''
    rows, cols = arr.shape
    neighbors = [
        (x - 1, y), (x + 1, y),  # Up, Down
        (x, y - 1), (x, y + 1),  # Left, Right
        (x - 1, y - 1), (x - 1, y + 1),  # Top-left, Top-right
        (x + 1, y - 1), (x + 1, y + 1)   # Bottom-left, Bottom-right
    ]
    return all(0 <= nx < rows and 0 <= ny < cols and arr[nx, ny] == Element for nx, ny in neighbors)

def biomeMapZone1(grid):
    '''
    This function turns every temperature element into a valid zone
    '''
    scaled_grid = np.array(grid, dtype='<U11')

    # Apply cellular automata rules
    updated_grid = scaled_grid.copy()
    rows, cols = scaled_grid.shape
    for i in range(rows):
        for j in range(cols):
            if scaled_grid[i, j] == 'desert' and is_surrounded_by_X(scaled_grid, i, j, 'desert'):
                if random.random() < 0.4375:
                    updated_grid[i, j] = 'desert'
                elif random.random() < 0.75:
                    updated_grid[i, j] = 'desert'
                elif random.random() < 0.95:
                    updated_grid[i, j] = 'desert'
                else:
                    updated_grid[i, j] = 'waste'
            
            if scaled_grid[i, j] == 'tundra' and is_surrounded_by_X(scaled_grid, i, j, 'tundra'):
                if random.random() < 0.7125:
                    updated_grid[i, j] = 'Iforest'
                elif random.random() < 0.3125:
                    updated_grid[i, j] = 'tundra'
                elif random.random() < 0.95:
                    updated_grid[i, j] = 'Imountain'
                else:
                    updated_grid[i, j] = 'Imountain'
            
            if scaled_grid[i, j] == 'Cplains' and is_surrounded_by_X(scaled_grid, i, j, 'Cplains'):
                if random.random() < 0.375:
                    updated_grid[i, j] = 'Cplains'
                elif random.random() < 0.8125:
                    updated_grid[i, j] = 'Cforest'
                elif random.random() < 0.7875:
                    updated_grid[i, j] = 'swamp'
                else:
                    updated_grid[i, j] = 'swamp'
                    
            
            if scaled_grid[i, j] == 'plains' and is_surrounded_by_X(scaled_grid, i, j, 'plains'):
                if random.random() < 0.375:
                    updated_grid[i, j] = 'plains'
                elif random.random() < 0.375:
                    updated_grid[i, j] = 'forest'
                else:
                    updated_grid[i, j] = 'forest'

    return updated_grid

def get_neighbors(grid, x, y):
    """Get the neighbors of a cell at (x, y) in the grid."""
    neighbors = []
    rows, cols = grid.shape
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < rows and 0 <= ny < cols:
            neighbors.append(grid[nx, ny])
    return neighbors

def biomeMapSmooth(grid, iterations=1):
    """
    Smooths a biome map using a cellular automata approach.

    Args:
        grid (numpy.ndarray): 2D array where each cell contains a string representing the biome.
        iterations (int): Number of smoothing iterations to perform.

    Returns:
        numpy.ndarray: Smoothed biome map.
    """
    for _ in range(iterations):
        new_grid = grid.copy()
        rows, cols = grid.shape
        for x in range(rows):
            for y in range(cols):
                neighbors = get_neighbors(grid, x, y)
                if neighbors:
                    # Find the most common biome among neighbors
                    biome_counts = Counter(neighbors)
                    most_common_biome = biome_counts.most_common(1)[0][0]
                    new_grid[x, y] = most_common_biome
        grid = new_grid
    return grid

def biomeMapRivers(grid, groups):
    """
    Creates thin rivers in the biome map where different biome groups meet.
    
    Args:
        grid (numpy.ndarray): 2D array where each cell contains a string representing the biome.
        groups (list of list): List of biome groups. Each group is a list of biome names.
        
    Returns:
        numpy.ndarray: Updated grid with 'river' cells where biomes from different groups meet.
    """
    # Flatten groups into a dictionary for quick lookup
    biome_to_group = {}
    for i, group in enumerate(groups):
        for biome in group:
            biome_to_group[biome] = i

    def is_different_group(biome1, biome2):
        """Check if two biomes belong to different groups."""
        return biome_to_group.get(biome1, -1) != biome_to_group.get(biome2, -1)
    
    rows, cols = grid.shape
    new_grid = grid.copy()
    
    for x in range(rows):
        for y in range(cols):
            current_biome = grid[x, y]
            if current_biome == 'sea':  # Skip cells that are 'sea'
                continue
            
            neighbors = get_neighbors(grid, x, y)
            different_group_found = False
            
            for neighbor in neighbors:
                if neighbor == 'sea':  # Skip changes if neighbor is 'sea'
                    continue
                if is_different_group(current_biome, neighbor):
                    different_group_found = True
                    break
            
            # Change to 'river' only if a different group neighbor is found
            if different_group_found:
                new_grid[x, y] = 'river'
    
    return new_grid

def biomeMapEdge(grid):
    """
    Adjusts the biome map edges:
    - Converts land (except 'desert') in contact with 'sea' or 'lake' into 'coast'.
    - Converts 'sea' in contact with 'river' into 'lake'.
    
    Args:
        grid (numpy.ndarray): 2D array where each cell contains a string representing the biome.
        
    Returns:
        numpy.ndarray: Updated grid with modified edges.
    """
    land_types = {'plains', 'Cplains', 'forest', 'Iforest', 'rocky'}  # Exclude 'desert'
    rows, cols = grid.shape
    new_grid = grid.copy()
    
    for x in range(rows):
        for y in range(cols):
            current_biome = grid[x, y]
            
            # Skip if current cell is desert or already coast/lake
            if current_biome == 'desert':
                continue
            
            neighbors = get_neighbors(grid, x, y)
            
            # Convert land in contact with sea/lake into coast
            if current_biome in land_types and any(n in {'sea', 'lake'} for n in neighbors):
                new_grid[x, y] = 'coast'
            
            # Convert sea in contact with river into lake
            elif current_biome == 'sea' and any(n == 'river' for n in neighbors):
                new_grid[x, y] = 'lake'
    
    return new_grid

def seeMap(grid, name):
    """
    Visualizes a grid map using Pillow in a Jupyter Notebook.
    """
    # Determine grid size
    x = int(math.sqrt(grid.size))
    rows, cols = x, x
    
    # Define cell size
    cell_size = 25
    img_width = cols * cell_size
    img_height = rows * cell_size

    # Create a blank image
    img = Image.new("RGB", (img_width, img_height), "white")
    draw = ImageDraw.Draw(img)

    # Draw the grid
    for i in range(rows):
        for j in range(cols):
            color = color_map.get(grid[i, j], (255, 255, 255))  # Default to white
            top_left = (j * cell_size, i * cell_size)
            bottom_right = ((j + 1) * cell_size, (i + 1) * cell_size)
            draw.rectangle([top_left, bottom_right], fill=color)

    # Display the image 
    img.show()
    img.save(name)

class biome:
    def __init__(self, biomeID, temp, colour, survival):
        self.biomeID = biomeID
        self.temp = temp
        self.colour = colour
        self.survival = survival