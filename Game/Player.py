# from Tool.Variable import *
# from Game.world import *
# from Game.Variable_Game import *
from Game.Variable_Game import *
from Tool.Sound_List import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5
        self.move_left = False
        self.move_right = False
        self.move_up = False
        self.move_down = False
        self.current_action = "idle"
        self.current_index = 0
        self.update_animation_time = 7

        self.last_time = pygame.time.get_ticks()
        self.direction = False
        self.jump = False
        self.vel_y = 0
        self.in_air = False
        self.GRAVITY = 1

        self.image = animation_list[self.current_action][self.current_index]
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.width = self.image.get_width() - (SIZE_Player ** 2 * 2)
        self.height = self.image.get_height() - (SIZE_Player ** 2 * 2)

        self.dx = 0
        self.dy = 0
        self.world = None

        self.CountSound = 0
    
    def SlientPlayer(self):
        self.move_left = False
        self.move_right = False
        self.jump = False

    def LoadWorld(self, world):
        self.world = world
    
    def update_action(self):
        try:
            self.image = animation_list[self.current_action][self.current_index]
        
        except:
            self.current_index = 0
            self.image = animation_list[self.current_action][self.current_index]

        self.current_action = "idle"

        if self.move_left or self.move_right:
            self.current_action = "run"
        
        current_time = pygame.time.get_ticks()

        if current_time - self.last_time >= self.update_animation_time * 10:
            self.last_time = current_time
            self.current_index += 1
            
            if self.current_index >= len(animation_list[self.current_action]):
                self.current_index = 0
    
    def collideret_player_y(self, block_rect):
        jump_and_fall = [False, False]
        if self.vel_y < 0:
            self.vel_y = 0
            self.dy = block_rect.bottom - (self.rect.y + ((SIZE_Player ** 2) * 2))
            jump_and_fall[0] = True
                
        elif self.vel_y >= 0:
            self.vel_y = 0
            self.in_air = False
            self.dy = block_rect.top - ((self.rect.y + ((SIZE_Player ** 2) * 2)) + self.height - 10)
            jump_and_fall[1] = True
        
        return jump_and_fall

    def rect_player_x(self):
        return (self.rect.x + (SIZE_Player ** 2) + 8) + self.dx, self.rect.y + ((SIZE_Player ** 2) * 2), self.width - 16, self.height - 10

    def rect_player_y(self):
        return self.rect.x + (SIZE_Player ** 2) + 10, self.rect.y + ((SIZE_Player ** 2) * 2) + self.dy, self.width - 20, self.height - 10
    
    def FootStepSound(self):
        # print(self.CountSound)
        # if self.jump and self.in_air == False:
            # Sound_List["FootstepGrass"].play()

        if (self.move_left or self.move_right) and Object.Level == 1:
            if self.CountSound == 0:
                Sound_List["FootstepGrass"].play()
                self.CountSound += 1
        
            elif self.CountSound not in range(17):
                self.CountSound = 0
        
            else:
                self.CountSound += 1
        
                # Sound_List["FootstepGrass"].play()
            # self.CountSound = 0
       
    def collideret_player(self):
        for tile in self.world.obstacle_list:
            if tile[1].colliderect(self.rect_player_x()):
                self.dx = 0
                self.FootStepSound()
            
            if tile[1].colliderect(self.rect_player_y()):
                self.collideret_player_y(tile[1])
                self.FootStepSound()
    
    def SoundJump(self):
        if self.CountSound == 0:
            Sound_List["jump"].play()
            self.CountSound += 1

    def move(self):
        self.dx = 0
        self.dy = 0

        Object.screen_scroll = 0

        if self.move_left:
            self.dx = -self.speed
            self.direction = True
        
        elif self.move_right:
            self.dx = self.speed
            self.direction = False
        
        if self.jump and self.in_air == False:
            self.vel_y = -17
            self.in_air = True
            self.CountSound = 0
        
        if self.jump:
            self.SoundJump()
        
        self.vel_y += self.GRAVITY

        if self.vel_y > 14:
            self.vel_y
            
            if self.jump == False:
                self.CountSound = 0
        
        self.dy += self.vel_y

        self.collideret_player()

        self.rect.x += self.dx
        self.rect.y += self.dy

        if (self.rect.right > screen_width - SCROLL_THRESH and Object.bg_scroll < (self.world.level_length * 100) - screen_width) or \
        (self.rect.left < SCROLL_THRESH and Object.bg_scroll > abs(self.dx)):
            self.rect.x -= self.dx
            Object.screen_scroll = -self.dx
        
    
    # def move_test(self, speed = 5):
    #     dx = 0
    #     dy = 0

    #     if self.move_left:
    #         dx = -speed
        
    #     if self.move_right:
    #         dx = speed
        
    #     if self.move_up:
    #         dy = -speed
        
    #     if self.move_down:
    #         dy = speed

    #     for tile in world.obstacle_list:
    #         if tile[1].colliderect((self.rect.x + (SIZE_Player ** 2) + 8) + dx, self.rect.y + ((SIZE_Player ** 2) * 2), self.width - 16, self.height - 10):
    #             dx = 0
            
    #         if tile[1].colliderect(self.rect.x + (SIZE_Player ** 2) + 10, self.rect.y + ((SIZE_Player ** 2) * 2) + dy, self.width - 20, self.height - 10):
    #             if self.vel_y < 0:
    #                 print("is jumping")
                
    #             elif self.vel_y >= 0:
    #                 print("is falling")
        
    #     self.rect.x += dx
    #     self.rect.y += dy
    
    def draw(self):
        # ScreenGame.blit(pygame.transform.flip(self.image,self.direction,False), self.rect)
        screen.blit(pygame.transform.flip(self.image,self.direction,False), self.rect)
    
    def update(self):
        self.move()
        self.update_action()