# from Game.Variable_Game import *
# import Game.Player

import Game.Player
from Game.Variable_Game import *
from Tool.image_game import *
# import pandas as pd
from Game.Object import *
from Game.StartUpFile import *

# pd = importlib.import_module("pandas")

class Block_Special(Object):
    def __init__(self, x, y, tile_size):
        self.x = x
        self.y = y
        close_img = pygame.transform.scale(img_list[1], (tile_size, tile_size))
        open_img = pygame.transform.scale(img_list[2], (tile_size, tile_size))
        self.Img_list = [close_img, open_img]

        self.image = self.Img_list[0]


        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y - 70

        self.time_stop = 200
        self.last_time = pygame.time.get_ticks()
    
    def update(self, player):
        current_time = pygame.time.get_ticks()

        if self.rect.colliderect(player.rect_player_x()):
            player.dx = 0
        if self.rect.colliderect(player.rect_player_y()):
            is_collidert = player.collideret_player_y(self.rect)

            if is_collidert[0]:
                self.image = self.Img_list[1]
                self.last_time = current_time
        else:
            if current_time - self.last_time > self.time_stop:
                self.image = self.Img_list[0]

    
    def draw(self):
        self.rect.x += self.screen_scroll
        screen.blit(self.image, self.rect)

class World():
    def __init__(self):
        background1 = image_game["Background-background1"]
        background2 = image_game["Background-background2"]
        self.background1 = pygame.transform.scale(background1, (screen_width, screen_height))
        self.background2 = pygame.transform.scale(background2, (screen_width, screen_height))
        self.ResetAll()
        self.NextLevel = None
    
    def ResetAll(self):
        self.obstacle_list = []

    def CheckInDoor(self, pos, Lst : list, GetNextLevel = True):
        NLst = [tuple(element[:-1]) for element in Lst]
        if pos in NLst: 
            if GetNextLevel:
                self.NextLevel = Lst[NLst.index(pos)][2]
            return True
        return False
    
    def process_data(self, data, tile_size = 50):
        self.level_length = len(data[0])

        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile != -1 and tile != 18:
                    IMG = block_list[tile]
                    IMG = pygame.transform.scale(IMG, (tile_size, tile_size))

                    if tile == 12:
                        player = Game.Player.Player(x * tile_size, y * tile_size + SIZE_Player)
                    
                    elif tile == 11:
                        CorrectGate = False
                        ClockGate = False
                        
                        if self.CheckInDoor((y,x), CorrectGateList[Object.Level - 1]):
                            CorrectGate = True
                    
                        if (y,x) in GateClockList[Object.Level - 1]:
                            ClockGate = True
                        
                        gate = Gate(x * tile_size, y * tile_size, CorrectGate, ClockGate, self.NextLevel)
                        GATE_GROUP.add(gate)

                        self.NextLevel = None
                    
                    elif tile == 13:
                        text = "Go through the gate on the left"

                        if Object.Level == 2:
                            text = "Parkour And Open The Door Over there"

                        WB = WoodenBoard(x * tile_size, y * tile_size, text)
                        WOODENBOARD_GROUP.add(WB)
                    
                    elif tile == 14 or tile == 15:
                        ClockedDoor = True
                        width = 150
                        height = 200

                        if tile == 15:
                            width = 300
                            height = 300
                            ClockedDoor = False

                        DOOR = Door(x * tile_size, y * tile_size - height + 100, width, height, 
                                      IMG, ClockedDoor)
                        DOOR_GROUP.add(DOOR)

                    else:
                        img_rect = IMG.get_rect()
                        img_rect.x = x * tile_size
                        img_rect.y = y * tile_size
                        tile_data = (IMG, img_rect)
                        self.obstacle_list.append(tile_data)
        
        return player
    
    def draw(self):
        for tile in self.obstacle_list:
            tile[1][0] += Object.screen_scroll
            screen.blit(tile[0],tile[1])
    
    def DrawBackground(self):
        screen.blit(self.background1, (0,0))
        screen.blit(self.background2, (0,0))