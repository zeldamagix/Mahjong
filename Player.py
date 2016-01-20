import Mahjong
from Mahjong import Tile


class Player:
    MAX_HAND_SIZE = 13
    
    ''' defines a new player'''
    def __init__(self, name: str, turn: int):
        self.name = id
        ''' player's tiles'''
        ''' open is a tuple (triplet as a list, position to be tilted)'''
        self.open = []
        ''' closed is just a list of tiles in hand'''
        self.closed = []
        ''' discards is just a list of tiles discarded'''
        self.discards = []
        self.next_tile = None
        ''' player's points'''
        self.points = 250
        '''turn is the player's turn position (which position the player is for Ton)'''
        self.turn = turn
        ''' richi is the turn the player called richi, only based off the players turns, not off the 
        rounds turns. Turn 0 is first discard!!!'''
        self.richi = -1
    
    ''' adds the start tiles when starting a game'''
    def deal(self, tiles: [Tile]):
        self.closed.extend(tiles)
    
    ''' draws a single tile'''
    def draw_tile(self, tile: Tile):
        self.next_tile = tile
        
    '''discards the n tile in the open hand'''
    def discard_tile(self, n: int):
        '''safety net'''
        if n < 0 and n >= len(self.closed):
            return
        self.discards.append(self.closed[n])
        del self.closed[n]
    
    ''' discards the next tile'''
    def pass_tile(self):
        self.discards.append(self.next_tile)
        self.next_tile = None
        
    ''' inserts the next tile into the hand'''
    ''' insertion sort since no need to resort everything'''
    def insert_tile(self):
        for i in range(len(self.closed)):
            if self.next_tile > self.closed[i]:
                continue
            self.closed.insert(i, self.next_tile)
            self.next_tile = None
            return
        '''special case if the tile belongs at the end of the list i.e, bigger than everything else'''
        self.closed.append(self.next_tile)
        self.next_tile = None
        
    ''' resets the hand for next game'''
    def clear_hand(self):
        self.closed = []
        self.open = []
        self.discards = []
        self.next_tile = None
    
    ''' makes a richi call if conditions are met'''
    def call_richi(self):
        if len(self.open) == 0 and self.next_tile != None:
            self.richi = len(self.discards)
            
    ''' allow cancelling of richi if its the turn we called it'''
    def cancel_richi(self):
        if len(self.discards) <= self.richi:
            self.richi = -1
        
    '''COMPLICATED STUFF BELOW'''
    ''' returns whether or not a tile t can be combined into a triple'''
    def can_pon(self, t: Tile) -> bool:
        return (sum(item == t for item in self.closed) >= 2)
    
    '''calls a triple on a tile t'''
    ''' position is the position of the tile to be tilted, zero based indexing'''
    def pon(self, t: Tile, p: int):
        '''delete 2 copies of the tile from the hand'''
        self.delete_tile(t)
        self.delete_tile(t)
        self.open.append(([t.copy(), t.copy(), t.copy()], p))
        
    ''' can make an open quad'''
    def can_open_kan(self, t: Tile):
        return (sum(item == t for item in self.closed) >= 3)
    
    ''' make an open quad'''
    def open_kan(self, t: Tile, p: int):
        '''delete 3 copies of the tile from the hand'''
        self.delete_tile(t)
        self.delete_tile(t)
        self.delete_tile(t)
        self.open.append(([t.copy(), t.copy(), t.copy(), t.copy()], p))
    
    ''' can make a closed quad from hand'''
    def can_closed_kan(self):
        ''' if we have 4 of a kind in the closed hand'''
        for i in range(len(self.closed)-3):
            if ((self.closed[i] == self.closed[i+1]) and (self.closed[i] == self.closed[i+2]) and 
                (self.closed[i] == self.closed[i+3])):
                return True
        '''if we have a triple and we draw the fourth'''
        if (sum(item == self.next_tile for item in self.closed) == 3):
            return True
        return False
    
    ''' make a closed kan from hand with tile starting from position p'''
    def closed_kan(self, p: int):
        '''handle index out of bounds error easily with a try except block'''
        ''' case where we draw the fourth tile and have 3 in hand'''
        try:
            if sum(item == self.next_tile for item in self.closed) == 3:
                if ((self.closed[p] == self.next_tile) and (self.closed[p+1] == self.next_tile) and
                    (self.closed[p+2] == self.next_tile)):
                    '''add a set of 4 to our open hand'''
                    self.open.append(([self.next_tile.copy(), self.next_tile.copy(), self.next_tile.copy(),
                                      self.next_tile.copy()], 3))
                    '''delete 3 copies of tile from our hand'''
                    for i in range(3):
                        self.delete_tile(self.next_tile)
                    '''delete the next tile'''
                    self.next_tile = None
        except IndexError:
            pass 
        '''handle index out of bounds errors easily with a try except block'''
        ''' case where we have 4 in a row in hand'''
        try:
            ''' if there are 4 copies of the selected tile'''
            if ((self.closed[p] == self.closed[p+1]) and (self.closed[p] == self.closed[p+2]) and
                (self.closed[p] == self.closed[p+3])):
                ''' add 4 copies to open hand'''
                self.open.append(([self.closed[p].copy(), self.closed[p].copy(), self.closed[p].copy(),
                                   self.closed[p].copy()], 3))
                ''' delete 4 copies of the tile'''
                for i in range(4):
                    self.delete_tile(self.closed[p])
            
        except IndexError:
            return
        
    '''returns whether or not a tile can be added to a triple to become a quad'''
    def can_added_kan(self):
        ''' check every triplet in open hand'''
        for tup in self.open:
            ''' if the triplet is a pon'''
            if ((tup[0][0] == tup[0][1]) and (tup[0][0] == tup[0][2])):
                '''if the triplet tile is in our closed hand or our next tile'''
                if ((tup[0][0] == self.next_tile) or (tup[0][0] in self.closed)):
                    return True
        return False
    
    '''make an added kan'''
    ''' P HERE IS THE POSITION OF THE TRIPLET IN THE OPEN HAND''' 
    def added_kan(self, p: int):
        ''' if the triplet is a pon'''
        if (self.open[p][0][0] == self.open[p][0][1] and len(self.open[p][0])<4):
            '''if the next tile is the same as the triple'''
            if self.open[p][0][0] == self.next_tile:
                '''add next tile to the triplet and get rid of our next tile'''
                self.open[p][0].append(self.next_tile)
                self.next_tile = None
            ''' if the the last tile is in our hand'''
            if self.open[p][0][0] in self.closed:
                self.open[p][0].append(self.open[p][0][0])
                '''delete tile from closed hand'''
                del self.closed[self.closed.index(self.open[p][0][0])]
                
    ''' returns whether or not a tile can be eaten'''
    def can_chi(self, t: Tile) -> bool:
        if t.num == 0:
            return False
        if Tile(t.num-2, t.suit) in self.closed and Tile(t.num-1, t.suit) in self.closed:
            return True
        if Tile(t.num-1, t.suit) in self.closed and Tile(t.num+1, t.suit) in self.closed:
            return True
        if Tile(t.num+1, t.suit) in self.closed and Tile(t.num+2, t.suit) in self.closed:
            return True
        return False
        
    ''' eats a consecutive triple'''
    ''' position p is where the consecutive starts for the chi'''
    ''' always position 0 to be tilted'''
    def chi(self, t: Tile, p: int):
        if self.closed[p].suit != t.suit:
            return
        ''' if our case is 1,2 eat 3'''
        if self.closed[p].num == t.num-2 and Tile(t.num-1, t.suit) in self.closed:
            self.open.append(([t, self.closed[p], Tile(t.num-1, t.suit)], 0))
            del self.closed[p]
            self.delete_tile(Tile(t.num-1, t.suit))
        '''if our case is 2,4 eat 3'''
        if self.closed[p].num == t.num-1 and Tile(t.num+1, t.suit) in self.closed:
            self.open.append(([t, self.closed[p], Tile(t.num+1, t.suit)], 0))
            del self.closed[p]
            self.delete_tile(Tile(t.num+1, t.suit))
        ''' if our case is 4, 5 eat 3'''
        if self.closed[p].num == t.num+1 and Tile(t.num+2, t.suit) in self.closed:
            self.open.append(([t, self.closed[p], Tile(t.num+2, t.suit)], 0))
            del self.closed[p]
            self.delete_tile(Tile(t.num+2, t.suit))
        
        
    ''' deletes a tile t from closed hand'''
    ''' used for the different calls'''
    def delete_tile(self, t: Tile):
        for i in range(len(self.closed)):
            if self.closed[i] == t:
                del self.closed[i]
                return
            
        
    ''' sorts the closed hand'''
    def sort(self):
        ''' make our buckets and add our tiles into the buckets'''
        buckets = []
        for i in range(len(Tile.SUITS)):
            buckets.append([])
        for t in self.closed:
            buckets[t.get_placement()].append(t)
            
        '''clear our hand'''
        self.closed = []
        ''' sort within each bucket and add back into hand'''
        for b in buckets:
            b.sort(key = lambda x: x.num)
            self.closed.extend(b)
        
        
if __name__ == '__main__':
    mg = Mahjong.Mahjong(1)
    round = mg.Round(0)
    round.start()
    p = Player('A', 0)
    for i in range(3):
        p.deal(round.deal(4))
    print(len(p.closed))
    p.sort()
    
    for i in p.closed:
        print(i.to_string().replace('\n', ' '), end = ' ')
    print('')
        
    p.draw_tile(round.draw())
    print('draw is: ' + p.next_tile.to_string().replace('\n', ' '), end = ' ')
    p.insert_tile()
    print('')
    
    for i in p.closed:
        print(i.to_string().replace('\n', ' '), end = ' ')
    
    print('')
    print('discarding the 5th tile...')
    p.discard_tile(5)
    for i in p.closed:
        print(i.to_string().replace('\n', ' '), end = ' ')  
    print('')
      
    print('\n')  
    print('pon tests')
    p2 = Player('B', 1)
    p2.closed = [Tile(0, 'TON'), Tile(0, 'TON')]
    print('P2 can pon:', Tile(0, 'TON') in p2.closed)
    p2.pon(Tile(0, 'TON'), 1)
    print('P2 closed hand:')
    for i in p2.closed:
        print(i.to_string().replace('\n', ' '), end = ' ')
    print('P2 open hand:')
    for i in p2.open:
        print(i)
    
    print('\n')  
    print('chi tests')
    p3 = Player('C', 2)
    p3.closed = [Tile(1, 'Man'), Tile(2, 'Man'), Tile(3, 'Man'), Tile(7, 'Man'), Tile(8, 'Man'), 
                 Tile(9, 'Man'), Tile(0, 'TON'), Tile(0, 'TON'), Tile(0, 'TON')]
    print('P3 can chi 1 man:', p3.can_chi(Tile(1, 'Man')))
    print('P3 can chi 2 man:', p3.can_chi(Tile(2, 'Man')))
    print('P3 can chi 3 man:', p3.can_chi(Tile(3, 'Man')))
    print('P3 can chi 4 man:', p3.can_chi(Tile(4, 'Man')))
    print('P3 can chi 5 man:', p3.can_chi(Tile(5, 'Man')))
    print('P3 can chi 6 man:', p3.can_chi(Tile(6, 'Man')))
    print('P3 can chi 7 man:', p3.can_chi(Tile(7, 'Man')))
    print('P3 can chi 8 man:', p3.can_chi(Tile(8, 'Man')))
    print('P3 can chi 9 man:', p3.can_chi(Tile(9, 'Man')))
    print('P3 can chi TON:', p3.can_chi(Tile(0, 'TON')))
    #p3.chi(Tile(2, 'Man'), 0)
    for i in p3.closed:
        print(i.to_string().replace('\n', ' '), end = ' ')
        
    print('\n')        
    print('kan tests:')
    p3.next_tile = Tile(0, 'TON')
    print('P3 can open kan 1 man:', p3.can_open_kan(Tile(1, 'Man')))
    print('P3 can open kan 9 man:', p3.can_open_kan(Tile(9, 'Man')))
    print('P3 can open kan TON:', p3.can_open_kan(Tile(0, 'TON')))
    print('P3 can closed kan TON:', p3.can_closed_kan())
    p3.closed_kan(0)
    print('P3.closed =')
    for i in p3.closed:
        print(i.to_string().replace('\n', ' '), end = ' ')
    print()
    p3.closed_kan(9)
    print('P3.closed =')
    for i in p3.closed:
        print(i.to_string().replace('\n', ' '), end = ' ')
    print()
    p3.closed_kan(6)
    print('P3.closed =')   
    for i in p3.closed:
        print(i.to_string().replace('\n', ' '), end = ' ')
    print()
    print('P3.open =')
    for t in p3.open:
        for i in t[0]:
            print(i.to_string().replace('\n', ' '), end = ' ')
        
    print('\n')
    print('added kan tests:')
    p4 = Player('D', 3)
    p4.closed = [Tile(1, 'Man'), Tile(2, 'Man'), Tile(3, 'Man'), Tile(7, 'Man'), Tile(8, 'Man'), 
                 Tile(9, 'Man')]
    p4.next_tile = Tile(0, 'TON')
    p4.open = [([Tile(1, 'Man'), Tile(1, 'Man'), Tile(1, 'Man')], 2),
               ([Tile(0, 'TON'), Tile(0, 'TON'), Tile(0, 'TON')], 1),
               ([Tile(2, 'Man'), Tile(3, 'Man'), Tile(4, 'Man')], 0)]
    print('P4.closed =')
    for i in p4.closed:
        print(i.to_string().replace('\n', ' '), end = ' ')
    print()
    print('P4 can added kan:', p4.can_added_kan())
    p4.added_kan(0)
    print('P4.open =')
    for t in p4.open:
        for i in t[0]:
            print(i.to_string().replace('\n', ' '), end = ' ')
    p4.added_kan(1)
    print()
    print('P4.open =')
    for t in p4.open:
        for i in t[0]:
            print(i.to_string().replace('\n', ' '), end = ' ')
    p4.added_kan(2)
    print()
    print('P4.open =')
    for t in p4.open:
        for i in t[0]:
            print(i.to_string().replace('\n', ' '), end = ' ')
    print()
    print('P4.closed =')
    for i in p4.closed:
        print(i.to_string().replace('\n', ' '), end = ' ')
        
    
     
    
    
        
      
