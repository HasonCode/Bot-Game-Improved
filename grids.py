"""
Grid definitions for all levels in the Bot Game

Tile types:
0 = Blank tile (walkable)
1 = Basic wall (impassable)
2 = Zappy wall (respawns bot)
3 = End/finish line
4 = Yellow key
5 = Yellow gate
6 = Red key
7 = Red gate
8 = Blue key
9 = Blue gate
10 = Green key
11 = Green gate
12 = Purple key
13 = Purple gate
"""

from python_decoder import Grid

# ============================================================================
# LEVEL DEFINITIONS
# ============================================================================

LEVEL_1 = {
    'name': 'Tutorial: First Steps',
    'description': 'Learn to move forward and turn',
    'data': [
        [1,1,1,1,1],
        [1,0,0,3,1],
        [1,0,1,1,1],
        [1,0,1,1,1],
        [1,0,1,1,1]
    ],
    'start_pos': (4,1),
    'start_dir': 0,
    'par': 3,
    'difficulty': 'Easy'
}

LEVEL_2 = {
    'name': 'The Corner',
    'description': 'Navigate around corners',
    'data': [
        [1,1,1,1,1,1,1],
        [1,0,0,0,0,0,1],
        [1,0,1,1,1,0,1],
        [1,0,1,3,1,0,1],
        [1,0,1,0,1,0,1],
        [1,0,0,0,0,0,1],
        [1,1,1,1,1,1,1]
    ],
    'start_pos': (5,1),
    'start_dir': 0,
    'par': 6,
    'difficulty': 'Easy'
}

LEVEL_3 = {
    'name': 'The Maze',
    'description': 'Find your way through the maze',
    'data': [
        [1,1,1,1,1,1,1,1,1],
        [1,0,0,0,1,0,0,0,1],
        [1,0,1,0,1,0,1,0,1],
        [1,0,1,0,0,0,1,0,1],
        [1,0,1,1,1,1,1,0,1],
        [1,0,0,0,0,0,0,0,1],
        [1,1,1,1,1,0,1,1,1],
        [1,3,0,0,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,1]
    ],
    'start_pos': (1,1),
    'start_dir': 3,
    'par': 10,
    'difficulty': 'Medium'
}

LEVEL_4 = {
    'name': 'Spiral',
    'description': 'Navigate the spiral path',
    'data': [
        [1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,0,0,0,0,0,1],
        [1,0,1,1,1,1,1,1,1,0,1],
        [1,0,1,0,0,0,0,0,1,0,1],
        [1,0,1,0,1,1,1,0,1,0,1],
        [1,0,1,0,0,3,1,0,1,0,1],
        [1,0,1,0,1,1,1,0,1,0,1],
        [1,0,1,0,0,0,0,0,0,0,1],
        [1,0,1,1,1,1,1,1,1,0,1],
        [1,0,0,0,0,0,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1,1]
    ],
    'start_pos': (9,1),
    'start_dir': 0,
    'par': 15,
    'difficulty': 'Medium'
}

LEVEL_5 = {
    'name': 'The Trap',
    'description': 'Avoid the zappy walls!',
    'data': [
        [1,1,1,1,1,1,1],
        [1,0,0,0,0,0,1],
        [1,0,2,2,2,0,1],
        [1,0,2,0,0,0,1],
        [1,0,2,3,2,0,1],
        [1,0,2,2,2,0,1],
        [1,0,0,0,0,0,1],
        [1,1,1,1,1,1,1]
    ],
    'start_pos': (6,3),
    'start_dir': 0,
    'par': 8,
    'difficulty': 'Medium'
}

LEVEL_6 = {
    'name': 'Key Hunt',
    'description': 'Collect the yellow key to open the gate',
    'data': [
        [1,1,1,1,1,1,1,1,1],
        [1,0,0,0,1,0,0,4,1],
        [1,0,1,0,1,0,1,0,1],
        [1,0,1,0,0,0,1,0,1],
        [1,0,1,1,5,1,1,0,1],
        [1,0,0,0,0,0,0,0,1],
        [1,0,1,1,1,1,1,0,1],
        [1,3,0,0,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,1]
    ],
    'start_pos': (1,1),
    'start_dir': 3,
    'par': 12,
    'difficulty': 'Hard'
}

LEVEL_7 = {
    'name': 'Double Keys',
    'description': 'Navigate through multiple locked gates',
    'data': [
        [1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,5,0,0,0,7,0,1],
        [1,0,1,0,1,0,1,0,1,0,1],
        [1,0,1,6,1,0,1,0,1,0,1],
        [1,0,1,1,1,0,1,0,1,3,1],
        [1,0,0,0,0,0,1,0,0,0,1],
        [1,0,1,1,1,1,1,0,1,1,1],
        [1,4,0,0,0,0,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1,1]
    ],
    'start_pos': (7,1),
    'start_dir': 0,
    'par': 18,
    'difficulty': 'Hard'
}

LEVEL_8 = {
    'name': 'The Challenge',
    'description': 'The ultimate test of your skills',
    'data': [
        [1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,0,1,0,0,0,0,0,1],
        [1,0,1,1,1,0,1,0,1,1,1,0,1],
        [1,0,1,8,1,0,0,0,1,6,1,0,1],
        [1,0,1,1,1,0,1,0,1,1,1,0,1],
        [1,0,0,0,0,0,1,0,0,0,0,0,1],
        [1,1,1,5,1,1,1,1,1,7,1,1,1],
        [1,0,0,0,0,0,1,0,0,0,0,0,1],
        [1,0,1,1,1,0,1,0,1,1,1,0,1],
        [1,0,1,4,1,0,0,0,1,3,1,0,1],
        [1,0,1,1,1,0,1,0,1,1,1,0,1],
        [1,0,0,0,0,0,1,0,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1]
    ],
    'start_pos': (11,1),
    'start_dir': 0,
    'par': 25,
    'difficulty': 'Expert'
}

# ============================================================================
# LEVEL REGISTRY
# ============================================================================

ALL_LEVELS = [
    LEVEL_1,
    LEVEL_2,
    LEVEL_3,
    LEVEL_4,
    LEVEL_5,
    LEVEL_6,
    LEVEL_7,
    LEVEL_8
]

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_level(level_number):
    """
    Get a specific level by number (1-indexed)
    
    Args:
        level_number (int): The level number (1-8)
    
    Returns:
        dict: Level configuration dictionary
    """
    if level_number < 1 or level_number > len(ALL_LEVELS):
        raise ValueError(f"Level {level_number} does not exist. Available levels: 1-{len(ALL_LEVELS)}")
    
    return ALL_LEVELS[level_number - 1]

def create_grid(level_number):
    """
    Create a Grid object for a specific level
    
    Args:
        level_number (int): The level number (1-8)
    
    Returns:
        Grid: A Grid object ready for gameplay
    """
    level = get_level(level_number)
    return Grid(
        data=level['data'],
        start_pos=level['start_pos'],
        start_dir=level['start_dir'],
        par=level['par']
    )

def get_level_info(level_number):
    """
    Get information about a level without creating a Grid
    
    Args:
        level_number (int): The level number (1-8)
    
    Returns:
        dict: Level information (name, description, difficulty, par)
    """
    level = get_level(level_number)
    return {
        'number': level_number,
        'name': level['name'],
        'description': level['description'],
        'difficulty': level['difficulty'],
        'par': level['par'],
        'size': f"{len(level['data'])}x{len(level['data'][0])}"
    }

def list_all_levels():
    """
    Get information about all available levels
    
    Returns:
        list: List of level information dictionaries
    """
    return [get_level_info(i + 1) for i in range(len(ALL_LEVELS))]

def get_levels_by_difficulty(difficulty):
    """
    Get all levels of a specific difficulty
    
    Args:
        difficulty (str): 'Easy', 'Medium', 'Hard', or 'Expert'
    
    Returns:
        list: List of level numbers matching the difficulty
    """
    return [i + 1 for i, level in enumerate(ALL_LEVELS) if level['difficulty'] == difficulty]

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("BOT GAME - LEVEL CATALOG")
    print("=" * 60)
    print()
    
    for level_info in list_all_levels():
        print(f"Level {level_info['number']}: {level_info['name']}")
        print(f"  Description: {level_info['description']}")
        print(f"  Difficulty: {level_info['difficulty']}")
        print(f"  Grid Size: {level_info['size']}")
        print(f"  Par: {level_info['par']} commands")
        print()
    
    print("=" * 60)
    print("DIFFICULTY BREAKDOWN")
    print("=" * 60)
    print(f"Easy: {get_levels_by_difficulty('Easy')}")
    print(f"Medium: {get_levels_by_difficulty('Medium')}")
    print(f"Hard: {get_levels_by_difficulty('Hard')}")
    print(f"Expert: {get_levels_by_difficulty('Expert')}")

