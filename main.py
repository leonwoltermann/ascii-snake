from shutil import get_terminal_size
from random import randint
from os import system
from time import sleep
from pynput import keyboard


class Snake:
    def __init__(self):
        self.columns, self.lines = get_terminal_size()
        self.grid = self.create_grid()
        self.snake_column, self.snake_line = self.snake_init()
        self.snake = [(self.snake_line, self.snake_column)]
        self.snake_length = 20
        self.gameover = False
        self.column_speed = 0.09
        self.line_speed = 0.05
        self.food = self.spawn_food()
        self.score = 0

    def create_grid(self):
        return [[0 for _ in range(self.columns)] for _ in range(self.lines-1)]
    
    def snake_init(self):
        return (int(self.columns / 2), int(self.lines / 2))
    
    def update_grid(self):
        for i, e in enumerate(self.snake):
            if i == 0:
                self.grid[e[0]][e[1]] = 1
            else:
                self.grid[e[0]][e[1]] = 2
            if i == self.snake_length:
                self.grid[e[0]][e[1]] = 0
                self.snake.pop(i)

        for i, e in enumerate(self.food):
            self.grid[e[0]][e[1]] = 3
            
    def update_snake(self, direction):
        if direction == "UP":
            self.snake_line -= 1
        if direction == "DOWN":
            self.snake_line += 1
        if direction == "RIGHT":
            self.snake_column += 1
        if direction == "LEFT":
            self.snake_column -= 1
        
        if ((self.snake_line, self.snake_column) in self.snake 
            or self.snake_line == 0
            or self.snake_line == self.lines - 2
            or self.snake_column == 0
            or self.snake_column == self.columns - 1
            ):
            self.gameover = True
        else:
            self.snake.insert(0, (self.snake_line, self.snake_column))

    def spawn_food(self):
        food = (randint(1, self.lines - 3), randint(1, self.columns - 2))
        while food in self.snake:
            food = (randint(1, self.lines - 3), randint(1, self.columns - 2))

        return [food]
    
    def snake_eat(self):
        if self.snake[0] == self.food[0]:
            self.score += 1
            self.snake_length += 5
            self.food.pop(0)

            food = (randint(1, self.lines - 3), randint(1, self.columns - 2))
            while food in self.snake:
                food = (randint(1, self.lines - 3), randint(1, self.columns - 2))
            self.food.insert(0, food)

            if self.line_speed > 0.01:
                self.column_speed -= 0.009
                self.line_speed -= 0.005

    def draw_board(self):
        board = ""
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if i == 0 and j == 0:
                    board += "┌" #"█" #"┌"
                elif i == 0 and j == self.columns-1:
                    board += "┐" #"█" #"┐"
                elif i == self.lines-2 and j == 0:
                    board += "└"# "█" #"└"
                elif i == self.lines-2 and j == ((self.columns-1)//2)-5:
                    board += f" SCORE: {self.score} "
                elif i == self.lines-2 and j > ((self.columns-1)//2)-5 and j < ((self.columns-1)//2)+5:
                    pass
                elif i == self.lines-2 and j == self.columns-1:
                    board += "┘"#"█" #"┘"
                elif i == 0 or i == self.lines - 2:
                    board += "─"#"█" #"─"
                elif j == 0 or j == self.columns - 1:
                    board += "│"# "█" #"│"
                elif self.grid[i][j] == 0:
                    board += " "
                elif self.grid[i][j] == 1:
                    board += "@"
                elif self.grid[i][j] == 2:
                    board += "o"#"▢"
                elif self.grid[i][j] == 3:
                    board += "%"

        return(board)


snake = Snake()

direction = "RIGHT"

def on_press(key):
    global direction
    if key == keyboard.Key.up:
        direction = 'UP'
    elif key == keyboard.Key.down:
        direction = 'DOWN'
    elif key == keyboard.Key.left:
        direction = 'LEFT'
    elif key == keyboard.Key.right:
        direction = 'RIGHT'
        
listener = keyboard.Listener(on_press=on_press)
listener.start()

while not snake.gameover:
    system("clear")
    snake.update_grid()
    print(snake.draw_board())
    snake.update_snake(direction)
    snake.snake_eat()

    if direction == "UP" or direction == "DOWN":
        sleep(snake.column_speed)
    if direction == "LEFT" or direction == "RIGHT":
        sleep(snake.line_speed)

print("Game Over")
