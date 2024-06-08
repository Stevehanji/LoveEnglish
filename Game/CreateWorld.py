from Game.Variable_Game import *
from Tool.image_game import *
# import pandas
from Tool.Variable import *
from Tool.Create_Button import *
# from datetime import datetime
from Tool.Button import *
from Tool.TextInput import *
import importlib

pandas = importlib.import_module("pandas")
# datetime = importlib
WoodenBoardText_X = 100
WoodenBoardText_Y = screen_height - 100 * 2 + 50
WoodenBoardText_W = screen_width - WoodenBoardText_X * 2
WoodenBoardText_H = 100
WoodenBoardText = TextInputBox(WoodenBoardText_X,
                               WoodenBoardText_Y,
                               WoodenBoardText_W,
                               WoodenBoardText_H)

WoodenBoardText.SetFont(50, Font_path)

# PosStandard = (screen_height - self.Height // 2 - edge // 2,edge, edge)

def GetBlockEditPage(page, block_list):
    return page * 11 if page * 11 < len(block_list) else len(block_list) - (page - 1) * 11

df = pandas.read_excel("StoreData\\Game\\MapEditing.xlsx", header=None)
MAPDATA = df.values
class CreateWorld:
    def __init__(self):
        background = image_game["Background-background1"]
        self.background = pygame.transform.scale(background,(screen_width,screen_height))
        background1 = image_game["Background-background2"]
        self.background1 = pygame.transform.scale(background1,(screen_width,screen_height))
        self.ResetAll()
        self.IsButtonActive = False
        
    def ResetAll(self):
        self.bg_x = 0
        self.Height = 200
        self.bg_y = -self.Height
        self.ROW = 18
        self.COL = 26
        self.row = self.ROW
        self.col = self.COL
        self.speed = 5
        self.move_left = False
        self.move_right = False
        # self.map_data = [[-1 for i in range(self.col)] for j in range(self.row)]

        self.map_data = MAPDATA

        self.show = True
        self.PutBlockHold = False
        self.style = None
        self.so_luong = 0
        self.page = 1
        self.choose_block = False
        self.choose_block_x = None
        self.choose_block_y = None
        self.speed_block = 5
        self.move_up = False
        self.move_down = False
        self.ApperIconToChoose = True

        self.PosCorrectGate = []
        self.PosGateClock = []
        self.TextPosWoodenBoard = {}
        self.PosClockDoor14 = []

        self.IsTyping = False
    
    # def ResetAllTextBox(self, listInputBoxs : list):
        # for InputBox in listInputBoxs:
        # InputBox.Is_Input = False
        # InputBox.showCurso(False)
    
    def IsInsideRect(self, rect, mouse_x, mouse_y):
        if mouse_x > rect.x and rect.x + rect.w > mouse_x and mouse_y > rect.y and mouse_y < rect.y + rect.h:
            return True
        
        return False

    def update_map_data(self, map_data, style, bg_x, bg_y, hold = False, page = None, block_list = []):
        try:
            mouse_x,mouse_y = pygame.mouse.get_pos()

            if not self.IsInsideRect(SaveCreateWorldButton, mouse_x, mouse_y):
                if mouse_y < 700 and style != None:
                    mouse_x += abs(bg_x)
                    mouse_y += abs(bg_y)
                    mouse_x //= 50
                    mouse_y //= 50

                    if style == -1:
                        if (mouse_x, mouse_y) in self.PosCorrectGate:
                            self.PosCorrectGate.remove((mouse_x, mouse_y))

                    map_data[mouse_y][mouse_x] = style + (page - 1) * 11 if style != -1 else -1
                
                elif mouse_y > 700 and hold == False and self.ApperIconToChoose:
                    mouse_x //= 100

                    if (mouse_y > 750 and mouse_y < 750 + 75) and mouse_x != 0 and mouse_x < GetBlockEditPage(page, block_list) + 1:
                        NewStyle = mouse_x - 1

                        return NewStyle, None, None
                    
                    return None, None, None

                elif style == None and mouse_y < 700:
                    if self.ApperIconToChoose:
                        mouse_x += abs(bg_x)
                        mouse_y += abs(bg_y)
                        mouse_x //= 50
                        mouse_y //= 50
                        if map_data[mouse_y][mouse_x] != -1:
                            return None, mouse_x, mouse_y
            
                elif self.ApperIconToChoose == False and mouse_y > 700:
                    return None, self.choose_block_x, self.choose_block_y
        
        except:
            pass

        return self.style, None, None
    
    def ButtonTick(self, ListInput : list, x, y, w = None, h = None, text = None, padding = 5):
        if text == None: raise TypeError("Text Not None")
        ButtonTick = pygame.Rect(x,y,w,h)
        pygame.draw.rect(screen, "black",(x, y, w, h))
        pygame.draw.rect(screen, "gray",(ButtonTick.x + padding,
                                         ButtonTick.y + padding,
                                         ButtonTick.w - padding * 2,
                                         ButtonTick.h - padding * 2))
    
        font(text, 35, "white",(175,0),[ButtonTick.x,
                                                    ButtonTick.y,
                                                    ButtonTick.w,
                                                    ButtonTick.h])

        if B.Is_Clicked(ButtonTick):
            PosTick = (self.choose_block_x, self.choose_block_y)
            if PosTick in ListInput:
                ListInput.remove(PosTick)
            
            else:
                ListInput.append(PosTick)

        if (self.choose_block_x, self.choose_block_y) in ListInput:
            screen.blit(pygame.transform.scale(image_game["Other-Tick"],
                                            (100 - padding * 3,100 - padding * 3)),
                                            (ButtonTick.x - 10,
                                             ButtonTick.y - 10))
        return ListInput

    def WoodenBoard(self):
        if B.Is_Clicked(pygame.Rect(WoodenBoardText_X, WoodenBoardText_Y,
                                    WoodenBoardText_W, WoodenBoardText_H)):
            self.IsTyping = True
        
        # WoodenBoardText.adjust_value()
        if (self.choose_block_x, self.choose_block_y) not in self.TextPosWoodenBoard:
            self.TextPosWoodenBoard[(self.choose_block_x, self.choose_block_y)] = ""
            WoodenBoardText.adjust_value("", Object.event)
        
        else:
            if self.IsTyping == False:
                WoodenBoardText.adjust_value(
                        self.TextPosWoodenBoard[(self.choose_block_x, self.choose_block_y)], 
                        Object.event
                    )
            
            else:
                self.TextPosWoodenBoard[(self.choose_block_x, self.choose_block_y)] = WoodenBoardText.get_value()

        if self.IsTyping == False:
            WoodenBoardText.Is_Input = False
            WoodenBoardText.showCurso = False
        
        WoodenBoardText.draw(Object.event)

    def TableChooseGate(self):
        edge = 75
        self.PosCorrectGate = self.ButtonTick(self.PosCorrectGate, 100, screen_height - self.Height // 2 - edge // 2,
                            edge, edge, text = "Correct Gate")
        
        self.PosGateClock = self.ButtonTick(self.PosGateClock, 500, screen_height - self.Height // 2 - edge // 2,
                            edge, edge, text = "Clock Gate")

    def Door14(self):
        edge = 75
        self.ButtonTick(self.PosClockDoor14, 100, screen_height - self.Height // 2 - edge // 2,
                            edge, edge, text = "Clock Door")

    def Door15(self):
        edge = 75
        self.ButtonTick(self.PosClockDoor14, 100, screen_height - self.Height // 2 - edge // 2,
                            edge, edge, text = "Clock Door")

    def CaveGate(self):
        edge = 75
        self.ButtonTick(self.PosClockDoor14, 100, screen_height - self.Height // 2 - edge // 2,
                            edge, edge, text = "Clock Cave")

    def run(self, display):
        self.col = self.so_luong + self.COL

        if len(self.map_data[0]) < self.col:
            for i in range(len(self.map_data)):
                for j in range(self.col - len(self.map_data)):
                    self.map_data[i].append(-1)

        screen.blit(self.background,(self.bg_x,self.bg_y))
        screen.blit(self.background1,(self.bg_x,self.bg_y))
        screen.blit(self.background,(self.bg_x + self.background.get_width(),self.bg_y))
        screen.blit(self.background1,(self.bg_x + self.background1.get_width(),self.bg_y))


        if self.PutBlockHold:
            if pygame.mouse.get_pressed()[0]:
                self.update_map_data(self.map_data, self.style, self.bg_x, self.bg_y, True, page=self.page)
            
            if pygame.mouse.get_pressed()[2]:
                self.update_map_data(self.map_data, -1, self.bg_x, self.bg_y, True, page=self.page)
        
        if self.show:
            for y in range(1,self.row):
                for x in range(1,self.col):
                    pygame.draw.line(screen, "white",(x * 50 + self.bg_x, 0 - self.Height), 
                                    (x * 50 + self.bg_x, 700))
                    
                    pygame.draw.line(screen, "white",(0, y * 50 + self.bg_y), 
                                    (screen_width, y * 50 + self.bg_y))

        for y in range(self.row):
            for x in range(self.col):
                if self.map_data[y][x] != -1:
                    IMG = pygame.transform.scale(block_list[self.map_data[y][x]],(50,50))
                    screen.blit(IMG,(x * 50 + self.bg_x, y * 50 + self.bg_y))
            
        pygame.draw.rect(screen, "darkgreen", (0,700,screen_width,screen_height - 700))

        if self.style != None:
            pygame.draw.rect(screen, "red", ((self.style + 1) * 100 - 5, 750 - 5, 85, 85))
        

        if self.ApperIconToChoose:
            for IndexImage in range(GetBlockEditPage(self.page, block_list)):
                try:
                    IMG = pygame.transform.scale(block_list[IndexImage + ((self.page - 1) * 11)], (75,75))
                    IMGRect = IMG.get_rect(topleft = ((IndexImage + 1) * 100, 750))
                    screen.blit(IMG, IMGRect)
                except:
                    pass
        
        if self.choose_block_x != None and self.choose_block_y != None:
            self.choose_block = True
            draw_rect_alpha(screen, (0,255,0,100), (self.choose_block_x * 50 - abs(self.bg_x), 
                                                    self.choose_block_y * 50 - abs(self.bg_y), 50, 50))
        
        else:
            self.choose_block = False

        if self.choose_block:
            self.ApperIconToChoose = False

            if self.map_data[self.choose_block_y][self.choose_block_x] == 11:
                self.TableChooseGate()
            
            elif self.map_data[self.choose_block_y][self.choose_block_x] == 13:
                self.WoodenBoard()
            
            elif self.map_data[self.choose_block_y][self.choose_block_x] == 14:
                self.Door14()
            
            elif self.map_data[self.choose_block_y][self.choose_block_x] == 15:
                self.Door15()
            
            elif self.map_data[self.choose_block_y][self.choose_block_x] == 18:
                self.Door15()
        else:
            self.ApperIconToChoose = True
            self.IsTyping = False

        
        if self.move_left and self.bg_x < 0: self.bg_x += self.speed
        elif self.move_right: self.bg_x -= self.speed
        if self.move_up and self.bg_y < 0: self.bg_y += self.speed
        elif self.move_down and self.bg_y > -self.Height: self.bg_y -= self.speed

        if self.bg_x % 50 == 0:
            self.so_luong = abs(self.bg_x) // 50

        if SaveCreateWorldButton.draw_Button_with_text("SAVE",25, "white","white", [None, None, 0]):
            SaveFileList = {
                    "PosCorrectGate" : self.PosCorrectGate, 
                    "PosGateClock" : self.PosGateClock,
                    "PosClockDoor14" : self.PosClockDoor14
            }

            SaveFileDictionary = {
                "TextPosWoodenBoard" : self.TextPosWoodenBoard
            }

            # print(SaveFileList)


            for File in SaveFileList:
                resultSaveFileList = ""
                data = SaveFileList[File]
                if len(data) == 0: continue

                for D in data:
                    datax = D[0]; datay = D[1]
                    resultSaveFileList += f"{datay} {datax}\n"

                # print(File + ".txt :",resultSaveFileList.rstrip("\n"))
                f = open(f"{File}.txt", mode = "w")
                f.write(resultSaveFileList.rstrip("\n"))

            # df = pandas.DataFrame(self.map_data)
            # CurrentTime = datetime.now()
            # Time = f"{CurrentTime.year}_{CurrentTime.month}_{CurrentTime.day}_{CurrentTime.hour}_{CurrentTime.minute}_{CurrentTime.second}"
            # df.to_excel(f"StoreData/Map/Map_{Time}.xlsx", index=False, header=False)
            # df.to_excel(f"MapEditing.xlsx", index=False, header=False)


            print("Đã Save")

        font(f"Block Put Hold: {self.PutBlockHold}",25,"red",(10,0))

        return display