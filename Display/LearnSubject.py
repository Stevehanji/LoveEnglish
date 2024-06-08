from Tool.Variable import *
from Tool.Button import *
import random
# from QuestionAndAnswer.QuestionAndAnswer import *
from Tool.Create_Button import *
from Tool.Speak import *
from QuestionAndAnswer.QuestionAndAnswer import *
from Game.Other import *
from StoreData.Setting import *

class Subject:
    def __init__(self):
        self.tile_map = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        self.Object = []
        self.tile_size = 200
        self.screen_scroll = 0

        self.level = DataStore.StudyData["Level"]
        # self.level = 0

        self.speed = 10
        self.pigx = 0
        self.pigy = 0
        self.count = 0
        self.showbox = False
        self.YesToLearn = False
        self.ShowBoxCorrectOrIncorrect = False
        self.IsTrueOfMultipleChoiceQuestion = False
        self.time = 0
        self.AmountOfQuestion = 0
        self.cycle = 2

        self.Question = 0

        self.QuestionLevel = []
        self.AnswerListIncorrect = []
        self.AmountOfIncorrectQuestion = 0
        self.AmountOfCorrectQuestion = 0

        self.ShowIconRedo = False
        self.over = False

        self.speak = True
        self.Timespeak = 0
        self.SpeakStart = True

        self.TimeSound = 0
        self.Achivement = True
        self.TimeAchivementSound = 0
        self.AchivementX = screen_width

        self.FrameOfAchivement = pygame.time.get_ticks()
        self.timeAchivement = 1

        # self.speed = 10
        self.goBack = False

        self.AmountOfLevel = 8

        # self.ChildLevel = [0] * (self.AmountOfLevel)
        self.ChildLevel = DataStore.StudyData["ChildLevelList"]

        self.LevelCurrentToLearn = None
        self.CurrentChildOfCurrentLevelToLean = None

        self.Answer = None
        self.Letters = None
        self.text = []

        self.RectHover = None

        # self.LetterChoice = []
        self.LetterChoice = {}
        # self.IndexListOfLetterChoice = []

        self.LPos = None
        self.RPos = None

        self.WordsLeft = None
        self.WordsRight = None
        self.ChoiceWordLeft = ""
        self.ChoiceWordRight = ""
        self.ChoiceConnectWord = []

        self.ShowBoxForChild = False
        self.IsUpdateLevel = False
        # self.NewIndexSpeak = None


        # Setting
        self.JumpScared = DataStore.SettingData["Hoc"]["JumpScared"]

        self.JumpScaredScreen = False
        self.JumpScaredProbability = DataStore.SettingData["Hoc"]["ProbalityOfJumpScared"]

        self.Hard = False
        self.RESULT = None
        self.IsLevelTest = False
    
    def ProcessdataTest(self):
        diction_map = {
            1 : "Mire"
        }

        solevel = 0

        for x in range(len(self.tile_map[0])):
            for y in range(len(self.tile_map)):
                if solevel == self.AmountOfLevel: break

                if self.tile_map[y][x] > 0:
                    IMG = img_list[diction_map[self.tile_map[y][x]]]
                    IMG = pygame.transform.scale(IMG,(self.tile_size, self.tile_size))
                    img_rect = IMG.get_rect()
                    img_rect.x = x * 100
                    img_rect.y = y * 100 + 50
                    tile_data = (IMG, img_rect)
                    
                if self.tile_map[y][x] == 1:
                    self.Object.append(tile_data)
                    solevel += 1
    
    def DrawPigAndUpdatePig(self):
        IMG = pygame.transform.scale(img_list["PigHanji"], (120,100))
        PigPos = self.Object[self.level][1]
        screen.blit(IMG, (PigPos.x + 30,PigPos.y + 30))

        for CurrentLevelDrawCarrot in range(self.level+1, self.AmountOfLevel):
            IMG = pygame.transform.scale(img_list["Carrot"], (120,100))
            CarrotPostion = self.Object[CurrentLevelDrawCarrot][1]
            screen.blit(IMG, (CarrotPostion.x + 30, CarrotPostion.y + 30))

    def ModBox(self):
        pass

    def drawBox(self):
        draw_rect_alpha(screen, (0,0,0,50),(0,0,screen_width,screen_height))
        pygame.draw.rect(screen, "white", (200, 200,screen_width - 400, screen_height - 400), border_radius=50)
        font(f"Unit: {self.LevelCurrentToLearn + 1}", 75, "black",(0,-200),(200, 200,screen_width - 400, screen_height - 400))
        font(f"{levelDictionary[self.LevelCurrentToLearn]}", 45, "black",(0,-100),(200, 200,screen_width - 400, screen_height - 400))

        MaxChildLevel = {len(os.listdir(f"QuestionAndAnswer\\Level{self.LevelCurrentToLearn}"))}
        font(f"{self.ChildLevel[self.LevelCurrentToLearn] + 1} : {MaxChildLevel}",
             50, "black",(0,0),(200, 200,screen_width - 400, screen_height - 400))

        # Nút
        border_width = 5
        pygame.draw.rect(screen, "black", (screen_width - 500 - border_width, screen_height - 350 - border_width, 200 + border_width * 2, 75 + border_width * 2))
        YesButton = pygame.draw.rect(screen, "lime", (screen_width - 500, screen_height - 350, 200, 75))
        pygame.draw.rect(screen, "black", (300 - border_width, screen_height - 350 - border_width, 200 + border_width * 2, 75 + border_width * 2))
        NoButton = pygame.draw.rect(screen, "red", (300, screen_height - 350, 200, 75))
        font(f"Học", 35, "black",(0,0),(screen_width - 500, screen_height - 350, 200, 75))
        font(f"Thoát", 35, "black",(0,0),(300, screen_height - 350, 200, 75))

        if B.Is_Clicked(YesButton):
            self.YesToLearn = True
            self.showbox = False

        if B.Is_Clicked(NoButton):
            self.LevelCurrentToLearn = None
            self.showbox = False
        
    def draw(self, move):
        count = 0
        pointold = ()

        # Draw Line
        for level, tile in enumerate(self.Object):
            if count in range(1, 10):
                newpoint = tile[1]
                dx = 100
                dy = 100
                pygame.draw.line(screen, "white",(pointold.x + dx,pointold.y + dy),
                                 (newpoint.x + dx,newpoint.y + dy), 5)
            
            pointold = tile[1]

            # Level Button Click
            if self.showbox == False:
                if B.Is_Clicked(tile[1]) and self.level >= level:
                    self.LevelCurrentToLearn = level
                    self.showbox = True

            if count <= 10:
                count += 1

        # Draw Mule
        for tile in self.Object:
            screen.blit(tile[0], tile[1])
            
            if self.showbox == False:
                if self.Object[0][1].x <= 50:
                    if move[0] == True:
                        tile[1][0] += self.speed
                
                if self.Object[self.AmountOfLevel - 1][1].x >= 1000:
                    if move[1] == True:
                        tile[1][0] -= self.speed
        
        if self.YesToLearn:
            self.LoadQuestion()
            return "QuestionTest", False

        if Var_Obj.IsAdmin:
            pygame.draw.rect(screen, "black",(100 - 5,100 - 5,100 + 10,50 + 10))
            ButtonTestOfAdmin = pygame.draw.rect(screen, "white",(100,100,100,50))
            font("Test",25,"red",(-50,0),(100,100,200,50))
            
            if B.Is_Clicked(ButtonTestOfAdmin):
                self.LoadQuestion(True)
                self.YesToLearn = True
                self.LevelCurrentToLearn = 0
                self.IsLevelTest = True
                return "QuestionTest", False

        return "LearnMenu", True
    
    def DrawBoxCorrectOrInCorrectOfMultipleChoiceQuestion(self):
        pos_rect = (screen_width // 2 - (screen_width - 600) // 2, 
                    screen_height // 2 - (screen_height - 600) // 2,
                    screen_width - 600, 
                    screen_height - 600)
        # if isTrue
        draw_rect_alpha(screen, (0,0,0,50),(0,0,screen_width,screen_height))
        pygame.draw.rect(screen, "white", pos_rect, border_radius=50)

        # Check Đúng Sai
        if self.IsTrueOfMultipleChoiceQuestion:
            IMG = pygame.transform.scale(img_list["tick_icon"], (150,150))
            screen.blit(IMG, ((screen_width) // 2 - IMG.get_width() // 2,
                                                   310))

            color_button = "lime"
            
            font(f"Chính Xác!", 35, "lime",(0,50), pos_rect)

            if self.TimeSound == 0:
                pygame.mixer.Sound.play(ding)
                self.TimeSound += 1

        else:
            IMG = pygame.transform.scale(img_list["x_icon"], (150,150))
            screen.blit(IMG, ((screen_width) // 2 - IMG.get_width() // 2,
                                                   310))
            
            font(f"Đáp án đúng: '{self.Answer}'", 35, "red",(0,50), pos_rect)

            color_button = "red"

            if self.TimeSound == 0:
                pygame.mixer.Sound.play(wrong)
                self.TimeSound += 1

        TextButton = "Tiếp"
        # Nút tiếp theo
        NextButton = pygame.draw.rect(screen, color_button, (screen_width - 500,screen_height - 360, 150, 50), border_radius=50)
        font(TextButton, 35, "white",(0,0), (screen_width - 500,screen_height - 360, 150, 50))

        # Nếu click nút tiếp theo
        if B.Is_Clicked(NextButton):
            self.TimeSound = 0
            return True
    
    def LoadQuestion(self, IsAdmin = False) -> list:
        if not IsAdmin:
            self.CurrentChildOfCurrentLevelToLean = self.ChildLevel[self.LevelCurrentToLearn]
            self.QuestionLevel = GetQuestion(self.LevelCurrentToLearn, self.CurrentChildOfCurrentLevelToLean)
        
        else:
            self.QuestionLevel = GetQuestion("Test","Test", True)
        # self.Question = len(self.QuestionLevel) - 1

    def ResetQuestion(self):
        self.AnswerListIncorrect = []
        self.QuestionLevel = []
        self.over = False
        self.AmountOfQuestion = 0
        self.time = 0
        self.ShowBoxCorrectOrIncorrect = False
        self.ShowIconRedo = False

        self.Question = 0

        self.YesToLearn = False
        self.AmountOfIncorrectQuestion = 0
        self.AmountOfCorrectQuestion = 0
        self.TimeSound = 0
        self.SpeakStart = True

        self.count = 0
        self.Answer = None
        self.LetterChoice = {}

        self.WordsLeft = None
        self.WordsRight = None
        self.ChoiceWordLeft = ""
        self.ChoiceWordRight = ""
        self.ChoiceConnectWord = []
        self.Letters = None

    def UpdateLevelOrChildLevel(self):
        if self.ChildLevel[self.LevelCurrentToLearn] < len(os.listdir(f"QuestionAndAnswer\\Level{self.LevelCurrentToLearn}")):
            self.ChildLevel[self.LevelCurrentToLearn] += 1
            
            if self.ChildLevel[self.LevelCurrentToLearn] == len(os.listdir(f"QuestionAndAnswer\\Level{self.LevelCurrentToLearn}")):
                self.ChildLevel[self.LevelCurrentToLearn] -= 1

                if self.level == self.LevelCurrentToLearn and self.level != 8:
                    self.level = self.LevelCurrentToLearn + 1

            DataStore.StudyData["Level"] = self.level
            DataStore.StudyData["ChildLevelList"] = self.ChildLevel

    def PlayMusicComplete(self):
        if self.TimeSound == 0:
            LevelComplete.stop()
            LevelComplete.play()
            self.TimeSound += 1

    def DisplayOverQuestion(self):
        # Chạy nhạc
        self.PlayMusicComplete()
        
        font("CHÚC MỪNG BẠN ĐÃ", 75, "white",(None, 200))
        font("HOÀN THÀNH LEVEL", 65, "white",(None, 300))

        screen.blit(pygame.transform.scale(img_list["check.png"],(75,75)),(250,500))
        screen.blit(pygame.transform.scale(img_list["wrong.png"],(75,75)),(250,600))

        font(f"SỐ CÂU ĐÚNG: {self.AmountOfCorrectQuestion}", 50, "lime",(350,500))
        font(f"SỐ CÂU SAI: {self.AmountOfIncorrectQuestion}", 50, "red",(350,600))
        
        # self.UpdateLevelOrChildLevel()
    
    def ResetQuestionOfLevel(self):
        self.ShowBoxCorrectOrIncorrect = False
        self.time = 0
        self.IsTrueOfMultipleChoiceQuestion = None
        self.Question += 1

        if not self.RESULT and self.Hard:
            self.Question = 0

        self.count = 0
        self.Timespeak = 0
        self.speak = False
        self.SpeakStart = True
        self.Answer = None
        self.LetterChoice = {}
        self.RESULT = None

    def SetResult(self, r):
        self.RESULT = r

    def NewQuestionDisplay(self):
        is_back = ButtonBack.draw_Button_with_image(img_list["back_icon"], button_color_1, 5, border=["black",5,5])


        if is_back and not self.ShowBoxCorrectOrIncorrect and not self.JumpScaredScreen:
            self.ResetQuestion()
            LevelComplete.stop()
            self.IsLevelTest = False

            if self.IsUpdateLevel and not self.IsLevelTest:
                self.UpdateLevelOrChildLevel()
                self.IsUpdateLevel = False
        
        if self.YesToLearn == False:
            return "LearnMenu", True

        if self.over == False:
            self.AmountOfQuestion = len(self.QuestionLevel)

            if self.time != 0:
                # Check xem nó có vượt quá Question không
                if self.Question < self.AmountOfQuestion:
                    Q = self.QuestionLevel[self.Question]

                    if not self.JumpScaredScreen:
                        if self.Answer == None and Q[0] != 30:
                            # self.Answer = Q[2][0]
                            self.Answer = Q[3]

                        # Kiểm tra nếu câu hỏi là trắc nghiệm dạng đọc hoặc nghe  (số 0)
                        if Q[0] == 0 or Q[0] == 20:
                            IsListening = Q[0] == 20
                            result = self.MultipleChoiceQuestion(Q[1], Q[2], self.Answer, IsListening)

                        # Kiểm tra nếu câu hỏi là sắp xếp lại câu dạng đọc hoặc nghe  (số 0)
                        elif Q[0] == 1 or Q[0] == 21:
                            IsListening = Q[0] == 21
                            IsSpeak = bool(Q[4])
                            result = self.RearrangeSentences(Q, IsListening, IsSpeak)
                        
                        elif Q[0] == 30:
                            result = self.ConnectWord(Q)
                        
                        else:
                            result = None

                        if self.ShowBoxCorrectOrIncorrect == False:
                            if result != None:
                                self.SetResult(result)
                                # Nếu kết quả đúng
                                if result:
                                    self.IsTrueOfMultipleChoiceQuestion = True
                                    
                                    if self.ShowIconRedo == False:
                                        self.AmountOfCorrectQuestion += 1
                                
                                else:
                                    self.IsTrueOfMultipleChoiceQuestion = False

                                    self.AnswerListIncorrect.append(self.QuestionLevel[self.Question])

                                    if self.ShowIconRedo == False:
                                        self.AmountOfIncorrectQuestion += 1
                                
                                if self.JumpScared and not self.IsTrueOfMultipleChoiceQuestion and (1 + self.JumpScaredProbability) // 2 == random.randint(1, self.JumpScaredProbability):
                                    self.JumpScaredScreen = True

                                else:
                                    # Hiển thị box
                                    self.ShowBoxCorrectOrIncorrect = True

                # Hiển thị box
                if self.ShowBoxCorrectOrIncorrect:
                    # Nếu bấm nút tiếp -> Reset
                    if self.DrawBoxCorrectOrInCorrectOfMultipleChoiceQuestion():
                        self.ResetQuestionOfLevel()

                elif self.JumpScaredScreen:
                    Jump_Scare.run()

                # Hiển thị số câu hỏi
                if not self.JumpScaredScreen:
                    font(f"{self.Question + 1}/{self.AmountOfQuestion}", 75, "white",(None,10))
        
        # Nếu Làm Test Xong
        if self.Question >= self.AmountOfQuestion:
            # Nếu gặp câu Sai
            if len(self.AnswerListIncorrect) > 0:
                self.Question = 0
                self.QuestionLevel = self.AnswerListIncorrect
                self.ShowIconRedo = True
                self.AnswerListIncorrect = []
            
            else:
                self.over = True
                self.DisplayOverQuestion()
                # self.UpdateLevelOrChildLevel()
                self.IsUpdateLevel = True
        
        if self.time == 0:
            self.time += 1

        return "QuestionTest", False

    def shuffle(self, arr):
        random.shuffle(arr)
        return arr
    
    def check_MultipleChoiceQuestion(self, YourAnswer, AnswerCorrect):
        if YourAnswer == AnswerCorrect: return True
        else: return False

    def complete(self):
        if self.Achivement == True:
            if self.TimeAchivementSound == 0:
                
                self.TimeAchivementSound += 1

            IMG = pygame.transform.scale(img_list["AchivementEnd"], (400,150))
            screen.blit(IMG,(self.AchivementX, 0))
            font("Hoàn Thành Thử Thách",21, "#CC33FF",(50,0),(self.AchivementX, 0, IMG.get_width(), IMG.get_height()))

            # font("Hoàn Thành Thử Thách",21, "#CC33FF",(50,0),(screen_height-100, 0, IMG.get_width(), IMG.get_height()))

            if self.goBack == False:
                if self.AchivementX >= screen_width - 390:
                    self.AchivementX -= self.speed
                
                else:
                    currenttimeofAchivement = pygame.time.get_ticks()

                    if currenttimeofAchivement - self.FrameOfAchivement >= self.timeAchivement:
                        self.goBack == True
            
            elif self.goBack == True:
                # print(True)
                if self.AchivementX <= screen_width:
                    self.AchivementX += self.speed

    def ListeningButton(self, w = 200, h = 200, dx = 0, dy = 0):
        imgButtonSoundSpeak = pygame.transform.scale(img_list["SoundSpeak.png"],(w,h))
        imgButtonSoundSpeakrect = imgButtonSoundSpeak.get_rect(topleft = (screen_width // 2 - imgButtonSoundSpeak.get_width() // 2 + dx, 300 + dy))
        imgButtonSoundSpeak = screen.blit(imgButtonSoundSpeak,imgButtonSoundSpeakrect)

        if B.Is_Clicked(imgButtonSoundSpeakrect):
            self.speak = True
            return True

    def MultipleChoiceQuestion(self, Question : str, AnswerList : list, AnswerCorrect : int, IsListening : bool):
        dx = 50
        dy = 50

        if self.count == 0:
            self.QuestionList = self.shuffle(AnswerList).copy()
            self.count += 1

        dictionary_question = {}
        dictionary_question["red"] = [self.QuestionList[0], (dx + 100, screen_height - 200 - 20 - dy, 500, 100)]
        dictionary_question["blue"] = [self.QuestionList[1], (dx + 620, screen_height - 200 - 20 - dy, 500, 100)]
        dictionary_question["yellow"] = [self.QuestionList[2], (dx + 100, screen_height - 100 - 10 - dy, 500, 100)]
        dictionary_question["green"] = [self.QuestionList[3], (dx + 620, screen_height - 100 - 10 - dy, 500, 100)]

        if len(Question) < 40:
            size = 55
        
        else:
            size = 20
        
        if not IsListening:
            TEXT = font(Question, size, "white",(None, 300), ReturnRect=True)
            if self.LevelCurrentToLearn < 4:
                font("Chọn Đúng Nghĩa", 75, "white",(None, 100))
                pygame.draw.line(screen, "white", (TEXT.x, TEXT.y + TEXT.h - 20),(TEXT.x + TEXT.w, TEXT.h + TEXT.y - 20))

            if B.Is_Hover(TEXT):
                if self.LevelCurrentToLearn < 4:
                    width = 250
                    pygame.draw.rect(screen, "white", (screen_width // 2 - width // 2, 400, width,50), 2)
                    IMG = pygame.transform.scale(img_list["left_arrow_icon"], (50,50))
                    IMG = pygame.transform.rotate(IMG, 360-90)
                    SetColor(IMG, (255,255,255,0))
                    screen.blit(IMG, (screen_width // 2 - IMG.get_width() // 2, 400 - IMG.get_height() + 12))
                    font(AnswerCorrect, 25, "white", (0,0),(screen_width // 2 - 200 // 2, 400, 200,50))

                self.speak = True
                self.Timespeak += 1
            
            else:
                self.speak = False
                self.Timespeak = 0
        
        else:
            font("Nghe Và Chọn Đúng Nghĩa", 75, "white",(None, 100))
            # imgButtonSoundSpeak = pygame.transform.scale(img_list["SoundSpeak.png"],(200,200))
            # imgButtonSoundSpeakrect = imgButtonSoundSpeak.get_rect(topleft = (screen_width // 2 - imgButtonSoundSpeak.get_width() // 2, 300))
            # imgButtonSoundSpeak = screen.blit(imgButtonSoundSpeak,imgButtonSoundSpeakrect)

            # if B.Is_Clicked(imgButtonSoundSpeakrect):
            #     self.speak = True
            self.ListeningButton()

        red = pygame.draw.rect(screen, "red", dictionary_question["red"][1])
        blue = pygame.draw.rect(screen, "blue", dictionary_question["blue"][1])
        yellow = pygame.draw.rect(screen, (255, 153, 0), dictionary_question["yellow"][1])
        green = pygame.draw.rect(screen, "darkgreen", dictionary_question["green"][1])
        ColorsQuestion = ["red","blue","yellow","green"]

        for index in range(4):
            font(self.QuestionList[index], 25, "white", (0,0), dictionary_question[ColorsQuestion[index]][1])
        
        if ((self.speak and self.Timespeak in range(0,2)) or self.SpeakStart) and self.ShowBoxCorrectOrIncorrect == False:
            TextToSpeak = Question.replace("_",".")
            speak(TextToSpeak)
            self.speak = False
            self.SpeakStart = False
        
        if self.ShowBoxCorrectOrIncorrect == False:
            if B.Is_Clicked(red): 
                return self.check_MultipleChoiceQuestion(dictionary_question["red"][0], AnswerCorrect)
            
            elif B.Is_Clicked(blue): 
                return self.check_MultipleChoiceQuestion(dictionary_question["blue"][0], AnswerCorrect)
            
            elif B.Is_Clicked(green): 
                return self.check_MultipleChoiceQuestion(dictionary_question["green"][0], AnswerCorrect)
            
            elif B.Is_Clicked(yellow): 
                return self.check_MultipleChoiceQuestion(dictionary_question["yellow"][0], AnswerCorrect)
            
    def RearrangeSentences(self, Question, IsListening, IsSpeak):
        QT = Question[1]
        NewIndexSpeak = None

        # Random chữ
        if self.count == 0:
            self.Letters = self.shuffle(Question[2])
            self.count += 1

        # Vẽ cái đường thẳng ở giữa
        w_line = 200
        pygame.draw.line(screen, "white",(w_line,screen_height // 2), (screen_width - w_line, screen_height // 2), 2)

        # Nếu nó không phải là phần nghe
        if not IsListening:
            font(QT, 50, "white",(None, 200))
        
        else:
            # Nếu là phần nghe sẽ thêm Button

            if self.ListeningButton(150,150,0,-100):
                self.Timespeak = 0 

            # Bắt đầu nói
            if self.SpeakStart or self.Timespeak == 0:
                speak(QT)
                self.speak = False
                self.SpeakStart = False
                self.Timespeak += 1

        # Vẽ cái chữ bên dưới
        x = 200
        margin = 50
        size_l = 50

        for Index, l in enumerate(self.Letters):
            w = font(l, size_l, ReturnFontWidth=True)
            
            if Index not in self.LetterChoice:
                r = font(l, size_l, "white",(x, (screen_height + screen_height // 2) // 2 - 100), ReturnRect=True)
                if self.ShowBoxCorrectOrIncorrect == False:
                    if B.Is_Hover(r):
                        r = font(l, size_l, button_color_1,(x, (screen_height + screen_height // 2) // 2 - 100), ReturnRect=True)
                        if B.Is_Clicked(r):
                            if bool(Question[4]):
                                self.speak = True
                                self.Timespeak = 0

                            self.LetterChoice[Index] = l
                            NewIndexSpeak = Index

            x += w + margin

        # Nếu Voice True
        if IsSpeak == True:
            if self.speak and self.Timespeak == 0:
                if NewIndexSpeak != None:
                    speak(self.LetterChoice[NewIndexSpeak])
                    self.Timespeak += 1
                

        x = 200
        margin = 15
        for Index, l in self.LetterChoice.items():
            w = font(l, size_l, ReturnFontWidth=True)
            r = font(l, size_l, "white",(x, (screen_height // 2 - 75)),ReturnRect=True)

            if self.ShowBoxCorrectOrIncorrect == False:
                if B.Is_Hover(r):
                    r = font(l, size_l, button_color_1,(x, (screen_height // 2 - 75)), ReturnRect= True)

                    if B.Is_Clicked(r):
                        self.LetterChoice.pop(Index)
                        break

            x += w + margin
        
        # Nút hoàn thành
        pygame.draw.rect(screen, (0,153,51),(screen_width - 300, screen_height - 150, 200 + 5, 100 + 5))
        ButtonFinish = pygame.draw.rect(screen, (0,255,0),(screen_width - 300, screen_height - 150, 200, 100))

        font("Finish",45,"white",(0,0),(screen_width - 300, screen_height - 150, 200, 100))

        if B.Is_Clicked(ButtonFinish):
            text = list(self.LetterChoice.values())
            text = " ".join(text).capitalize()
            if text == self.Answer.capitalize():
                return True
            
            return False
    
    def ConnectWord(self, LstWord):
        # Khởi tạo word
        if self.count == 0:
            self.WordsLeft = list(LstWord[1].keys())
            self.WordsRight = list(LstWord[1].values())
            self.WordsLeft = self.shuffle(self.WordsLeft)
            self.WordsRight = self.shuffle(self.WordsRight)
            self.count += 1

        WordsLeftx = 200
        RectWordWidth = 300
        Wordsrightx = screen_width - WordsLeftx - RectWordWidth
        Wordsy = 200

        def ProcessLeftAndRightPos(pos, IndexWord):
            if pos == None:
                return IndexWord
                
            elif pos != IndexWord:
                return IndexWord
                
            else:
                return None

        for Indexword in range(len(self.WordsLeft)):
            if self.WordsLeft[Indexword] != None:
                if self.LPos == Indexword:
                    L = pygame.draw.rect(screen, button_color_1,(WordsLeftx, Wordsy, RectWordWidth, 250 // 2))
                
                else:
                    L = pygame.draw.rect(screen, "white",(WordsLeftx, Wordsy, RectWordWidth, 250 // 2),5)
                
                font(self.WordsLeft[Indexword], 30, rect = (WordsLeftx, Wordsy, RectWordWidth, 250 // 2))

                if self.ShowBoxForChild == False:
                    if B.Is_Clicked(L):
                        self.LPos = ProcessLeftAndRightPos(self.LPos, Indexword)
                        
                        if self.ChoiceWordLeft != self.WordsLeft[Indexword]:
                            self.ChoiceWordLeft = self.WordsLeft[Indexword]
                        
                        else:
                            self.ChoiceWordLeft = ""
                

            if self.WordsRight[Indexword] != None:
                if self.RPos == Indexword:
                    R = pygame.draw.rect(screen, button_color_1,(Wordsrightx, Wordsy, RectWordWidth, 250 // 2))
                
                else:
                    R = pygame.draw.rect(screen, "white",(Wordsrightx, Wordsy, RectWordWidth, 250 // 2),5)

                font(self.WordsRight[Indexword], 30, rect = (Wordsrightx, Wordsy, RectWordWidth, 250 // 2))
                
                if self.ShowBoxForChild == False:
                    if B.Is_Clicked(R):
                        self.RPos = ProcessLeftAndRightPos(self.RPos, Indexword)
                        
                        if self.ChoiceWordRight != self.WordsRight[Indexword]:
                            self.ChoiceWordRight = self.WordsRight[Indexword]
                        
                        else:
                            self.ChoiceWordRight = ""
            
            Wordsy += 150

        if self.ChoiceWordLeft != "" and self.ChoiceWordRight != "":
            if LstWord[1][self.ChoiceWordLeft] == self.ChoiceWordRight:
                self.ChoiceWordLeft = ""
                self.ChoiceWordRight = ""
                self.WordsLeft[self.LPos] = None
                self.WordsRight[self.RPos] = None
                self.LPos = None
                self.RPos = None
            
            else:
                self.ShowBoxForChild = True

        if self.ShowBoxForChild:
            pos_rect = (screen_width // 2 - (screen_width - 600) // 2, 
                screen_height // 2 - (screen_height - 600) // 2,
                screen_width - 600, 
                screen_height - 600)
            # if isTrue
            if self.TimeSound == 0:
                pygame.mixer.Sound.play(wrong)
                self.TimeSound += 1
        
            draw_rect_alpha(screen, (0,0,0,50),(0,0,screen_width,screen_height))
            pygame.draw.rect(screen, "white", pos_rect, border_radius=50)
            font("Sai rồi", 35, "red",(0,50), pos_rect)
            IMG = pygame.transform.scale(img_list["x_icon"], (150,150))
            screen.blit(IMG, ((screen_width) // 2 - IMG.get_width() // 2,
                                                   310))
            NextButton = pygame.draw.rect(screen, "red", (screen_width - 500,screen_height - 360, 150, 50), border_radius=50)
            font("OK", 35, "white",(0,0), (screen_width - 500,screen_height - 360, 150, 50))
            if B.Is_Clicked(NextButton):
                self.ShowBoxForChild = False
                self.ChoiceWordLeft = ""
                self.ChoiceWordRight = ""
                self.LPos = None
                self.RPos = None
                self.TimeSound = 0
                pygame.mixer.Sound.stop(wrong)
        
        if len(set(self.WordsLeft)) == 1 and len(set(self.WordsRight)) == 1:
            if list(set(self.WordsLeft))[0] == None and list(set(self.WordsRight))[0] == None:
                return True