from pygame_template import *

TILE_NUMS = 20
TILE_SIZE = 600 // TILE_NUMS
TOTAL_TILES = 12
UP, RIGHT, DOWN, LEFT = 0, 1, 2, 3

class Tile:
    def __init__(self, tile_index=-1):
        self.image = pygame.Surface((TILE_SIZE,TILE_SIZE), pygame.SRCALPHA)
        self.rules = []     # up, right, down, left
        self.valid_states = list(range(TOTAL_TILES))
        self.collapsed = False        
        self.tile_index = tile_index
        self.get_correct_tile()

    def get_correct_tile(self):
        pygame.draw.rect(self.image, 'gray', (0,0,TILE_SIZE,TILE_SIZE), 0)  
        match self.tile_index:
            case 11:     # top left curve
                pygame.draw.circle(self.image, 'black', (0, 0), TILE_SIZE//2 + TILE_SIZE // 8 // 2, TILE_SIZE // 8)
                self.rules = [1,0,0,1]
                
            case 10:     # bottom left curve
                pygame.draw.circle(self.image, 'black', (0, TILE_SIZE), TILE_SIZE//2 + TILE_SIZE // 8 // 2, TILE_SIZE // 8)
                self.rules = [0,0,1,1]
                
            case 9:     # bottom right curve
                pygame.draw.circle(self.image, 'black', (TILE_SIZE, TILE_SIZE), TILE_SIZE//2 + TILE_SIZE // 8 // 2, TILE_SIZE // 8)
                self.rules = [0,1,1,0]
                
            case 8:     # top right curve
                pygame.draw.circle(self.image, 'black', (TILE_SIZE, 0), TILE_SIZE//2 + TILE_SIZE // 8 // 2, TILE_SIZE // 8)
                self.rules = [1,1,0,0]
                
            case 7:     # left line half 
                pygame.draw.line(self.image, 'black', (TILE_SIZE//2, TILE_SIZE//2), (0, TILE_SIZE//2), TILE_SIZE // 8)
                self.rules = [0,0,0,1]
            case 6:     # down line half
                pygame.draw.line(self.image, 'black', (TILE_SIZE//2, TILE_SIZE//2), (TILE_SIZE//2, TILE_SIZE), TILE_SIZE // 8)
                self.rules = [0,0,1,0]
            case 5:     # right line half
                pygame.draw.line(self.image, 'black', (TILE_SIZE//2, TILE_SIZE//2), (TILE_SIZE, TILE_SIZE//2), TILE_SIZE // 8)
                self.rules = [0,1,0,0]
            case 4:     # top line half
                pygame.draw.line(self.image, 'black', (TILE_SIZE//2, 0), (TILE_SIZE//2, TILE_SIZE//2), TILE_SIZE // 8)
                self.rules = [1,0,0,0]
            case 3:     # full cross
                pygame.draw.line(self.image, 'black', (TILE_SIZE//2, 0), (TILE_SIZE//2, TILE_SIZE), TILE_SIZE // 8)
                pygame.draw.line(self.image, 'black', (0,TILE_SIZE//2), (TILE_SIZE,TILE_SIZE//2), TILE_SIZE // 8)
                self.rules = [1,1,1,1]
            case 2:     # vertical line full
                pygame.draw.line(self.image, 'black', (TILE_SIZE//2, 0), (TILE_SIZE//2, TILE_SIZE), TILE_SIZE // 8)
                self.rules = [1,0,1,0]
            case 1:     # horizontal line full
                pygame.draw.line(self.image, 'black', (0,TILE_SIZE//2), (TILE_SIZE,TILE_SIZE//2), TILE_SIZE // 8)
                self.rules = [0,1,0,1]
            case 0:     # 0 index default blank
                self.rules = [0,0,0,0]
            case _: 
                self.image.fill((10,10,10,255))
                pygame.draw.line(self.image, (50,50,50,50), (0,TILE_SIZE//2), (TILE_SIZE,TILE_SIZE//2), max(TILE_SIZE // 50,1))
                pygame.draw.line(self.image, (50,50,50,50), (TILE_SIZE//2, 0), (TILE_SIZE//2, TILE_SIZE), max(TILE_SIZE // 50,1))
                
    def draw(self, screen, x, y):
        screen.blit(self.image, (x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE))
        
class run(APP):
    def init(self):
        self.WIDTH = 600
        self.HEIGHT = 600
        self.window_title = 'Wave Function Collapse'
        self.limit_fps = True
        # self.FPS = 8
    
    def setup(self):
        self.grid = [[Tile() for y in range(TILE_NUMS)] for x in range(TILE_NUMS)]
        self.start_propagation()
        
    def start_propagation(self):
        # choose random first tile
        x,y = random.randint(0,TILE_NUMS-1), random.randint(0,TILE_NUMS-1)
        tile = self.grid[x][y]
        # set first tile
        tile = Tile(random.randint(0,TOTAL_TILES-1))
        tile.get_correct_tile()
        tile.collapsed = True
        self.grid[x][y] = tile
        self.propagate_constraints(x,y)
                
    def propagate_constraints(self, x, y):
        tile = self.grid[x][y]
        neighbors = [
            (x, y - 1, UP, DOWN),  # Above
            (x + 1, y, RIGHT, LEFT),  # Right
            (x, y + 1, DOWN, UP),  # Below
            (x - 1, y, LEFT, RIGHT)  # Left
        ]
        # set all entropies
        for nx, ny, my_side, their_side in neighbors:
            if 0 <= nx < TILE_NUMS and 0 <= ny < TILE_NUMS:
                neighbor = self.grid[nx][ny]
                if not neighbor.collapsed:
                    neighbor.valid_states = [state for state in neighbor.valid_states if Tile(state).rules[their_side] == tile.rules[my_side]]
        
    def collapse_next(self):
        min_entropy = float('inf')
        best_tile = None
        best_x, best_y = None, None
        # Find the tile with the lowest entropy
        for x in range(TILE_NUMS):
            for y in range(TILE_NUMS):
                tile = self.grid[x][y]
                if not tile.collapsed:
                    entropy = len(tile.valid_states)
                    if entropy <= min_entropy:
                        min_entropy = entropy
                        best_tile = tile
                        best_x, best_y = x, y
        if best_tile and best_tile.valid_states:
            # Collapse the best tile to a single valid state
            chosen_state = random.choice(best_tile.valid_states)
            new_tile = Tile(chosen_state)
            new_tile.collapsed = True  # Mark as collapsed
            self.grid[best_x][best_y] = new_tile
            self.propagate_constraints(best_x, best_y)

    def draw(self):            
        for y in range(TILE_NUMS):
            for x in range(TILE_NUMS):
                self.grid[x][y].draw(self.screen, x, y)
                
    def update(self):
        # if pygame.key.get_just_pressed()[pygame.K_SPACE]: self.collapse_next()
        # if pygame.key.get_pressed()[pygame.K_SPACE]: self.collapse_next()
        self.collapse_next()
        
run()