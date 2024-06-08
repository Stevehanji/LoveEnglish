from Tool.Variable import *
import os

class Object:
    screen_scroll = 0
    bg_scroll = 0
    TextBoard = ""
    CorrectGate = None
    event = None
    NextLevel = None
    Level = 1
    JumpScared = False
    IsShowBoard = False
    ShowGateLocked = False  
    IsShowDoorLocked = False
    IsWon = False

class SpriteSheet():
	def __init__(self, image):
		self.sheet = image

	def get_image(self, frame, width, height, scale, colour):
		image = pygame.Surface((width, height))#.convert_alpha()
		image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
		image = pygame.transform.scale(image, (width * scale, height * scale))
		image.set_colorkey(colour)

		return image

animation_list = {}
animation_step = os.listdir("Asset/Game/Player")
width = 32
SIZE_Player = 3

for animation in animation_step:
    sprite = []
    img = pygame.image.load(f"Asset/Game/Player/{animation}")

    for x in range(img.get_width() // width):
        sprite.append(SpriteSheet(img).get_image(x, 32, 32, SIZE_Player, (0,0,0)))
    
    animation_list[animation.replace(".png", "")] = sprite

SCROLL_THRESH = 700

GATE_GROUP = pygame.sprite.Group()
WOODENBOARD_GROUP = pygame.sprite.Group()
DOOR_GROUP = pygame.sprite.Group()

block_list = []
path_block = "Asset/Game/Editor"

Block_List_File = sorted(os.listdir(path_block), key=lambda x: int(x.split('.')[0]))
for block in Block_List_File:
    block_list.append(pygame.image.load(os.path.join(path_block, block)))