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

LEVEL_12 = {
    'name': 'Back to the Basics',
    'description': 'It\'s not that bad',
    'data': [
        [1,1,1,1,1,1,1],
        [1,0,0,0,0,0,1],
        [1,1,1,0,1,1,1],
        [1,0,0,0,0,0,1],
        [1,0,1,1,1,0,1],
        [1,0,0,0,0,0,0],
        [1,1,1,1,1,1,3]
    ],
    'start_pos': (1,1),
    'start_dir': 3,  # Facing right
    'par': 4,
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
        [1,0,1,0,0,0,1],
        [1,0,1,1,1,1,1]
    ],
    'start_pos': (6,1),
    'start_dir': 0,
    'par': 3,
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
    'par': 4,
    'difficulty': 'Medium'
}

LEVEL_4 = {
    'name': 'Red Key Challenge',
    'description': 'Collect the red key to pass through the red gate',
    'data': [
        [1,0,0,0,0,0,3],  # Row 0: wall, empty, empty, empty, empty, empty, red gate
        [1,1,1,1,1,7,1],  # Row 1: all walls
        [6,0,0,0,1,0,1],  # Row 2: wall, red key, wall, empty, wall, empty, wall
        [1,1,0,0,0,0,1],  # Row 3: wall, empty, wall, empty, wall, empty, wall
        [0,0,0,1,1,1,1],  # Row 4: wall, empty, wall, empty, wall, empty, wall
        [0,1,1,1,1,1,1]   # Row 5: empty (bot start), wall, empty path, wall
    ],
    'start_pos': (5,0),
    'start_dir': 3,  # Facing right
    'par': 4,
    'difficulty': 'Medium'
}

LEVEL_5 = {
    'name': 'The Rocks',
    'description': 'Find your way through the rough terrain',
    'data': [
        [1,1,0,0,0,1,1,1,1,1],
        [1,1,0,1,0,0,1,1,1,1],
        [1,0,0,1,1,0,0,1,1,1],
        [1,0,0,1,1,1,0,0,1,1],
        [1,0,1,1,1,1,1,0,0,1],
        [1,0,1,1,1,1,1,1,0,1],
        [0,0,1,1,1,1,1,1,0,0],
        [1,0,0,1,1,1,1,1,1,0],
        [1,0,0,1,1,3,1,0,0,0],
        [1,1,0,0,1,0,0,0,1,1]
    ],
    'start_pos': (9,3),
    'start_dir': 1,
    'par': 4,
    'difficulty': 'Medium'
}


LEVEL_6 = {
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
    'par': 6,
    'difficulty': 'Medium'
}

LEVEL_7 = {
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
    'par': 4,
    'difficulty': 'Medium'
}

LEVEL_8 = {
    'name': 'Key Hunt',
    'description': 'Collect the yellow key to open the gate',
    'data': [
        [1,1,1,1,1,1,1,1,1],
        [1,0,0,0,1,0,0,4,1],
        [1,0,1,0,1,0,1,0,1],
        [1,0,1,0,0,0,1,0,1],
        [1,0,1,1,1,1,1,0,1],
        [1,0,0,0,0,0,0,0,1],
        [1,5,1,1,1,1,1,0,1],
        [1,3,5,0,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,1]
    ],
    'start_pos': (1,1),
    'start_dir': 3,
    'par': 6,
    'difficulty': 'Hard'
}

LEVEL_9 = {
    'name': 'Double Keys',
    'description': 'Navigate through multiple locked gates',
    'data': [
        [1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,0,0,0,7,0,1],
        [1,0,1,0,1,0,1,0,1,0,1],
        [1,0,1,4,1,0,1,0,1,3,1],
        [1,0,1,1,1,0,1,0,1,1,1],
        [1,0,0,0,0,0,1,0,0,0,1],
        [1,0,1,1,1,1,1,0,1,1,1],
        [1,0,0,0,0,0,0,0,5,6,1],
        [1,1,1,1,1,1,1,1,1,1,1]
    ],
    'start_pos': (7,1),
    'start_dir': 0,
    'par': 18,
    'difficulty': 'Hard'
}

LEVEL_10 = {
    'name': 'Key Mania',
    'description': 'Collect all the keys without touching the zappy walls',
    'data': [
        [2,2,10,0,0,0,0 ,2,12,0],
        [2,0, 0,2,2,2,0 ,2, 2,0],
        [0,0, 0,0,2,0,0 ,0, 0,0],
        [0,0, 2,0,0,0,2 ,2, 0,2],
        [0,2, 2,0,2,2,2 ,0, 0,2],
        [0,0, 0,0,0,2,0 ,0, 0,2],
        [0,2, 0,2,8,0,0 ,2, 0,2],
        [0,0, 0,2,2,0,0 ,2, 6,2],
        [0,2, 0,2,0,0,2 ,2, 2,2],
        [0,0, 0,2,0,0,11,13,7,9]
    ],
    'start_pos':(9,0),
    'start_dir': 3,
    'par': 25,
    'difficulty': 'Expert'
}

LEVEL_11 = {
    'name': 'The Challenge',
    'description': 'The ultimate test of your skills',
    'data': [
        [1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,0,1,0,0,0,0,0,1],
        [1,0,2,2,2,0,1,0,2,2,2,0,1],
        [1,0,0,8,2,0,9,0,2,6,0,0,1],
        [1,0,2,2,2,0,1,0,2,2,2,0,1],
        [1,0,0,0,0,0,1,0,0,0,0,0,1],
        [1,1,1,5,1,1,1,1,1,7,1,1,1],
        [1,0,0,0,0,0,1,0,0,0,0,0,1],
        [1,0,2,0,2,0,1,0,2,2,2,0,1],
        [1,0,2,4,2,0,1,0,2,3,2,0,1],
        [1,0,2,2,2,0,1,0,2,0,2,0,1],
        [1,0,0,0,0,0,1,0,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1]
    ],
    'start_pos': (11,1),
    'start_dir': 0,
    'par': 25,
    'difficulty': 'Expert'
}


LEVEL_13 = {
    'name': 'Key Sequence',
    'description': 'Collect keys in the right order while avoiding zappy walls',
    'data': [
        [1,1,1,1,1,1,1,1,1],
        [1,0,2,0,2,0,2,0,1],
        [1,0,0,0,0,0,0,0,1],
        [1,2,0,4,0,6,0,2,1],
        [1,0,0,0,0,0,0,0,1],
        [1,0,2,0,2,0,2,0,1],
        [1,0,0,0,0,0,0,0,1],
        [1,2,0,0,0,2,2,2,1],
        [0,0,0,0,0,0,7,5,3]
    ],
    'start_pos': (8,0),
    'start_dir': 3,  # Facing right
    'par': 16,
    'difficulty': 'Medium'
}

LEVEL_14 = {
    'name': 'Algorithm Mastery',
    'description': 'Use loops and conditions to navigate complex key-gate combinations',
    'data': [
        [1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,0,0,0,0,6,1],
        [1,0,2,2,2,2,2,2,2,0,1],
        [1,0,2,0,0,0,0,4,2,0,1],
        [1,0,2,5,2,2,2,0,2,0,1],
        [1,0,2,11,0,3,2,0,2,0,1],
        [1,0,2,5,2,2,2,0,2,0,1],
        [1,0,2,0,0,0,7,10,2,0,1],
        [1,0,2,2,2,2,9,2,2,0,1],
        [1,8,0,0,0,0,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1,1]
    ],
    'start_pos': (9,5),
    'start_dir': 0,  # Facing up
    'par': 20,
    'difficulty': 'Hard'
}

LEVEL_15 = {
    'name': 'Zappy Navigation',
    'description': 'Navigate through zappy walls to collect multiple keys',
    'data': [
        [1,1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,2,2,0,0,0,0,2,2,0,1],
        [1,0,2,4,2,0,0,2,6,2,0,1],
        [1,0,0,9,2,0,0,2,9,0,0,1],
        [1,0,2,0,2,0,0,2,0,2,0,1],
        [1,0,2,0,0,0,0,0,0,2,0,1],
        [1,0,2,2,0,0,0,0,2,2,0,1],
        [1,0,0,0,0,5,7,0,0,0,0,1],
        [1,2,2,0,2,0,10,2,0,2,2,1],
        [1,9,0,0,2,0,0,2,0,11,3,1],
        [1,1,1,1,1,1,1,1,1,1,1,1]
    ],
    'start_pos': (2,10),
    'start_dir': 0,  # Facing up
    'par': 22,
    'difficulty': 'Hard'
}


# ============================================================================
# LEVEL REGISTRY
# ============================================================================

ALL_LEVELS = [
    LEVEL_1,
    LEVEL_12,
    LEVEL_2,
    LEVEL_3,
    LEVEL_4,
    LEVEL_5,
    LEVEL_6,
    LEVEL_7,
    LEVEL_8,
    LEVEL_9,
    LEVEL_10,
    LEVEL_13,
    LEVEL_14,
    LEVEL_15,
    LEVEL_11,
]

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_level(level_number):
    """
    Get a specific level by number (1-indexed)
    
    Args:
        level_number (int): The level number (1-16)
    
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

