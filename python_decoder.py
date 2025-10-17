class WinInterruption(Exception):
    pass

class MovesExceeded(Exception):
    pass

class DeathInterruption(Exception):
    pass

def exec_func(source, globals=None, locals=None):
    try:
        exec(source, globals, locals)
    except WinInterruption:
        pass

class Grid:
    """Data denotes tile types: 0 = blank tile, 1 = basic wall tile, 2 = zappy wall tile, 3 = end
       4 = Yellow key, 5 = Yellow gate, 6 = Red key, 7 = Red gate, 8 = Blue key, 9 = Blue gate,
       10 = Green key, 11 = Green gate, 12 = Purple key, 13 = Purple gate 
    """
    def __init__(self, data, start_pos, start_dir, par):
        self.start_pos = start_pos
        self.rows = len(data)
        self.cols = len(data[0])
        
        # Create a deep copy of data to avoid modifying the original level data
        self.data = [[data[i][j] for j in range(len(data[0]))] for i in range(len(data))]

        
        # Create a backup copy for reset functionality
        self.data_copy = [[data[i][j] for j in range(len(data[0]))] for i in range(len(data))]
        
        self.start_direction = start_dir
        self.par = par
    def get(self, row, col):
        return self.data[row][col]
    def reset(self):
        """Restore grid to original state - all keys and gates are regenerated"""
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                self.data[i][j] = self.data_copy[i][j]

        

class Bot:
    def __init__(self, grid:Grid):
        self.grid = grid
        self.direction = grid.start_direction
        self.start = grid.start_pos
        self.win_state = False
        self.i = grid.start_pos[0]
        self.j = grid.start_pos[1]
        self.alive = True
        self.moves = 0
        self.moves_limit = 10000

        
    def move_backward(self):
        self.moves += 1
        directions = ["up", "left", "down", "right"]
        keys = [4, 6, 8, 10, 12]
        dir = directions[self.direction]
        if dir == "down" and self.alive and not self.win_state:
            if self._can_move_back():
                if self.grid.data[self.i-1][self.j] == 2:
                    self.reset()
                elif self.grid.data[self.i-1][self.j] in keys:
                    self.pick_up(self.grid.data[self.i-1][self.j], (self.i-1, self.j))
                    self.i -= 1
                else:
                    self.i -= 1
        elif dir == "up" and self.alive and not self.win_state:
            if self._can_move_back():
                if self.grid.data[self.i+1][self.j] == 2:
                    self.reset()
                elif self.grid.data[self.i+1][self.j] in keys:
                    self.pick_up(self.grid.data[self.i+1][self.j], (self.i+1, self.j))
                    self.i += 1
                else:
                    self.i += 1
        if dir == "left" and self.alive and not self.win_state:
            if self._can_move_back():
                if self.grid.data[self.i][self.j+1] == 2:
                    self.reset()
                elif self.grid.data[self.i][self.j+1] in keys:
                    self.pick_up(self.grid.data[self.i][self.j+1], (self.i, self.j+1))
                    self.j += 1
                else:
                    self.j+=1
        if dir == "right" and self.alive and not self.win_state:
            if self._can_move_back():
                if self.grid.data[self.i][self.j-1] == 2:
                    self.reset()
                elif self.grid.data[self.i][self.j-1] in keys:
                    self.pick_up(self.grid.data[self.i][self.j-1], (self.i, self.j-1))
                    self.j -= 1
                else:
                    self.j -= 1
        # print(self.__str__())
        self.win_state = self.check_win()
        if (self.win_state):
            raise WinInterruption

    def move_forward(self):
        self.moves += 1
        directions = ["up", "left", "down", "right"]
        keys = [4, 6, 8, 10, 12]
        dir = directions[self.direction]
        if dir == "up" and self.alive and not self.win_state:
            if self._can_move():
                if self.grid.data[self.i-1][self.j] == 2:
                    self.reset()
                elif self.grid.data[self.i-1][self.j] in keys:
                    self.pick_up(self.grid.data[self.i-1][self.j], (self.i-1, self.j))
                    self.i -= 1
                else:
                    self.i -= 1
        elif dir == "down" and self.alive and not self.win_state:
            if self._can_move():
                if self.grid.data[self.i+1][self.j] == 2:
                    self.reset()
                elif self.grid.data[self.i+1][self.j] in keys:
                    self.pick_up(self.grid.data[self.i+1][self.j], (self.i+1, self.j))
                    self.i += 1
                else:
                    self.i += 1
        if dir == "right" and self.alive and not self.win_state:
            if self._can_move():
                if self.grid.data[self.i][self.j+1] == 2:
                    self.reset()
                elif self.grid.data[self.i][self.j+1] in keys:
                    self.pick_up(self.grid.data[self.i][self.j+1], (self.i, self.j+1))
                    self.j += 1
                else:
                    self.j+=1
        if dir == "left" and self.alive and not self.win_state:
            if self._can_move():
                if self.grid.data[self.i][self.j-1] == 2:
                    self.reset()
                elif self.grid.data[self.i][self.j-1] in keys:
                    self.pick_up(self.grid.data[self.i][self.j-1], (self.i, self.j-1))
                    self.j -= 1
                else:
                    self.j -= 1
        self.win_state = self.check_win()
        if (self.win_state):
            raise WinInterruption
    
    def turn_right(self):
        self.moves += 1
        self.direction -= 1
        self.direction %= 4

    def turn_left(self):
        self.moves += 1
        self.direction += 1
        self.direction %= 4
    
    def pick_up(self, key, key_location):
        for i in range(self.grid.rows):
            for j in range(self.grid.cols):
                if self.grid.data[i][j]==key+1:
                    self.grid.data[i][j] = 0
                if i == key_location[0] and j == key_location[1]:
                    self.grid.data[i][j] = 0
        
    def _can_move_back(self, additional_blocks=[]):
        # Safety check: ensure bot position is valid
        if not (0 <= self.i < self.grid.rows and 0 <= self.j < self.grid.cols):
            return False
            
        directions = ["up", "left", "down", "right"]
        dir = directions[self.direction]
        if dir == "down":
            if self.i > 0:
                return self.grid.data[self.i-1][self.j] not in [1, 5, 7, 9, 11, 13] + additional_blocks
        elif dir == "up":
            if self.i < self.grid.rows - 1:  # Fixed: was self.grid.rows
                return self.grid.data[self.i+1][self.j] not in [1, 5, 7, 9, 11, 13] + additional_blocks
        elif dir == "left":
            if self.j < self.grid.cols - 1:  # Fixed: was self.grid.cols
                return self.grid.data[self.i][self.j+1] not in [1, 5, 7, 9, 11, 13] + additional_blocks
        elif dir == "right":
            if self.j > 0:
                return self.grid.data[self.i][self.j-1] not in [1, 5, 7, 9, 11, 13] + additional_blocks
        return False
    
    def can_move_back(self):
        return self._can_move_back([2])

    def can_move(self):
        return self._can_move([2])


    def _can_move(self, additional_blocks=[]):
        # Safety check: ensure bot position is valid
        if not (0 <= self.i < self.grid.rows and 0 <= self.j < self.grid.cols):
            return False
            
        directions = ["up", "left", "down", "right"]
        dir = directions[self.direction]
        if dir == "up":
            if self.i > 0:
                return self.grid.data[self.i-1][self.j] not in [1, 5, 7, 9, 11, 13] + additional_blocks
        elif dir == "down":
            if self.i < self.grid.rows - 1:  # Fixed: was self.grid.rows
                return self.grid.data[self.i+1][self.j] not in [1, 5, 7, 9, 11, 13] + additional_blocks
        elif dir == "right":
            if self.j < self.grid.cols - 1:  # Fixed: was self.grid.cols
                return self.grid.data[self.i][self.j+1] not in [1, 5, 7, 9, 11, 13] + additional_blocks
        elif dir == "left":
            if self.j > 0:
                return self.grid.data[self.i][self.j-1] not in [1, 5, 7, 9, 11, 13] + additional_blocks
        return False

    def check_win(self):
        if self.moves > self.moves_limit:
            raise MovesExceeded("Too many moves taken")
        if self.grid.get(self.i, self.j) == 3:
            return True
        return False


    def reset(self):
        """Reset bot to initial state and restore all keys/gates in the grid"""
        self.i = self.start[0]
        self.j = self.start[1]
        self.direction = self.grid.start_direction
        self.alive = True
        self.win_state = False
        self.moves = 0
        self.grid.reset()  # This restores all keys and gates from data_copy
        raise DeathInterruption("The bot has died")
    
    def __str__(self):
        strong = ""
        emojis = ["⬜","⬛","🟧","🟫", "🟡", "🟨", "🔴", "🟥", "🔵", "🟦", "🟢","🟩", "🟣","🟪"]
        bot_emoji = ["⬆️","⬅️","⬇️","➡️"]
        for i in range(self.grid.rows):
            for j in range(self.grid.cols):
                if i == self.i and j == self.j:
                    # Safety check for direction index
                    if 0 <= self.direction < len(bot_emoji):
                        strong+=bot_emoji[self.direction]
                    else:
                        strong+=emojis[0]  # Default emoji if direction is invalid
                else:
                    cell_value = self.grid.get(i,j)
                    # Safety check for emoji index
                    if 0 <= cell_value < len(emojis):
                        strong+=emojis[cell_value]
                    else:
                        strong+=emojis[0]  # Default emoji if value is invalid
            strong+="\n"
        return strong
    
            
def count_bot_commands(code:str):
    lines = code.split("\n")
    commands = 0
    for i in lines:
        if "can_move()" in i:
            if i.find("#") == -1 or i.find("#")>i.find("can_move()"):
                commands+=1
        elif "turn_right()" in i:
            if i.find("#") == -1 or i.find("#")>i.find("turn_right()"):
                commands+=1
        elif "turn_left()" in i:
            if i.find("#") == -1 or i.find("#")>i.find("turn_left()"):
                commands+=1
        elif "move_forward()" in i:
            if i.find("#") == -1 or i.find("#")>i.find("move_forward()"):
                commands+=1
        elif "move_backward()" in i:
            if i.find("#") == -1 or i.find("#")>i.find("move_backward()"):
                commands+=1
        elif "can_move_back()" in i:
            if i.find("#") == -1 or i.find("#")>i.find("can_move_back()"):
                commands+=1
    return commands

def interpreter(code:str, grid):
    bot = Bot(grid)
    bot.moves = 0
    lines = code.split("\n")
    code_arr = []
    for line in lines:
        if "import" in line:
            pass
        else:
            code_arr.append(line)
    mod_string = "\n".join(code_arr)
    exec_func(mod_string, globals={"bot":bot})
    if bot.win_state:
        commands = count_bot_commands(mod_string)
        # if commands <= grid.par:
        #     print("Star")
        # else:
        #     print("check")  


griddy = [[1,1,1,1,1],
          [1,0,0,3,1],
          [1,0,1,1,1],
          [1,0,1,1,1],
          [1,0,1,1,1]]
robot_start = (4,1)
direction = 0
grid = Grid(griddy, robot_start, direction, 3)

bot = Bot(grid)

