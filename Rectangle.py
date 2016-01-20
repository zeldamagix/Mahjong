from tkinter.constants import CENTER


class Rectangle:
    def __init__(self, t: 'Tile', x: int, y: int, w: int, h: int, bw: int):
        ''' tile attributes'''
        self.tile = t
        ''' coordinates and dimensions'''
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.border_width = bw
        ''' how much the rectangle is raised by'''
        self.raised = 0
     
    ''' draw the rectangle on a canvas c'''   
    def draw(self, c: 'Canvas'):
        if self.tile != None:
            c.create_rectangle(self.x, self.y-self.raised, self.x+self.width, self.y-self.raised+self.height,
                               fill = 'white', activewidth = self.border_width)
            c.create_text((2*self.x+self.width)/2, (2*(self.y-self.raised)+self.height)/2, 
                          text=self.tile.to_string(), fill = self.tile.return_color(), justify = CENTER)
        else:
            c.create_rectangle(self.x, self.y, self.x+self.width, self.y+self.height)
    
    ''' checks if a coordinate is inside the rectangle, left-justified'''
    def inside(self, x: int, y: int) -> bool:
        return ((x >= self.x) and (y >= self.y-self.raised) and (x < self.x+self.width) and 
                (y <= self.y-self.raised+self.height))
    
    ''' move the rectangle up and down'''
    def upper(self):
        self.raised = self.height//5
        
    def lower(self):
        self.raised = 0
    
    ''' check if rectangle raised'''
    def is_raised(self) -> bool:
        return self.raised != 0
    
    
    
    
