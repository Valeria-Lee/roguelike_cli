# Threads.
# Un hilo realiza la generacion de dungeons (areas) mientras que otro se encarga de la logica del juego.

import random, threading

cols_nums: int = 8
rows_nums: int = 4

prev_symbol: str = None
door = None
playing: bool

map_lock = threading.Lock()
gameplay_loop_thread = None
terrain_gen_thread = None

class Tile:
    def __init__(self, symbol='\033[0;32m.\033[0;32m', type='grass'):
        self.symbol = symbol
        self.type = type
    
    def get_symbol(self):
        return self.symbol
    
    def set_symbol(self, s):
        self.symbol = s

        if self.symbol ==  '.':
            self.type = 'grass'
        elif self.set_symbol == '~':
            self.type = 'water'
        elif self.set_symbol == '^':
            self.type = 'rock'
        elif self.set_symbol == 'Y' or self.set_symbol == 'T':
            self.type = 'tree'

class Player:
    def __init__(self, pos=[1,1], symbol="\033[0;31mX\033[0;31m"):
        self.symbol = symbol
        self.pos = pos # initial position

    def move(self, dir:str):
        if dir.lower() == 's' and self.pos[0] < 4:
            self.pos[0] += 1
        if dir.lower() == 'w' and self.pos[0] > 0:
            self.pos[0] -= 1
        if dir.lower() == 'd' and self.pos[1] < 9:
            self.pos[1] += 1
        if dir.lower() == 'a' and self.pos[1] > 0:
            self.pos[1] -= 1

    def check_can_kill(self, attack_pos):
        can_kill_enemy: bool = False

        if self.pos in attack_pos:
            can_kill_enemy = True
        return can_kill_enemy

class Enemy:
    def __init__(self, pos=[], attack_pos=[], symbol="\x1b[33mO\x1b[33m"):
        self.pos = pos
        self.attack_pos = attack_pos
        self.symbol = symbol
    
    def get_attack_points(self):
        self.attack_pos = [
            [self.pos[0]+1, self.pos[1]],
            [self.pos[0], self.pos[1]+1],
            [self.pos[0]-1, self.pos[1]],
            [self.pos[0], self.pos[1]-1]
        ]

        return self.attack_pos

class Door:
    def __init__(self, pos=None, symbol = "\033[0;37m⊱\033[0;37m"):
        self.symbol = symbol
        self.pos = pos

    def get_pos(self):
        return self.pos

def generate_basic_map():
    game_map = [[Tile() for col in range(cols_nums)] for row in range(rows_nums)]
    return game_map

def generate_framed_screen():
    game_screen = generate_random_terrain()
    separator:list = ["\033[0;35m*\033[0;35m", "\033[0;35m=\033[0;35m", "\033[0;35m=\033[0;35m", "\033[0;35m=\033[0;35m", "\033[0;35m=\033[0;35m", "\033[0;35m=\033[0;35m", "\033[0;35m=\033[0;35m", "\033[0;35m=\033[0;35m", "\033[0;35m=\033[0;35m", "\033[0;35m*\033[0;35m"]

    for row in range(rows_nums):
        for col in range(cols_nums):
            if col == 0:
                game_screen[row].insert(col, "\033[0;35m|\033[0;35m")
            if col == 3:
                game_screen[row].append("\033[0;35m|\033[0;35m")

    game_screen.insert(0, separator)
    game_screen.append(separator)

    return game_screen

def add_door(map):
    door = Door()

    door.pos = [random.randint(1,3), 9]

    map[door.pos[0]][door.pos[1]] = door.symbol

    return door

def display_screen(game_screen: list):
    for i in range(6):
        for j in range(10):
            if isinstance(game_screen[i][j], Tile):
                print(game_screen[i][j].get_symbol(), end=" ")
            else: 
                print(game_screen[i][j], end=" ")
        print("\n")

def generate_random_terrain(): # edit the map
    map = generate_basic_map()
    symbols: list = ["\033[0;37m^\033[0;37m", "\033[1;34m~\033[1;34m", "\x1b[38;5;142mY\x1b[38;5;142m", "\033[1;32mT\033[1;32m"]

    props_number = random.randint(1, 16)

    if props_number == 1:
        random_symbol = random.choice(symbols)
        map[random.randint(0,3)][random.randint(0,7)].set_symbol(random_symbol)
    else:
        for i in range(props_number):
            random_symbol = random.choice(symbols)
            map[random.randint(0,3)][random.randint(0,7)].set_symbol(random_symbol)
    
    return map

def init_map(map, player):
    map[player.pos[0]][player.pos[1]] = player.symbol
    display_screen(map)

def update_map(map, player): 
    with map_lock:

        prev_symbol = map[player.pos[0]][player.pos[1]]

        if prev_symbol == "\033[0;31mX\033[0;31m": prev_symbol = '\033[0;32m.\033[0;32m'

        for i in range(len(map)):
            for j in range(len(map[i])):
                if map[i][j] == "\033[0;31mX\033[0;31m":
                    map[i][j] = prev_symbol
                    break

        map[player.pos[0]][player.pos[1]] = player.symbol

        display_screen(map)

def add_enemy(map):
    enemy_pos = [random.randint(1,3), random.randint(1,7)]
    e = Enemy()

    map[enemy_pos[0]][enemy_pos[1]] = e.symbol
    e.pos = [enemy_pos[0],enemy_pos[1]]

    return e

def kill_enemy(enemy, map):
    enemy_killed: bool = True

    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == enemy.symbol:
                new_tile = Tile()
                map[i][j] = new_tile.get_symbol()
                print("you killed the enemy!!")
                return enemy_killed

def check_win(enemy_killed, door , player):
    if enemy_killed and player.pos == door.pos:
        print("you win!!")
        main_gameplay()

def main_gameplay():
    global map_lock, terrain_gen_thread, gameplay_loop_thread
    initial_map = generate_framed_screen()
    setup_done: bool = False
    p: Player
    dir: str = None
    e = add_enemy(initial_map)
    attack_pos = e.get_attack_points()
    door = add_door(initial_map)
    can_kill_enemy: bool = False
    playing: bool = True

    while playing:
        if not setup_done:
            p = Player()
            init_map(initial_map, p)
            dir = input("> ")
            setup_done = True
        else:
            if dir != None:
                p.move(dir)
                update_map(initial_map, p)
                dir = input("> ") 

                if can_kill_enemy == False:
                    can_kill_enemy = p.check_can_kill(attack_pos)
                else:
                    kill_enemy(e,initial_map)
                
                check_win(can_kill_enemy, door, p)
        if terrain_gen_thread is not None:
            print(f"El hilo de generacion de terreno esta vivo? -> {terrain_gen_thread.is_alive()}")
        if gameplay_loop_thread is not None:
            print(f"El hilo del juego esta vivo? -> {gameplay_loop_thread.is_alive()}")

def terrain_thread():
    global game_map
    while True:
        with map_lock:
            game_map = generate_random_terrain()
            print("\ntierra generada, hilo a punto de dormir")
        threading.Event().wait(3)

def gameplay_thread():
    main_gameplay()

def main():
    global terrain_gen_thread, gameplay_loop_thread

    terrain_gen_thread = threading.Thread(target=terrain_thread)
    terrain_gen_thread.start()

    gameplay_loop_thread = threading.Thread(target=gameplay_thread)
    gameplay_loop_thread.start()

if __name__ == '__main__':
    main()