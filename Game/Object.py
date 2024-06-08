from Tool.Variable import *
from Game.Variable_Game import *
from Tool.image_game import *
from Tool.img import *
from Game.Other import *

class Gate(pygame.sprite.Sprite):
    def __init__(self, x, y, CorrectGate, LockGate, GoToLevel = None):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.CorrectGate = CorrectGate
        self.LockGate = LockGate

        self.GoToLevel = GoToLevel

        self.image = image_game["Editor-11"]
        self.image = pygame.transform.scale(self.image, (150,200))
        self.rect = self.image.get_rect(topleft = (self.x, self.y - 100))

        self.ImageContact = pygame.transform.scale(img_list["Contact"], (100,100))
        self.ImageContactRect = self.ImageContact.get_rect(topleft = (self.x + 20, self.y - 200))

        self.NewRect = pygame.Rect(self.rect.x + 30, self.rect.y, self.rect.w - 30 * 2, self.rect.h)
    
    def update(self, player, Contact):
        if self.NewRect.colliderect(player.rect):
            screen.blit(self.ImageContact, self.ImageContactRect)
            if Contact:
                if self.LockGate == False:
                    if self.CorrectGate:
                        Object.CorrectGate = True
                        Object.NextLevel = self.GoToLevel
                    
                    else:
                        Object.CorrectGate = False
                        Object.JumpScared = True
                    
                    player.SlientPlayer()
                
                else:
                    player.SlientPlayer()
                    Object.ShowGateLocked = True

        self.rect.x += Object.screen_scroll
        self.ImageContactRect.x += Object.screen_scroll
        self.NewRect.x += Object.screen_scroll

class WoodenBoard(pygame.sprite.Sprite):
    def __init__(self, x, y, text):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.image = image_game["Editor-13"]
        self.image = pygame.transform.scale(self.image, (50,50))
        self.rect = self.image.get_rect(topleft = (self.x, self.y))

        self.ImageContact = pygame.transform.scale(img_list["Contact"], (50, 50))
        self.ImageContactRect = self.ImageContact.get_rect(topleft = (self.x + 5, self.y - 75))

        # self.text = "Go through the gate on the left"
        self.text = text
    
    def update(self, player, Contact):
        if self.rect.colliderect(player.rect):
            screen.blit(self.ImageContact, self.ImageContactRect)
            if Contact:
                player.SlientPlayer()
                Object.IsShowBoard = True
                Object.TextBoard = self.text

        self.rect.x += Object.screen_scroll
        self.ImageContactRect.x += Object.screen_scroll
    
class Door(pygame.sprite.Sprite):
    def __init__(self,x,y,w,h, img, clocked):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.image = pygame.transform.scale(img, (self.w, self.h))
        self.clocked = clocked
        self.rect = self.image.get_rect(topleft = (self.x, self.y))
        self.ImageContact = pygame.transform.scale(img_list["Contact"], (self.w - 50, self.h // 2))
        self.ImageContactRect = self.ImageContact.get_rect(topleft = (self.x + 20, self.y - self.h // 2))

    def update(self, player, Contact):
        if self.rect.colliderect(player.rect):
            screen.blit(self.ImageContact, self.ImageContactRect)

            if Contact:
                player.SlientPlayer()
                if self.clocked:
                    Object.IsShowDoorLocked = True
                
                else:
                    Object.IsWon = True
        
        self.rect.x += Object.screen_scroll
        self.ImageContactRect.x += Object.screen_scroll

class Cave(pygame.sprite.Sprite):
    def __init__(self,x,y, clocked):
        self.x = x
        self.y = y
        self.image = pygame.transform.scale(img, (100,200))
        self.clocked = clocked
        self.rect = self.image.get_rect(topleft = (self.x, self.y))
        self.ImageContact = pygame.transform.scale(img_list["Contact"], (50, 50))
        self.ImageContactRect = self.ImageContact.get_rect(topleft = (self.x + 5, self.y - 75))

    def update(self, player, Contact):
        if self.rect.colliderect(player.rect):
            screen.blit(self.ImageContact, self.ImageContactRect)
        
        self.rect.x += Object.screen_scroll
        self.ImageContactRect.x += Object.screen_scroll