import pygame
from Tool.Color import *
import importlib

pygame.init()
screen_width = 1300
screen_height = 900

screen = pygame.display.set_mode((screen_width, screen_height))

os = importlib.import_module("os")

class Var_Obj:
    IsJumpApp = False
    Store_FlashCard = {}
    FlashCardTheme = {}
    FlashCardThemeNameList = []
    IsAdmin = False
    IsFinishButtonAdmin = False
    def __init__(self):
        self.DisplayTieuChuanIsShow = True
        self.running = True
        self.style = "dark"
        self.display = "FlashCard"

caption = "Love English"
pygame.display.set_caption(caption)
pygame.display.set_icon(pygame.image.load("Asset\\Icon\\Icon.ico"))

Font_path = "Asset/Font/Font.ttf"
def font(text, size, color = "white", pos = (0,0), rect = (), ReturnRect = False, ReturnFontWidth = False, ReturnFontHeight = False):
    font_text = pygame.font.Font(Font_path, size)
    font_text = font_text.render(text, False, color)
    

    font_width = font_text.get_width()
    font_height = font_text.get_height()

    if ReturnFontWidth: 
        return font_width
    elif ReturnFontHeight: return font_height
    
    font_x = pos[0]
    font_y = pos[1]

    if len(rect) == 4:
        font_x += rect[0] + rect[2] // 2 - font_width // 2
        font_y += rect[1] + rect[3] // 2 - font_height // 2
    
    if font_x == None:
        font_x = screen_width // 2 - font_width // 2
    
    if font_y == None:
        font_y = screen_height // 2 - font_height // 2

    screen.blit(font_text, (font_x, font_y))

    if ReturnRect:
        return pygame.Rect(font_x, font_y, font_width, font_height)

def SetColor(surface, color):
    w, h = surface.get_size()
    r, g, b, _ = color
    for x in range(w):
        for y in range(h):
            a = surface.get_at((x, y))[3]
            surface.set_at((x, y), pygame.Color(r, g, b, a))

def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)

FileData = None

# Lấy File FlashCard Của Bạn
PathFileFlashCard = os.path.join("StoreData","FlashCard")

pd = importlib.import_module("pandas")
def SaveFileFlashCard(TextList : list, StoreFlashCard : dict):
    for NameFile in StoreFlashCard:
        if NameFile in TextList:
            df = pd.DataFrame(StoreFlashCard[NameFile].values(), columns=['English', 'Vietnamese'])
            df.to_excel(os.path.join(PathFileFlashCard, f"{NameFile}.xlsx"), 
                        index=False)
        
        else:
            try: os.remove(os.path.join(PathFileFlashCard, f"{NameFile}.xlsx"))
            except: pass
    
    TextString = "\n".join(TextList)
    open("StoreData\\FlashCard\\FlashCardName.txt", mode = "w").write(TextString)

def LoadFileFlashCard():
    ResultFileText = [] 
    for NameFile in os.listdir(PathFileFlashCard):
        if ".txt" in NameFile:
            try:
                file = open(os.path.join(PathFileFlashCard,"FlashCardName.txt"), mode = "r")
                text = file.read().split("\n")
                if text[0] == '': continue
                ResultFileText = text
            
            except:
                continue

        else:
            Data = {}
            df = pd.read_excel(os.path.join(PathFileFlashCard, NameFile))
            for QuantityData in range(len(df)):
                Data[QuantityData] = [df["English"][0], df["Vietnamese"][0]]
            Var_Obj.Store_FlashCard[NameFile.replace(".xlsx","")] = Data
    
    return ResultFileText

FileData = LoadFileFlashCard()

# Lấy File FlashCard Học Theo Chủ Đề
PathFileFlashCard = os.path.join("StoreData", "FlashCardTheme")
def GetFileFlashCardTheme():
    for FileName in os.listdir(PathFileFlashCard):
        DataStore = {}
        df = pd.read_excel(os.path.join(PathFileFlashCard, FileName), header=None)
        Name = FileName[1:].replace(".xlsx","")
        """
            df[0] : Từ vựng
            df[1] : nghĩa
        """
        DataStore = {Quantity: [df.at[Quantity, 0], df.at[Quantity, 1]] for Quantity in range(len(df))}
        Var_Obj.FlashCardTheme[Name] = DataStore  
        Var_Obj.FlashCardThemeNameList.append(Name)

GetFileFlashCardTheme()

def KMP(s1, s2):
    i = 1
    preLPS = 0
    lps = [0] * len(s1)
    while i < len(s1):
        if s1[i] == s1[preLPS]:
            lps[i] += preLPS + 1
            i += 1
        
        elif preLPS == 0:
            lps[i] = 0
            i += 1
        
        else:
            preLPS = lps[preLPS - 1]
    
    i = 0
    j = 0
    while i < len(s2):
        if s2[i] == s1[j]:
            i += 1
            j += 1
        
        elif j == 0:
            i += 1
        
        else:
            j = lps[j - 1]
        
        if j == len(s1):
            return True
    
    return False