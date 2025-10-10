class WinInterruption(Exception):
    pass

def exec_func(source, globals=None, locals=None):
    try:
        exec(source, globals, locals)
    except WinInterruption:
        pass

class Grid:
    """Data denotes tile types: 0 = blank tile, 1 = basic wall tile, 2 = zappy wall tile, 3 = end
       4 = Yellow key, 5 = Yellow gate, 6 = Red key, 7 = Red gate, 8 = Blue key, 9 = Blue gate 
    """
    def __init__(self, data, start_pos, start_dir, par):
        self.start_pos = start_pos
        self.rows = len(data)
        self.cols = len(data[0])
        self.data = data
        self.start_direction = start_dir
        self.par = par
    def get(self, row, col):
        return self.data[row][col]
    

class Bot:
    def __init__(self, grid:Grid):
        self.grid = grid
        self.direction = grid.start_direction
        self.start = grid.start_pos
        self.win_state = False
        self.i = grid.start_pos[0]
        self.j = grid.start_pos[1]
        self.alive = True
        

    def move_forward(self):
        directions = ["up", "left", "down", "right"]
        dir = directions[self.direction]
        if dir == "up" and self.alive and not self.win_state:
            if self.can_move():
                if self.grid.data[self.i-1][self.j] == 2:
                    self.reset()
                else:
                    self.i -= 1
        elif dir == "down" and self.alive and not self.win_state:
            if self.can_move():
                if self.grid.data[self.i+1][self.j] == 2:
                    self.reset()
                else:
                    self.i += 1
        if dir == "right" and self.alive and not self.win_state:
            if self.can_move():
                if self.grid.data[self.i][self.j+1] == 2:
                    self.reset()
                else:
                    self.j+=1
        if dir == "left" and self.alive and not self.win_state:
            if self.can_move():
                if self.grid.data[self.i][self.j-1] == 2:
                    self.reset()
                else:
                    self.j -= 1
        print(self.__str__())
        self.win_state = self.check_win()
        if (self.win_state):
            raise WinInterruption
    
    def turn_right(self):
        self.direction -= 1
        self.direction %= 4

    def turn_left(self):
        self.direction += 1
        self.direction %= 4
    
    def can_move(self):
        directions = ["up", "left", "down", "right"]
        dir = directions[self.direction]
        print(dir)
        if dir == "up":
            if self.i > 0:
                return self.grid.data[self.i-1][self.j] not in [1, 2, 5, 7, 9]
        elif dir == "down":
            if self.i < self.grid.rows:
                return self.grid.data[self.i+1][self.j] not in [1, 2, 5, 7, 9]
        elif dir == "right":
            if self.j < self.grid.cols:
                print("why")
                return self.grid.data[self.i][self.j+1] not in [1, 2, 5, 7, 9]
        elif dir == "left":
            if self.j > 0:
                return self.grid.data[self.i][self.j-1] not in [1, 2, 5, 7, 9]
        return False
    
    def check_win(self):
        if self.grid.get(self.i, self.j) == 3:
            return True
        return False


    def reset(self):
        self.i = self.start[0]
        self.j = self.start[1]
        self.alive = False
    
    def __str__(self):
        strong = ""
        emojis = ["⬜ ","⬛ ","🟦 ","🟫 "]
        bot_emoji = ["⬆️  ","⬅️  ","⬇️  ","➡️  "]
        for i in range(self.grid.rows):
            for j in range(self.grid.cols):
                if i == self.i and j == self.j:
                    strong+=bot_emoji[self.direction]
                else:
                    strong+=emojis[self.grid.get(i,j)]
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
    return commands

def interpreter(code:str, grid):
    bot = Bot(grid)
    lines = code.split("\n")
    code_arr = []
    for line in lines:
        if "import" in line and "math" not in line:
            pass
        else:
            code_arr.append(line)
    mod_string = "\n".join(code_arr)
    exec_func(mod_string, globals={"bot":bot})
    if bot.win_state:
        commands = count_bot_commands(mod_string)
        if commands <= grid.par:
            print("Star")
        else:
            print("check")   


griddy = [[1,1,1,1,1],
          [1,0,0,3,1],
          [1,0,1,1,1],
          [1,0,1,1,1],
          [1,0,1,1,1]]
robot_start = (4,1)
direction = 0
grid = Grid(griddy, robot_start, direction, 3)

bot = Bot(grid)


interpreter("""
import requests
while True:
    if (bot.can_move()):
        bot.move_forward()
    else:
        bot.turn_right()""", grid)
