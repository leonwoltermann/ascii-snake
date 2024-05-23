from shutil import get_terminal_size
from random import randint
import os
from time import sleep
from pynput import keyboard

# to do:
# lock input when running: https://stackoverflow.com/questions/67083097/how-to-prevent-user-input-into-console-when-program-is-running-in-python

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
        self.column_speed_increase = 0.009 #make this variable smaller to decrease difficulty
        self.line_speed_increase = 0.005 #and this too
        self.food = self.spawn_food()
        self.score = 0
        self.obstacles = self.spawn_obstacle()

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

        for i, e in enumerate(self.obstacles):
            self.grid[e[0]][e[1]] = 4
            
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
        elif (self.snake_line, self.snake_column) in self.obstacles:
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
            while food in self.snake or food in self.obstacles:
                food = (randint(1, self.lines - 3), randint(1, self.columns - 2))
            self.food.insert(0, food)

            obstacle = (randint(1, self.lines - 3), randint(1, self.columns - 2))
            while obstacle in self.snake or obstacle in self.food:
                obstacle = (randint(1, self.lines - 3), randint(1, self.columns - 2))
            self.obstacles.insert(0, obstacle)
                

            if self.line_speed > 0.01:
                self.column_speed -= self.column_speed_increase
                self.line_speed -= self.line_speed_increase
    
    def spawn_obstacle(self):
        obstacle = (randint(1, self.lines - 3), randint(1, self.columns - 2))
        while obstacle in self.snake or obstacle in self.food:
            obstacle = (randint(1, self.lines - 3), randint(1, self.columns - 2))

        return [obstacle]

    def draw_board(self):
        board = ""
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if i == 0 and j == 0:
                    board += "┌"
                elif i == 0 and j == self.columns-1:
                    board += "┐"
                elif i == self.lines-2 and j == 0:
                    board += "└"
                elif i == self.lines-2 and j == ((self.columns-1)//2)-5:
                    board += f" SCORE: {self.score} "
                elif i == self.lines-2 and j > ((self.columns-1)//2)-5 and j < ((self.columns-1)//2)+5:
                    pass
                elif i == self.lines-2 and j == self.columns-1:
                    board += "┘"
                elif i == 0 or i == self.lines - 2:
                    board += "─"
                elif j == 0 or j == self.columns - 1:
                    board += "│"
                elif self.grid[i][j] == 0:
                    board += " "
                elif self.grid[i][j] == 1:
                    board += "@"
                elif self.grid[i][j] == 2:
                    board += "o"#"▢"
                elif self.grid[i][j] == 3:
                    board += "%"
                elif self.grid[i][j] == 4:
                    board += "X"

        return(board)


snake = Snake()

direction = "RIGHT"

def on_press(key):
    global direction
    if key == keyboard.Key.up and direction != "DOWN":
        direction = 'UP'
    elif key == keyboard.Key.down and direction != "UP":
        direction = 'DOWN'
    elif key == keyboard.Key.left and direction != "RIGHT":
        direction = 'LEFT'
    elif key == keyboard.Key.right and direction != "LEFT":
        direction = 'RIGHT'
        
listener = keyboard.Listener(on_press=on_press)
listener.start()


while not snake.gameover:
    os.system('cls' if os.name == 'nt' else 'clear')
    snake.update_grid()
    print(snake.draw_board())
    snake.update_snake(direction)
    snake.snake_eat()

    if direction == "UP" or direction == "DOWN":
        sleep(snake.column_speed)
    if direction == "LEFT" or direction == "RIGHT":
        sleep(snake.line_speed)

print("Game Over")
