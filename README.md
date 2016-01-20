# Mahjong
Our first draft at a single player mahjong game.

As of now, the game runs but not tested extensively.

Controls currently are:
s: next player
a: reveal all player's tiles
d: draw a tile (only turn player can draw a tile)
r: declare richi (only turn player can declare richi)
n: start a new game

Left Click does multiple things, depends on the state of the game.
left click on the empty rectangle:
1. Nothing if last tile cannot be called and not the next player in line to draw
2. current player gets their tile back (used to remake moves)
3. call a tile if tile can be used in a set
4. draw a tile if next player in line and next player cannot use tile to make a set

left click within the hand:
After drawing a tile:
1. discard a tile
  1.1 exception are raised tiles, which means make a kan
After calling a tile:
1. choose tiles to make the set with. 
  1.1 clicking once chooses it and clicking again unchooses it. 

left click on the open sets
1. Make an added kan for a triplet currently there.
2. clicking on the empty rectangle makes a set after a tile is called. the rectangle only shows up once a full set has been made.


