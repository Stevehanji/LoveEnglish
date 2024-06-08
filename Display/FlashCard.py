from Tool.Variable import *
from Tool.Create_Button import *
from Tool.TextInput import *

# Create Button
OKButton = Button(screen_width - 400, screen_height - 200, 200, 100, button_color)
CompleteButton = Button(screen_width - 500, 50, 300, 100, "lime")

# ylr = screen_height // 2 - 75 // 2

dx_arrow_left = 0
ylr = screen_height - 175
LeftButton = Button(75, ylr, 75, 75, "white")
RightButton = Button(screen_width - 150, ylr, 75, 75, "white")


LeftButtonLearnFlashCard = Button(100, screen_height - 125, 75, 75, "white")
RightButtonLearnFlashCard = Button(screen_width - 200, screen_height - 125, 75, 75, "white")
AddButton = Button(screen_width - 120, screen_height // 2 - 100 // 2, 100, 100, "white")

ScreenButton = Button1()

# Create Text Input Box

# Name Text Input Box
Input_Box_Enter_Name_FlashCard = TextInputBox(100, 300, 1000, 100)
Input_Box_Enter_Name_FlashCard.SetFont(50, Font_path)

# Vocabulary Text Input Box
InputVocabularyText = TextInputBox(100, 300, 1000, 100)
InputVocabularyText.SetFont(50, Font_path)

# Mean Text Input Box
InputMeanText = TextInputBox(100, 500, 1000, 100)
InputMeanText.SetFont(50, Font_path)


"""
    -- FlashCard Menu --

        - Học FlashCard Theo Chủ Đề
        
        - FlashCard Của Bạn
            + Tạo FlashCard
            + Học FlashCard

"""

class FlashCard(Var_Obj):
    def __init__(self):
        self.timeanimation = pygame.time.get_ticks()
        self.second = 0.5
        self.do = False
        self.clockdo = True
        self.ShowTextIfNotEntered = False
        self.ShowTextIfDuplicate = False
        self.SaveText = ""

        self.InputTextlist = []
        self.screen_rect = screen.get_rect()

        # Store Vocabularys and means
        self.TemporaryStorage = {}
        self.SaveVocabulary = {}

        self.AmountOfVocabulary = 0
        self.CurrentPage = 0
        self.name = ""

        self.StartToLearnFlashCard = False
        self.RotateFlashCard = False

        self.Data = FileData

        self.YourFlashCard = None

        self.IDName = None
        self.NameThemeFlashCard = None

        self.count = 0

    # -- Flash Card Menu --
    def FlashCardMenu(self):
        font("FlashCard", 75, "White",(None, 10))
        screen.blit(pygame.transform.scale(img_list["FlashCardImg"], (500,500)), (750,125))

        if Nut_hoc_FlashCard_Theo_Chu_de.draw_Button_with_text("Học theo chủ đề bằng FlashCard",
                                                               30, "white",(button_color_1),[None,None,50]):
            self.DisplayTieuChuanIsShow = False
            return "LearnByThemeWithFlashCard"
        
        if Nut_Flash_Card_Cua_Ban.draw_Button_with_text("Flash Card Của Bạn",40, "white",(button_color_1),[None,None,50]):
            self.DisplayTieuChuanIsShow = False
            return "YourFlashCard"
        
        return "MenuFlashCard"

    # - Học FlashCard Theo Chủ Đề
    def LearnByThemeWithFlashCard(self):
        is_back = ButtonBack.draw_Button_with_image(img_list["back_icon"], button_color_1, 5, border=["black",5,5])

        pygame.draw.rect(screen, "#f2726a",(200,200,screen_width - 400, 500), border_radius=20)
        NutHoc = pygame.draw.rect(screen, "white", ((screen_width - 400 + 200) // 2 + 100 // 2 - 50, 600, 200,50), border_radius=20)

        font(Var_Obj.FlashCardThemeNameList[self.CurrentPage], 75, "white",(0,-100),
             (200,200,screen_width - 400, 500))
        font("Học",35,"black",(0,0), rect=((screen_width - 400 + 200) // 2 + 100 // 2 - 50, 600, 200,50))
        
        if self.CurrentPage < len(Var_Obj.FlashCardThemeNameList) - 1:
            IsRight = RightButton.draw_Button_with_image(img_list["Arrow"], button_color_1, 5, border=["black",5,5])
            if IsRight:
                self.CurrentPage += 1
                
        if self.CurrentPage != 0:
            IsLeft = LeftButton.draw_Button_with_image(pygame.transform.flip(img_list["Arrow"], True, False), button_color_1, 5, border=["black",5,5], dx = dx_arrow_left)

            if IsLeft:
                self.CurrentPage -= 1
        
        if B.Is_Clicked(NutHoc):
            self.IDName = Var_Obj.FlashCardThemeNameList[self.CurrentPage]
            self.NameThemeFlashCard = Var_Obj.FlashCardThemeNameList[self.CurrentPage]
            self.YourFlashCard = False
            return "LearnFlashCard", False

        if is_back:
            self.do = False
            self.clockdo = True
            self.CurrentPage = 0
            return "MenuFlashCard", True

        font("Học Qua FlashCard", 75, "White",(None, 10))
        

        return "LearnByThemeWithFlashCard", False

    # FlashCard Của Bạn
    def FlashCardCuaBan(self):
        is_back = ButtonBack.draw_Button_with_image(img_list["back_icon"], button_color_1, 5, border=["black",5,5])
        font("FlashCard Của Bạn", 75, "White",(None, 10))
        if Nut_tao_flash_card.draw_Button_with_text("Tạo Flash Card", 40, "white",(button_color_1),[None,None,50]) and self.count >= 10:
            self.count = 0
            return "CreateFlashCard", False

        else:
            self.count += 1

        if Nut_Hoc_Flash_Card_Cua_Ban.draw_Button_with_text("Học Flash Card Của Bạn",40, "white",(button_color_1),[None,None,50]) and self.count >= 10:
            self.count = 0
            return "LearnYourFlashCard", False

        else:
            self.count += 1

        if is_back:
            self.do = False
            self.clockdo = True
            self.count = 0
            return "MenuFlashCard", True
    
        return "YourFlashCard", False

    def animation(self):
        current_time = pygame.time.get_ticks()

        if self.do == False and self.clockdo:
            self.timeanimation = current_time
            self.clockdo = False

        if current_time - self.timeanimation >= self.second * 1000:
            self.do = True
    
    # +++ Các công cụ FlashCard Của Bạn +++
    def ResetAllTextBox(self, listInputBoxs : list):
        for InputBox in listInputBoxs:
            InputBox.Is_Input = False
            InputBox.showCurso(False)

    def ResetAllTextBoxIfClickScreen(self, listInputBoxs : list):
        if ScreenButton.Is_Clicked(self.screen_rect):
            self.ResetAllTextBox(listInputBoxs)    

    def ResetPage(self):
        self.CurrentPage = 0
        self.AmountOfVocabulary = 0

    # + Tạo FlashCard
    def FlashCardCreate(self, event):
        # self.animation()

        # if self.do:
            # Tạo Nút Thoát
            is_back = ButtonBack.draw_Button_with_image(img_list["back_icon"], button_color_1, 5, border=["black",5,5])

            self.ResetAllTextBoxIfClickScreen([Input_Box_Enter_Name_FlashCard])

            # Tên FlashCard Của Bạn
            font("Tên FlashCard Của Bạn", 50, "white",(100,200))
            Input_Box_Enter_Name_FlashCard.draw(event)
            Name_Flash_Card = Input_Box_Enter_Name_FlashCard.get_value()
            
            # OK Button
            if OKButton.draw_Button_with_text("OK",35, "white",(button_color_1),[None,None,50]):
                # if Name_Flash_Card not in GetTables():


                if Name_Flash_Card not in Var_Obj.Store_FlashCard:
                
                    # Check If you enter Text
                    if len(Name_Flash_Card) >= 1:
                        self.ShowTextIfNotEntered = False
                        self.name = Name_Flash_Card
                        self.ShowTextIfDuplicate = False
                        return "FlashCardCreateScreen", False
                    
                    else:
                        self.ShowTextIfNotEntered = True
                
                else:
                    self.SaveText = Name_Flash_Card
                    self.ShowTextIfDuplicate = True
            
            # If You Clicked OK Button, but you don't enter text
            if self.ShowTextIfNotEntered:
                font("*Bạn cần nhập tên FlashCard", 25, "red",(100,425))
            
            if self.ShowTextIfDuplicate:
                font(f"{self.SaveText} bị trùng", 25, "red",(100,425))

            if is_back:
                self.do = False
                self.clockdo = True
                Input_Box_Enter_Name_FlashCard.Reset_Button_Box(event)
                self.ShowTextIfNotEntered = False
                self.ShowTextIfDuplicate = False
                return "YourFlashCard", True

            # Tạo tiêu đề
            font("Tạo FlashCard", 75, "White",(None, 10))

            return "CreateFlashCard", False
    
    def FlashCardCreateScreen(self, event):
        is_back = ButtonBack.draw_Button_with_image(img_list["back_icon"], button_color_1, 5, border=["black",5,5])

        self.ResetAllTextBoxIfClickScreen([InputVocabularyText, InputMeanText])

        font("Từ Vựng", 50, "white",(100,200))
        InputVocabularyText.draw(event)
        VocabularyText = InputVocabularyText.get_value()

        font("Nghĩa", 50, "white",(100,400))
        InputMeanText.draw(event)
        MeanText = InputMeanText.get_value()

        if InputVocabularyText.Is_Input and 1 not in self.InputTextlist:
            self.InputTextlist.append(1)
        
        if InputMeanText.Is_Input and 2 not in self.InputTextlist:
            self.InputTextlist.append(2)
        
        DictionaryOfInputText = {
            1 : InputVocabularyText,
            2 : InputMeanText
        }
        
        if len(self.InputTextlist) > 1:
            InputTextFirstIndexOfInputTextlist = self.InputTextlist[0]
            del self.InputTextlist[0]
            DictionaryOfInputText[InputTextFirstIndexOfInputTextlist].Is_Input = False
            DictionaryOfInputText[InputTextFirstIndexOfInputTextlist].showCurso(False)
        
        IsComplete = CompleteButton.draw_Button_with_text("Hoàn Thành",35, "white",(button_color_1),[None,None,-1])

        if self.CurrentPage > 0:
            IsLeft = LeftButton.draw_Button_with_image(pygame.transform.flip(img_list["Arrow"], True, False), button_color_1, 5, border=["black",5,5], dx = dx_arrow_left)

            if IsLeft:
                self.CurrentPage -= 1
                self.ResetBox(event)
                

        if self.CurrentPage < self.AmountOfVocabulary and self.AmountOfVocabulary > 0:
            IsRight = RightButton.draw_Button_with_image(img_list["Arrow"], button_color_1, 5, border=["black",5,5])

            if IsRight:
                self.CurrentPage += 1
                self.ResetBox(event)

        IsAdd = AddButton.draw_Button_with_text("Thêm", 30, "black",(button_color_1),["black",10,-1])

        if IsAdd and self.CheckVocabularyMeans(VocabularyText, MeanText):
            self.CurrentPage += 1
            self.AmountOfVocabulary += 1
            self.TemporaryStorage[self.CurrentPage] = {"":""}
            InputVocabularyText.adjust_value("", event)
            InputMeanText.adjust_value("", event)
            InputVocabularyText.showCurso(False)
            InputMeanText.showCurso(False)
        
        self.TemporaryStorage[self.CurrentPage] = [VocabularyText, MeanText]

        font(f"{self.CurrentPage+1} : {self.AmountOfVocabulary+1}", 75, "white",(None, screen_height - 200))
        
        # If you clicked Complete button
        if IsComplete:
            if self.CurrentPage > 0:
                Var_Obj.Store_FlashCard[self.name] = self.TemporaryStorage
                self.ResetPage()
                InputVocabularyText.adjust_value("", event)
                InputMeanText.adjust_value("", event)
                InputVocabularyText.showCurso(False)
                InputMeanText.showCurso(False)
                self.Data.insert(0, self.name)
                self.TemporaryStorage = {}
                self.name = ""
                Input_Box_Enter_Name_FlashCard.adjust_value("",event)
                Input_Box_Enter_Name_FlashCard.showCurso(False)
                return "CreateFlashCard", True
            else:
                print("Không có FlashCard")

        if is_back:
            self.do = False
            self.clockdo = True
            return "CreateFlashCard", True

        return "FlashCardCreateScreen", False

    # +++ Các công cụ Tạo FlashCard
    def CheckVocabularyMeans(self, vocabulary, means):
        if len(vocabulary) != 0 and len(means) != 0:
            return True
        
        return False

    def ResetBox(self, event):
        VocabularyText = self.TemporaryStorage[self.CurrentPage][0]
        MeanText = self.TemporaryStorage[self.CurrentPage][1]
        InputVocabularyText.adjust_value(VocabularyText, event)
        InputMeanText.adjust_value(MeanText, event)
        InputVocabularyText.Is_Input = False
        InputMeanText.Is_Input = False
        InputVocabularyText.showCurso(False)
        InputMeanText.showCurso(False)

    # Phần FlashCard Của Bạn
    def LearnYourFlashCard(self):
        # self.animation()

        # if self.do:
            # Tạo Nút Thoát
            is_back = ButtonBack.draw_Button_with_image(img_list["back_icon"], button_color_1, 5, border=["black",5,5])
            # tables_list = GetTables()

            if len(self.Data) != 0:
                
                if len(self.Data) > 3:
                    quantity = 3
                
                else:
                    quantity = len(self.Data)

                for index in range(quantity):
                    # Vẽ cái box FlashCard và học FlashCard
                    if BoxFlashCard.DrawBoxFlashCard(index + 1, self.Data[index + self.CurrentPage]):
                        self.IDName = self.Data[index + self.CurrentPage]
                        self.YourFlashCard = True
                        return "LearnFlashCard", False

                if len(self.Data) > 3 and self.CurrentPage < len(self.Data) - 3:
                    IsRight = RightButton.draw_Button_with_image(img_list["Arrow"], button_color_1, 5, border=["black",5,5])

                    if IsRight:
                        self.CurrentPage += 1
                
                if self.CurrentPage != 0:
                    IsLeft = LeftButton.draw_Button_with_image(pygame.transform.flip(img_list["Arrow"], True, False), button_color_1, 5, border=["black",5,5], dx = dx_arrow_left)

                    if IsLeft:
                        self.CurrentPage -= 1
            
            else:
                font("Không có FlashCard", 75, "White",(None, None))

            # Tạo tiêu đề
            font("FlashCard Của Bạn", 75, "White",(None, 10))
            
            if is_back:
                self.do = False
                self.clockdo = True
                self.CurrentPage = 0
                return "YourFlashCard", True

            return "LearnYourFlashCard", False

    # Công Cụ Học FlashCard
    def LearnFlashCard(self):
        
        # Tạo tiêu đề
        pygame.draw.rect(screen, "white",(150,200,1000,500))
        font(self.IDName, 75, "white",(None, 25))

        # Thùng Rác (được xóa khi đây là flashCard của người dùng)
        if self.YourFlashCard:
            if TrashBinButton.draw_Button_with_image(img_list["TrashBin"], button_color_1, 5, ["black",10,5]):
                self.Data.remove(self.IDName)
                return "LearnYourFlashCard", False

        # nếu chưa học
        if self.StartToLearnFlashCard == False:
            ButtonStartLearn = pygame.draw.rect(screen, "red",(525 + 30, 400,200,100), border_radius=20)
            font("Bắt Đầu", 25, "white",(0,0), (525 + 30, 400,200,100))

            # Nếu Bấm nút học
            if B.Is_Clicked(ButtonStartLearn):
                self.StartToLearnFlashCard = True

                """
                    Nếu như FlashCard Của người dùng: 
                        self.SaveVocabulary = Var_Obj.Store_FlashCard
                    
                    Ngược lại học theo chủ đề thì
                        self.SaveVocabulary = ?
                
                """

                if self.YourFlashCard:
                    self.SaveVocabulary = Var_Obj.Store_FlashCard[self.IDName]
                
                else:
                    # print(Var_Obj.FlashCardTheme)
                    self.SaveVocabulary = Var_Obj.FlashCardTheme[self.NameThemeFlashCard]
        
        # Nếu đã học
        if self.StartToLearnFlashCard:
            RotateButton = pygame.draw.rect(screen, "white",(525 + 30, screen_height - 150,200,100), border_radius=20)
            font("Xoay", 25, "black",(0,0), (525 + 30, screen_height - 150,200,100))

            # Chỉnh trang FlashCard
            if self.CurrentPage > 0:
                IsLeft = LeftButtonLearnFlashCard.draw_Button_with_image(pygame.transform.flip(img_list["Arrow"], True, False), button_color_1, 5, border=["black",5,5], dx = dx_arrow_left)

                if IsLeft:
                    self.CurrentPage -= 1
                    self.RotateFlashCard = False

            if self.CurrentPage <= len(self.SaveVocabulary) - 2:
                IsRight = RightButtonLearnFlashCard.draw_Button_with_image(img_list["Arrow"], button_color_1, 5, border=["black",5,5])

                if IsRight:
                    self.CurrentPage += 1
                    self.RotateFlashCard = False

            # Nếu Click Xoay
            if B.Is_Clicked(RotateButton):
                self.RotateFlashCard = not self.RotateFlashCard
            
            # Check Điều kiện của xoay
            if self.RotateFlashCard == False:
                TEXT = self.SaveVocabulary[self.CurrentPage][0]
                Language = "Tiếng Anh"

            if self.RotateFlashCard:
                TEXT = self.SaveVocabulary[self.CurrentPage][1]
                Language = "Tiếng Việt"
            
            # Tạo Font (tiếng anh, tiếng việt)
            font(Language, 35, "black",(925,200))
            font(TEXT, 75, "black",(0,0),(150,200,1000,500))

            # Tạo Font (trang)
            font(f"{self.CurrentPage + 1} : {len(self.SaveVocabulary)}", 50, "white",(screen_width - 200, 50))

        is_back = ButtonBack.draw_Button_with_image(img_list["back_icon"], button_color_1, 5, border=["black",5,5])

        # Nếu Quay Lại
        if is_back:
            self.do = False
            self.clockdo = True
            self.StartToLearnFlashCard = False
            self.SaveVocabulary = {}
            self.ResetPage()
            self.RotateFlashCard = False
            self.YourFlashCard = None

            if self.YourFlashCard:
                return "LearnYourFlashCard", False
            
            else:
                return "LearnByThemeWithFlashCard", False
        
        return "LearnFlashCard", False