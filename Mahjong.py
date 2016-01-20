
'''defines a single tile'''
from _ast import Str
class Tile:
        
    '''List of all the possible suits'''
    SUITS = ['Sou', 'Pin', 'Man', 'TON', 'NAN', 'SHIA', 'PEI', 'HAKU', 'HATSU',
             'CHUN']
    WINDS = ['TON', 'NAN', 'SHIA', 'PEI']
    
    def __init__(self, num: int, suit: str):
        self.num = num
        self.suit = suit
       
    ''' returns the string name of the tile'''
    def to_string(self) -> str:
        if self.num == 0:
            if self.suit == 'HATSU':
                return "HA\nTSU"
            if self.suit == 'CHUN':
                return 'CH\nUN'
            '''ONCE DONE MAKE THIS BLANK'''
            if self.suit == 'HAKU':
                return 'HA\nKU'
            return self.suit
        return (str(self.num) + "\n" + self.suit)
        
    ''' define the greater than operation'''
    def __gt__(self, t2: 'Tile') -> bool:
        if self.get_placement() == t2.get_placement():
            return self.num > t2.num
        return self.get_placement() > t2.get_placement()
    
    '''define the equality operation'''
    def __eq__(self, t2: 'Tile') -> bool:
        if t2 == None:
            return False
        return self.num == t2.num and self.suit == t2.suit
    
    '''define a copy operation that returns a copy of the tile'''
    def copy(self) -> 'Tile':
        return Tile(self.num, self.suit)
        
    '''returns the color of the tile'''
    def return_color(self) -> str:
        if self.suit == 'HAKU':
            return 'black'
        elif self.suit == 'CHUN':
            return 'red'
        elif self.suit == 'HATSU':
            return '#009aff'
        elif self.suit == 'Pin':
            return '#cc00cc'
        elif self.suit == 'Man':
            return '#cc0000'
        elif self.suit == "Sou":
            #if self.num == 2 or self.num == 3 or self.num == 4 or self.num == 6 or self.num == 8:
            return '#009aff'
        else:
            return 'black'
    
    ''' returns a number for the suit (switch for int), used for sorting'''
    def get_placement(self) -> int:
        if self.suit == 'Sou':
            return 0
        if self.suit == 'Pin':
            return 1
        if self.suit == 'Man':
            return 2
        if self.suit == 'TON':
            return 3
        if self.suit == 'NAN':
            return 4
        if self.suit == 'SHIA':
            return 5
        if self.suit == 'PEI':
            return 6
        if self.suit == 'HAKU':
            return 7
        if self.suit == 'HATSU':
            return 8
        else:
             return 9
    
    ''' get number''' 
    def get_num(self) -> int:
        return self.num

import random

class Mahjong:
    ''' some constants'''
    NUMBER_OF_TILES = 136
    ONE_FOURTH = int(NUMBER_OF_TILES/4)
    ONE_EIGHTH = int(NUMBER_OF_TILES/8)
    
    ''' represents a single round of mahjong within the game, where the game is actually played'''
    class Round:
        
        ''' start a new round, creates a new tile set'''
        def __init__(self, stick_count: int):
            self.tiles = self.new_tile_set()
            ''' number of richi sticks (may be carried over)'''
            self.richi_sticks = stick_count
        
        def start(self):
            ''' generate new tile set, shuffle, and roll dice'''
            
            '''Tile 0 is the Ton player's right-most upper level tile
                Tile 1 is the Ton player's right-most lower level tile
                Tile 2 is the Ton player's second right-most upper level tile, etc...
                even tiles are upper-level tiles, odd tiles are lower-level tiles'''
            self.tiles = self.new_tile_set()
            self.size = len(self.tiles)
            self.shuffle()
            self.dice_roll = self.roll_dice()
            ''' how much money is in the pot'''
            self.pot = 0
            
            '''    THE FOLLOWING ARE ALL RELATIVE TO THE DEALER (DEALER = POSITION 0)''' 
            ''' where the wall starts'''
            self.wall = int(self.calculate_wall(self.dice_roll))
            ''' where the dead wall begins from the back'''
            self.deadwall = int((self.wall-2)%self.size)
            ''' where the dead wall begins from the front'''
            self.deadwall_start = int((self.wall-14)%self.size)
            ''' where the dora starts'''
            self.dora = int((self.wall-6)%self.size)
            ''' number of dora'''
            self.dora_count = 1
            
            
        ''' draws a single tile'''
        def draw(self) -> Tile:
            t = self.tiles[self.wall]
            self.tiles[self.wall] = None
            self.next_draw()
            return t
    
        ''' deals n tiles (4 or 1), used for starting hands'''
        def deal(self, n: int) -> [Tile]:
            t = []
            for i in range(n):
                t.append(self.draw())
            return t
        
        ''' draw a tile from the dead wall, update the wall, move deadwall forward'''
        def deadwall_draw(self) -> Tile:
            t = self.tiles[self.deadwall]
            self.tiles[self.deadwall] = None
            if self.deadwall%2 == 0:
                self.deadwall += 1
            else:
                self.deadwall = self.deadwall - 3
            ''' increase dora count by 1'''
            self.dora_count += 1
            return t
        
        ''' adds a richi stick to the pot'''
        def add_richi(self):
            self.richi_sticks += 1
        
        ''' returns a list of the dora'''
        def get_dora(self) -> [Tile]:
            dora_tiles = []
            for i in range(self.dora_count):
                dora_tiles.append(self.tiles[self.dora-2*i])
            return dora_tiles
        
        ''' returns a list of the uradora'''
        def get_uradora(self) -> [Tile]:
            dora_tiles = []
            for i in range(self.dora_count):
                dora_tiles.append(self.tiles[self.dora-2*i+1])
            return dora_tiles
        
        ''' returns true if exhaustive draw'''
        def exhaustive_draw(self) -> bool:
            return self.wall == self.deadwall_start
            
        
        ''' generates a new tile set'''
        def new_tile_set(self) -> [Tile]:
            tiles = []
            ''' add each type of tile 4 times'''
            for i in range(4):
                '''add the numbered suits'''
                for j in range(1,10):
                    tiles.append(Tile(j, 'Sou'))
                    tiles.append(Tile(j, 'Pin'))
                    tiles.append(Tile(j, 'Man'))
                tiles.append(Tile(0, 'TON'))
                tiles.append(Tile(0, 'NAN'))
                tiles.append(Tile(0, 'SHIA'))
                tiles.append(Tile(0, 'PEI'))
                tiles.append(Tile(0, 'HAKU'))
                tiles.append(Tile(0, 'HATSU'))
                tiles.append(Tile(0, 'CHUN'))
            return tiles
        
        '''shuffles the tiles'''
        def shuffle(self) -> None:
            for i in range(self.size-1, 0, -1):
                r = random.randrange(i)
                self.tiles[i], self.tiles[r] = self.tiles[r], self.tiles[i]
        
        '''rolls 2 dice for us'''
        def roll_dice(self) -> int:
            return (random.randrange(6) + random.randrange(6) + 2)
        
        '''calculates where the wall starts'''
        def calculate_wall(self, roll: int) -> int:
            mod = roll%4
            
            if mod == 0:
                mod = self.size/4
            elif mod == 1:
                mod = 0
            elif mod == 2:
                mod = 3*self.size/4
            else:
                mod = self.size/2
            
            return (mod + roll*2)
        
        ''' moves the next draw from the wall forward by 1'''
        def next_draw(self) -> None:
            self.wall += 1
            if self.wall >= self.size:
                self.wall = 0

    '''creates a brand new mahjong game object. Starts game from scratch'''
    ''' separate from a round where the game is actually played! represents all the rounds combined'''
    def __init__(self, number_of_winds: int):
        ''' number of winds to play'''
        self.number_of_winds = number_of_winds
        ''' start with first wind'''
        self.wind = 0
        ''' start with player 0'''
        self.dealer = 0
        ''' start with no bonus rounds'''
        self.bonus_round = 0
        
    ''' starts a round '''
    def start_round(self):
        self.Round.start()
        
    ''' moves the round counter by 1 and adjusts attributes as needed'''
    def next_round(self, repeat = False):
        ''' if no repeat, move round forward by 1'''
        if not repeat:
            self.bonus_round = 0
            self.dealer += 1
            ''' if round reaches 4, move wind forward'''
            if self.dealer >= 4:
                self.dealer = 0
                self.wind += 1
                ''' if wind reaches the limit, game is over'''
                if self.wind == self.number_of_winds:
                    self.game_over()
        ''' if repeat increment bonus round'''
        if repeat:
            self.bonus_round += 1
    
    ''' returns the current wind in string form'''        
    def get_wind(self) -> Str:
        return Tile.WINDS[self.wind]
    
    ''' marker for mahjong game over'''
    def game_over(self) -> int:
        return 0  
    
        
if __name__ == '__main__':
    a = Tile(0, 'TON')
    b = Tile(0, 'TON')
    print(a.copy()==b)
        
        
        
        
        
        
        
        
        
        
        
        
        
