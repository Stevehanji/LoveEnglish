from Tool.Variable import *
from Tool.Create_Button import *
from Tool.img import *
from Tool.Color import *
from Display.FlashCard import *
from Display.LearnSubject import *
from Tool.image_game import *
import importlib
# from math import sin

DisplayTieuChuanIsShow = True
DisplayLearn = "LearnMenu"

subject = Subject()
subject.ProcessdataTest()
sinx = 0
width_title = image_game["Menu-Title"].get_width()
height_title = image_game["Menu-Title"].get_height()

xC1 = 40
yC1 = 296
xC2 = 947
yC2 = 296

# Button
ButtonNewGameX = 434
# ButtonNewGameY = 225
ButtonNewGameY = screen_height // 2 - image_game["Menu-Button"].get_height() // 2

ButtonNewGame = image_game["Menu-Button"]
ButtonNewGamerect = ButtonNewGame.get_rect(topleft = (ButtonNewGameX, ButtonNewGameY))
WidthMainButtonNewGame = image_game["Menu-Button"].get_width()
HeightMainButtonNewGame = image_game["Menu-Button"].get_height()

# ButtonLoadGame = image_game["Menu-Button"]
# ButtonLoadGameRect = ButtonLoadGame.get_rect(topleft = (434,439))
mouseImg = pygame.transform.scale(image_game["Pointer-HoverMouse"], (50,50))

def Hoc(display, move):
    global DisplayLearn, DisplayTieuChuanIsShow

    if DisplayLearn == "LearnMenu":
        font("Học", 75, "White",(None, 10))
        DisplayLearn, DisplayTieuChuanIsShow = subject.draw(move)
        subject.DrawPigAndUpdatePig()

        # subject.complete()
    
    elif DisplayLearn == "QuestionTest":
        # DisplayLearn, DisplayTieuChuanIsShow = subject.QuestionDisplay()
        DisplayLearn, DisplayTieuChuanIsShow = subject.NewQuestionDisplay()

    return display, DisplayTieuChuanIsShow


from Game.PlayGame import *
LeftArrowButton = Button(75, screen_height - 300 - 75, 75, 75, "white")
RightArrowButton = Button(screen_width - 150, 
                          screen_height - 300 - 75, 
                          75, 
                          75, "white")

DisplaySetting = ["Hoc","Choi"]
PageSetting = 0

IsShowP1 = True
IsShowP2 = False

def Setting(display):
    global PageSetting, IsShowP1, IsShowP2

    def drawButtonAdmin(x,y,w,h):
        ButtonOpenPermission = pygame.draw.rect(screen, "black",(x,y,w,h))
        if B.Is_Clicked(ButtonOpenPermission):
            return True

    def ButtonTick(IsClick, x, y, w = None, h = None, text = None,padding = 5, dxText = 0):
        if text == None: raise TypeError("Text Not None")
        ButtonTick = pygame.Rect(x,y,w,h)
        pygame.draw.rect(screen, "black",(x, y, w, h))
        button = pygame.draw.rect(screen, "gray",(ButtonTick.x + padding,
                                         ButtonTick.y + padding,
                                         ButtonTick.w - padding * 2,
                                         ButtonTick.h - padding * 2))
    
        font(text, 35, "white",(175 + dxText,0),[ButtonTick.x,
                                                    ButtonTick.y,
                                                    ButtonTick.w,
                                                    ButtonTick.h])

        if IsClick:
            screen.blit(pygame.transform.scale(image_game["Other-Tick"],
                                            (w + w // 2 - padding * 3,w + w // 2 - padding * 3)),
                                            (ButtonTick.x - 10,
                                             ButtonTick.y - 10))
        
        return button
    

    if not Var_Obj.IsFinishButtonAdmin:
        if IsShowP1: 
            if drawButtonAdmin(0,0,2,2): IsShowP1 = False; IsShowP2 = True

        if IsShowP2: 
            if drawButtonAdmin(screen_width - 4,screen_height - 4,2,2): 
                IsShowP2 = False
                Var_Obj.IsFinishButtonAdmin = True
            # Var_Obj.IsAdmin = True

    font("Setting", 75, "White",(None, 10))
    if DisplaySetting[PageSetting] == "Hoc":

        font("Phần Học",75, "white",(None, screen_height - 350))
        JumpScaredButton = ButtonTick(subject.JumpScared, 200,200,100,100,"JumpScared")

        if B.Is_Clicked(JumpScaredButton):
            subject.JumpScared = not subject.JumpScared
            DataStore.SettingData["Hoc"]["JumpScared"] = subject.JumpScared
        
        if subject.JumpScared:
            # Xác xuất (Probablity)
            font("Xác suất", 50, "white",(None, 300))
            margin = 400

            HighButtonIsClick = False
            MediumButtonIsClick = False
            SmallButtonIsClick = False

            if subject.JumpScaredProbability in range(2,5):
                HighButtonIsClick = True
            
            elif subject.JumpScaredProbability in range(5,10):
                MediumButtonIsClick = True
            
            elif subject.JumpScaredProbability == 10:
                SmallButtonIsClick = True

            HighButton = ButtonTick(HighButtonIsClick, 100 + margin * 2,400,75,75,"High")
            MediumButton = ButtonTick(MediumButtonIsClick, 100 + margin * 1,400,75,75,"Medium")
            SmallButton = ButtonTick(SmallButtonIsClick, 100, 400,75,75,"Small")

            if B.Is_Clicked(HighButton):
                subject.JumpScaredProbability = 2
                DataStore.SettingData["Hoc"]["ProbalityOfJumpScared"] = 2
            
            elif B.Is_Clicked(MediumButton):
                subject.JumpScaredProbability = 5
                DataStore.SettingData["Hoc"]["ProbalityOfJumpScared"] = 5
            
            elif B.Is_Clicked(SmallButton):
                subject.JumpScaredProbability = 10
                DataStore.SettingData["Hoc"]["ProbalityOfJumpScared"] = 10

    elif DisplaySetting[PageSetting] == "Choi":
        font("Phần Chơi",75, "white",(None, screen_height - 350))

        EnglishAndVietnameseButton = ButtonTick(game.IsTranslate,200,200,100,100,"Translate To VietNam", dxText=100)
        
        if B.Is_Clicked(EnglishAndVietnameseButton):
            game.IsTranslate = not game.IsTranslate
            DataStore.SettingData["PlayGame"]["TranslateToVietName"] = game.IsTranslate


    # Page
    if PageSetting != 0:
        IsClick = LeftArrowButton.draw_Button_with_image(pygame.transform.flip(img_list["Arrow"], True, False), button_color_1, 5, border=["black",5,5])

        if IsClick: PageSetting -= 1
    
    if PageSetting < len(DisplaySetting) - 1:
        IsClick = RightArrowButton.draw_Button_with_image(img_list["Arrow"], button_color_1, 5, border=["black",5,5])

        if IsClick: PageSetting += 1

    return display

def GameDisplay(display, Permission):
    global sinx, width_title, height_title, yC1, yC2, ButtonNewGame

    size_bg = (1300, 700)
    bg1 = pygame.transform.scale(image_game["Background-background1"], size_bg)
    bg2 = pygame.transform.scale(image_game["Background-background2"],size_bg)
    screen.blit(bg1, (0,0))
    screen.blit(bg2, (0,0))

    TitleImage = pygame.transform.scale(image_game["Menu-Title"], (width_title, height_title))

    screen.blit(TitleImage,(screen_width // 2 - TitleImage.get_width() // 2,
                                          26))
    screen.blit(image_game["Menu-C1"], (40,yC1))
    screen.blit(image_game["Menu-C2"], (947,yC2))
    
    
    screen.blit(ButtonNewGame, ButtonNewGamerect)
    # screen.blit(ButtonLoadGame, ButtonLoadGameRect)

    # screen.blit(image_game["Menu-NewGame"],(495,246))
    screen.blit(image_game["Menu-NewGame"],(495,410))
    # screen.blit(image_game["Menu-LoadGame"],(478,462))

    if Permission == "Admin":
        if CreateButton.draw_Button_with_image(img_list["CreateButtonIcon"], None,10, ["black", 5, 0]):
            return "CreateWorld", False
        # screen.blit(pygame.transform.scale(img_list["CreateButton"], (200,200)), (screen_width - 100, 50))

    if B.Is_Hover(ButtonNewGamerect):
        pygame.mouse.set_visible(False)
        pos = pygame.mouse.get_pos()
        mouserect = mouseImg.get_rect(center = pos)
        screen.blit(mouseImg, mouserect)

        if B.Is_Clicked(ButtonNewGamerect):
            pygame.mouse.set_visible(True)
            return "PlayGame", False
        
        # elif B.Is_Clicked(ButtonLoadGameRect):
        #     pygame.mouse.set_visible(True)
        #     return "PlayGame", False
    
    else:
        pygame.mouse.set_visible(True)

    if importlib.import_module("math").sin(sinx) > 0:
        width_title += 1
        height_title += 1
        yC1 += 1
        yC2 += 1
    
    else:
        width_title -= 1
        height_title -= 1
        yC1 -= 1
        yC2 -= 1

    sinx += 0.25
    

    return display, True

# Flash card
flashcard = FlashCard()
displayflashcard = "MenuFlashCard"

def DisplayFlashCard(display, event):
    global displayflashcard, DisplayTieuChuanIsShow

    if displayflashcard == "MenuFlashCard":
        displayflashcard = flashcard.FlashCardMenu()
    
    elif displayflashcard == "LearnByThemeWithFlashCard":
        displayflashcard, DisplayTieuChuanIsShow = flashcard.LearnByThemeWithFlashCard()

    elif displayflashcard == "YourFlashCard":
        displayflashcard, DisplayTieuChuanIsShow = flashcard.FlashCardCuaBan()
    
    elif displayflashcard == "CreateFlashCard":
        displayflashcard, DisplayTieuChuanIsShow = flashcard.FlashCardCreate(event)
    
    elif displayflashcard == "LearnYourFlashCard":
        displayflashcard, DisplayTieuChuanIsShow = flashcard.LearnYourFlashCard()
    
    elif displayflashcard == "FlashCardCreateScreen":
        displayflashcard, DisplayTieuChuanIsShow = flashcard.FlashCardCreateScreen(event)
    
    elif displayflashcard == "LearnFlashCard":
        displayflashcard, DisplayTieuChuanIsShow = flashcard.LearnFlashCard()
    
    return display, DisplayTieuChuanIsShow

def change_color_display(style):
    SetColor(img_list["Setting"], 
             pygame.Color(display_color[style]["Color_Icon"]))
    SetColor(img_list["Camera"], 
             pygame.Color(display_color[style]["Color_Icon"]))

def display_tieu_chuan(style, display):
    pygame.draw.line(screen,line_background_color,(0,screen_height - 200), 
                     (screen_width,screen_height - 200), 3)
    
    texts = ["Học","Chơi","Flash Card"]
    if Nut_Hoc.draw_Button_with_text(texts[0],35, "white",(button_color_1),[None,None,50]) and subject.showbox == False:
        display = "Hoc"
    
    if Nut_Flash_Card.draw_Button_with_text(texts[2],35, "white",(button_color_1),[None,None,50]) and subject.showbox == False:
        display = "FlashCard"

    if Nut_Choi.draw_Button_with_text(texts[1],35, "white",(button_color_1),[None,None,50]) and subject.showbox == False:
        display = "Game"

    Camera_Button = screen.blit(img_list["Camera"], (screen_width - 300, 
                                      (screen_height + screen_height - 200) // 2 - 
                                      img_list["Camera"].get_height() // 2))
    
    Setting_Button = screen.blit(img_list["Setting"], (screen_width - 150, 
                                      (screen_height + screen_height - 200) // 2 - 
                                      img_list["Setting"].get_height() // 2))
    
    if B.Is_Hover(Setting_Button):
        SetColor(img_list["Setting"], pygame.Color(button_color))

        if B.Is_Clicked(Setting_Button):
            display =  "Setting"
    
    elif B.Is_Hover(Camera_Button):
        SetColor(img_list["Camera"], pygame.Color(button_color))

        if B.Is_Clicked(Camera_Button):
            display = "Camera"
    
    else:
        change_color_display(style)
    
    return display, DisplayTieuChuanIsShow

def CameraDisplay(display):
    font("Nhận diện từ vựng", 75, "white",(None, 10))
    # font("qua hình ảnh", 75, "white",(None, 95))

    screen.blit(img_list["MenuCamera.png"],(100,200))

    # NhanDienQuaHinhAnhButton.draw_Button_with_text("Nhận diện qua hình ảnh",35, "white",(button_color_1),[None,None,200])
    if NhanDienQuaCameraButton.draw_Button_with_text("Nhận diện qua Camera",35, "white",(button_color_1),[None,None,200]):
        Var_Obj.IsJumpApp = True

    return display