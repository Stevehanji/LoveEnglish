from Tool.Variable import *
from Game.world import *
from Game.Player import *
from Tool.Create_Button import *
from Tool.Color import *
from Game.StartUpFile import *
from StoreData.Setting import *
# from Player import *
# from Game.Variable_Game import *

class Game:
    def __init__(self):
        self.world = World()
        self.ResetAll()
        self.SurfaceScreen = pygame.Surface((screen_width, screen_height))
        self.WasFadeBlack = False
        self.TextVietNamese = None

        self.IsTranslate = DataStore.SettingData["PlayGame"]["TranslateToVietName"]

    def FadeBlack(self):
        draw_rect_alpha(screen, (0,0,0,self.CountFadeByFibonacciNum1), (0,0,screen_width, screen_height))

        if self.CountFadeByFibonacciNum1 < 255:
            self.tempFadeByFibonacci = self.CountFadeByFibonacciNum2
            self.CountFadeByFibonacciNum2 += self.CountFadeByFibonacciNum1
            self.CountFadeByFibonacciNum1 = self.tempFadeByFibonacci

            if self.CountFadeByFibonacciNum1 > 255:
                self.CountFadeByFibonacciNum1 = 255
                self.WasFadeBlack = True

    def RemoveAllSprite(self):
        GATE_GROUP.empty()
        WOODENBOARD_GROUP.empty()
        DOOR_GROUP.empty()

    def ResetAll(self):
        Jump_Scare.ResetAll()
        self.world.ResetAll()
        self.PlayerMoveLeft = False
        self.PlayerMoveRight = False
        self.PlayerJump = False
        self.Player = self.world.process_data(MapData[Object.Level - 1])

        self.Player.LoadWorld(self.world)
        self.screen_rect = screen.get_rect()
        self.ContactGate = False
        self.ContactWoodenBoard = False
        Object.screen_scroll = 0
        Object.bg_scroll = 0
        self.TextList = []
        self.CountFadeByFibonacciNum1 = 0
        self.CountFadeByFibonacciNum2 = 1
        self.tempFadeByFibonacci = self.CountFadeByFibonacciNum2
        self.ContactDoor = False

        # 0 : english ; 1 : vietname
        self.styleLanguage = 0
        Object.IsWon = False

    def WordProcessing(self, text : str, Max_Width : int, VietNamese = False):
        sList = text.split(" ")
        StartIndex = 0
        TextList = []

        for IndexText in range(len(sList)):
            NewText = " ".join(sList[StartIndex:IndexText + 1])

            if Max_Width < font(NewText, 75, ReturnFontWidth=True):
                StartIndex = IndexText
                NewTextList = NewText.split(" ")
                
                if IndexText != len(sList) - 1:
                    del NewTextList[-1]
                    NewText = " ".join(NewTextList)
                    TextList.append(NewText)
                
                else:
                    TextStartToEnd = " ".join(NewTextList[:len(NewTextList) - 1])
                    TextList.append(TextStartToEnd)
                    TextList.append(NewTextList[-1])
            
            else:
                if IndexText == len(sList) - 1:
                    TextList.append(NewText)
        
        self.TextList.append(TextList)
    
    def EnglishAndVietNamese(self):
        # Nếu nút là tiếng anh
        if self.styleLanguage == 0:
            IMG = pygame.transform.scale(image_game["Other-England"], (100, 100))
        
        # Nếu nút là tiếng việt
        elif self.styleLanguage == 1:
            IMG = pygame.transform.scale(image_game["Other-VietNam"], (100, 100))

        IMG_rect = IMG.get_rect(topleft = (screen_width - 125, 30))

        if B.Is_Clicked(IMG_rect):
            self.styleLanguage = int(not (self.styleLanguage))

        screen.blit(IMG, IMG_rect)

    def CheckLengthSizeFont(self, text, width, font_size = 75, EAV = [True, True]) -> bool:
        """
            EAV[0] : English
            EAV[1] : VietNamese
        """
        if width < font(text, font_size, ReturnFontWidth=True):
            if len(self.TextList) == 0:
                if EAV[0]:
                    self.WordProcessing(text, width)
                
                if EAV[1]:
                    self.WordProcessing(TranslateToVietNam(text), width)
            
            return True
        
        return False

    def ShowFontManyLine(self, PosStart):
        for y in range(len(self.TextList[self.styleLanguage])):
            font(self.TextList[self.styleLanguage][y], 75, "white", (None, PosStart + y * 75))

    def ShowBoard(self, text):
        draw_rect_alpha(screen, (0,0,0, 100),(0,0,screen_width, screen_height))
        IMG = pygame.transform.scale(image_game["Editor-13"], (image_game["Editor-13"].get_width() - 300,
                                                               image_game["Editor-13"].get_height() - 300))
        screen.blit(IMG, (screen_width // 2 - IMG.get_width() // 2,
                          screen_height // 2 - IMG.get_height() // 2 + 450))
        
        if self.CheckLengthSizeFont(text, IMG.get_width() - 100):
            PosStart = IMG.get_rect().y + 200
            self.ShowFontManyLine(PosStart)

        else:
            if self.styleLanguage == 0:
                font(text, 75, "white",(None, None))
            
            elif self.styleLanguage == 1 and DataStore.SettingData["PlayGame"]["TranslateToVietName"]:
                if self.TextVietNamese == None:
                    self.TextVietNamese = TranslateToVietNam(text)

                if self.CheckLengthSizeFont(self.TextVietNamese, IMG.get_width() - 100, EAV=[False, True]):
                
                    PosStart = IMG.get_rect().y + 200
                    self.ShowFontManyLine(PosStart)
                    
                else:
                    font(self.TextVietNamese, 75, "white", (None, None))

        if DataStore.SettingData["PlayGame"]["TranslateToVietName"]:
            self.EnglishAndVietNamese()
    
    def TextBox(self, text):
        pygame.draw.rect(screen, "black", (0, screen_height - 200, screen_width, screen_height - 200))
        pygame.draw.rect(screen, (255,255,255), (0, screen_height - 200, screen_width, screen_height - 200), 10)

        if self.CheckLengthSizeFont(text, screen_width):
            PosStart = screen_height - 200
            self.ShowFontManyLine(PosStart)
        else:
            if self.styleLanguage == 0:
                font(text, 75, "white", (None, screen_height - 200))
            
            elif self.styleLanguage == 1 and DataStore.SettingData["PlayGame"]["TranslateToVietName"]:
                if self.TextVietNamese == None:
                    self.TextVietNamese = TranslateToVietNam(text)

                if self.CheckLengthSizeFont(self.TextVietNamese, screen_width, EAV=[False, True]):
                    PosStart = screen_height - 200
                    self.ShowFontManyLine(PosStart)
                    
                else:
                    font(self.TextVietNamese, 75, "white", (None, screen_height - 200))

        if DataStore.SettingData["PlayGame"]["TranslateToVietName"]:
            self.EnglishAndVietNamese()

    def NewLevel(self, level):
        Object.Level = level
        Object.CorrectGate = False
        self.RemoveAllSprite()
        self.ResetAll()
        self.WasFadeBlack = False

    def DrawGame(self):
        self.world.DrawBackground()
        if Object.JumpScared == False:
            GATE_GROUP.draw(screen)
            DOOR_GROUP.draw(screen)

            self.world.draw()
            WOODENBOARD_GROUP.draw(screen)

            GATE_GROUP.update(self.Player, self.ContactGate)
            WOODENBOARD_GROUP.update(self.Player, self.ContactWoodenBoard)
            DOOR_GROUP.update(self.Player, self.ContactDoor)

            self.Player.draw()
            self.Player.update()

            if Object.IsShowBoard:
                self.ShowBoard(Object.TextBoard)

            Object.bg_scroll -= Object.screen_scroll
        
        else:
            Jump_Scare.run()
        
        if Object.ShowGateLocked:
            self.TextBox("The Gate Locked")

        elif Object.CorrectGate and self.WasFadeBlack == False:
            self.FadeBlack()
        
        if Object.IsWon:
            self.CountFadeByFibonacciNum1 = 0
            self.CountFadeByFibonacciNum2 = 1
            self.tempFadeByFibonacci = self.CountFadeByFibonacciNum2
        
        if Object.IsShowDoorLocked:
            self.TextBox("The Door Locked")
        
        if self.WasFadeBlack:
            self.NewLevel(Object.NextLevel)

    def RunGame(self, display):
        if Object.IsWon == False:
            self.DrawGame()
            self.ContactGate = False
            self.ContactWoodenBoard = False
            self.ContactDoor = False
        
        elif Object.IsWon == True:
            if self.WasFadeBlack == False: 
                self.FadeBlack()
            
            elif self.WasFadeBlack: 
                screen.fill("black")
                font("You Won",75,"white",(None, None))

        return display

game = Game()