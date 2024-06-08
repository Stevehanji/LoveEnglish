from Tool.Variable import *

running = True

def BoxPercent(percent):
    global running
    padding = 5
    screen.fill((19,31,36))
    font("Vui lòng đợi",75,"white",(None, screen_height // 2 - 100))
    font(f"{percent}%",75,"white",(screen_width - 200, screen_height // 2 + 25))

    pygame.draw.rect(screen, "black",(screen_width // 2 - 800 // 2 - padding, 
                                      screen_height // 2 - 100 // 2 + 100 - padding, 
                                      800 + padding * 2,
                                      100 + padding * 2))
    
    pygame.draw.rect(screen, "white",(screen_width // 2 - 800 // 2, 
                                      screen_height // 2 - 100 // 2 + 100, 
                                      800,
                                      100))
    
    pygame.draw.rect(screen, "red",(screen_width // 2 - 800 // 2, 
                                      screen_height // 2 - 100 // 2 + 100, 
                                      percent * 8,
                                      100))

    pygame.display.update()

if running:
    BoxPercent(0)

    from Display.display import *
    BoxPercent(20)

    # AIMAinModule = importlib.import_module("AIMain.CameraAppAI")
    from AIMain.CameraAppAI import *
    BoxPercent(30)
    
    from Game.PlayGame import *
    BoxPercent(50)
    
    import os
    BoxPercent(70)
    
    from Game.CreateWorld import *
    BoxPercent(80)
    
    from Tool.Sound_List import *
    BoxPercent(90)
    
    from StoreData.Setting import DataStore
    BoxPercent(100)

class EnglishGameApp():
    def __init__(self):
        self.DisplayTieuChuanIsShow = False
        self.running = True
        self.style = "dark"
        self.display = "Hoc"
        self.clock = pygame.time.Clock()
        self.FPS = 60

        self.TimeToEndJumpScare = 5
        self.CurrentTimeToEndJumpScare = 0

        self.CreateWorld = CreateWorld()

        # User / Admin
        self.Permission = "User"

        Var_Obj.IsFinishButtonAdmin = False
        self.IsClicked = False

        try:
            
            if DataStore.SettingData["Permission"] == "4B686F615675416E644368616E40383139323230313031323334":
                self.Permission = "Admin"
                Var_Obj.IsAdmin = True
                Var_Obj.IsFinishButtonAdmin = True
        except: pass

        #               Left   Right
        self.scroll = [False, False]

    def draw(self, event):
        screen.fill(display_color[self.style]["Background"])

        if self.display != "PlayGame" and self.display != "CreateWorld":
            if self.display == "Hoc":
                self.display, self.DisplayTieuChuanIsShow = Hoc(self.display, self.scroll)
            
            elif self.display == "Setting":
                self.display = Setting(self.display)
            
            elif self.display == "FlashCard":
                self.display, self.DisplayTieuChuanIsShow = DisplayFlashCard(self.display, event)
            
            elif self.display == "Game":
                self.display, self.DisplayTieuChuanIsShow = GameDisplay(self.display, self.Permission)
            
            elif self.display == "Camera":
                self.display = CameraDisplay(self.display)
        
        elif self.display == "PlayGame":
            self.display = game.RunGame(self.display)
        
        elif self.display == "CreateWorld":
            self.display = self.CreateWorld.run(self.display)
        
        if self.DisplayTieuChuanIsShow:
            self.display, self.DisplayTieuChuanIsShow = display_tieu_chuan(self.style, self.display)
        
        if subject.showbox:
            subject.drawBox()
    
    def run(self):
        while self.running and Var_Obj.IsJumpApp == False:
            self.StoreObjectFalse = [Object.IsShowBoard, Object.JumpScared,
                                     Object.ShowGateLocked, Object.IsShowDoorLocked
                                     ]
    
            self.StoreObjectNone = [Object.CorrectGate]

            self.clock.tick(self.FPS)
            events = pygame.event.get()
            
            Object.event = events
            self.draw(events)

            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.display == "CreateWorld":
                        if event.button == 1:
                            self.CreateWorld.style, self.CreateWorld.choose_block_x, self.CreateWorld.choose_block_y = self.CreateWorld.update_map_data(self.CreateWorld.map_data, 
                                                                                            self.CreateWorld.style, 
                                                                                            self.CreateWorld.bg_x,
                                                                                            self.CreateWorld.bg_y, 
                                                                                            page = self.CreateWorld.page, 
                                                                                            block_list=block_list)
                            
                        if event.button == 3:
                            self.CreateWorld.update_map_data(self.CreateWorld.map_data, -1, self.CreateWorld.bg_x,
                                                             self.CreateWorld.bg_y, page=self.CreateWorld.page)
                
                if event.type == pygame.KEYDOWN:
                    if self.display != "PlayGame" and self.display != "CreateWorld":
                        if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                            self.scroll[0] = True
                        
                        if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                            self.scroll[1] = True
                    
                        if event.key == pygame.K_ESCAPE and subject.showbox == True:
                            subject.showbox = False
                        
                        elif event.key == pygame.K_ESCAPE and subject.YesToLearn:
                            subject.ResetQuestion()
                            LevelComplete.stop()
                        
                        elif subject.JumpScaredScreen == True:
                            subject.JumpScaredScreen = False
                            subject.ResetQuestionOfLevel()
                            Jump_Scare.ResetAll()

                    
                    # Player Game KEY DOWN
                    elif self.display == "PlayGame":
                        if True not in self.StoreObjectFalse and True not in self.StoreObjectNone:
                            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                                game.Player.move_left = True

                            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                                game.Player.move_right = True

                            if event.key == pygame.K_w or event.key == pygame.K_UP:
                                game.Player.jump = True
                            
                            if event.key == pygame.K_RETURN:
                                game.ContactGate = True
                                game.ContactWoodenBoard = True
                                game.ContactDoor = True
                            
                            if event.key == pygame.K_ESCAPE:
                                game.RemoveAllSprite()
                                game.ResetAll()
                                game.NewLevel(1)
                                Object.Level = 1
                                Object.NextLevel = None
                                self.display = "Game"
                        
                        elif Object.JumpScared:
                            if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN and self.CurrentTimeToEndJumpScare > self.TimeToEndJumpScare * 10:
                                game.RemoveAllSprite()
                                game.ResetAll()
                                Object.JumpScared = False

                                if Object.CorrectGate == False:
                                    Object.CorrectGate = None
                        
                        elif Object.IsShowBoard:
                            if event.key == pygame.K_ESCAPE:
                                Object.IsShowBoard = False
                                Object.TextBoard = ""
                                game.TextList = []
                                game.styleLanguage = 0
                                game.TextVietNamese = None
                        
                        elif Object.ShowGateLocked:
                            if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                                Object.ShowGateLocked = False
                                game.TextList = []
                                game.styleLanguage = 0
                                game.TextVietNamese = None

                        elif Object.IsShowDoorLocked:
                            if event.key == pygame.K_ESCAPE:
                                Object.IsShowDoorLocked = False
                                game.styleLanguage = 0

                    # Create Map KEYDOWN
                    elif self.display == "CreateWorld":
                        if self.CreateWorld.IsTyping == False:
                            if event.key == pygame.K_b:
                                self.CreateWorld.show = not self.CreateWorld.show
                                
                            if event.key == pygame.K_v:
                                self.CreateWorld.PutBlockHold = not self.CreateWorld.PutBlockHold
                                
                            if event.key == pygame.K_d:
                                self.CreateWorld.move_right = True

                            if event.key == pygame.K_a:
                                self.CreateWorld.move_left = True
                            
                            if event.key == pygame.K_w:
                                self.CreateWorld.move_up = True

                            if event.key == pygame.K_s:
                                self.CreateWorld.move_down = True
                                
                            if event.key == pygame.K_LSHIFT:
                                self.CreateWorld.speed = 10

                            if self.CreateWorld.choose_block == False:
                                if event.key == pygame.K_LEFT and self.CreateWorld.page > 1:
                                    self.CreateWorld.page -= 1
                                    self.CreateWorld.style = None
                                    
                                if event.key == pygame.K_RIGHT and self.CreateWorld.page * 11 < len(block_list):
                                    self.CreateWorld.page += 1
                                    self.CreateWorld.style = None
                                
                                elif self.CreateWorld.choose_block == True:
                                    if event.key == pygame.K_LEFT:
                                        self.CreateWorld.map_data[self.CreateWorld.choose_block_y][self.CreateWorld.choose_block_x].x -= self.CreateWorld.speed_block
                                
                            if event.key == pygame.K_ESCAPE and self.CreateWorld.style != None:
                                self.CreateWorld.style = None
                            
                            elif event.key == pygame.K_ESCAPE and self.CreateWorld.choose_block:
                                self.CreateWorld.choose_block = False
                                self.CreateWorld.choose_block_x = None
                                self.CreateWorld.choose_block_y = None
                            
                            elif event.key == pygame.K_ESCAPE:
                                self.display = "Game"
                                self.CreateWorld.ResetAll()


                    if Var_Obj.IsFinishButtonAdmin and self.display not in ["PlayGame","CreateWorld"] and not subject.YesToLearn:
                        if event.key == pygame.K_9:
                            Var_Obj.IsAdmin = not Var_Obj.IsAdmin
                            self.Permission = "Admin" if Var_Obj.IsAdmin else "User"

                if event.type == pygame.KEYUP:
                    if self.display != "PlayGame" and self.display != "CreateWorld":
                        if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                            self.scroll[0] = False
                    
                        if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                            self.scroll[1] = False
                    
                    # Play Game KEY UP
                    elif self.display == "PlayGame":
                        if True not in self.StoreObjectFalse and True not in self.StoreObjectNone:
                            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                                game.Player.move_left = False

                            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                                game.Player.move_right = False

                            if event.key == pygame.K_w or event.key == pygame.K_UP:
                                game.Player.jump = False

                    # Create World
                    elif self.display == "CreateWorld":
                        if event.key == pygame.K_d:
                            self.CreateWorld.move_right = False

                        if event.key == pygame.K_a:
                            self.CreateWorld.move_left = False
                        
                        if event.key == pygame.K_w:
                            self.CreateWorld.move_up = False

                        if event.key == pygame.K_s:
                            self.CreateWorld.move_down = False
                        
                        if event.key == pygame.K_LSHIFT:
                            self.CreateWorld.speed = 5
            
            if Object.JumpScared:
                self.CurrentTimeToEndJumpScare += 1
            
            else:
                self.CurrentTimeToEndJumpScare = 0

            pygame.display.update()
        
        pygame.quit()

if __name__ == "__main__":
    EnglishGameApp().run()
    SaveDataSetting("Setting", DataStore.SettingData)

    DataStore.StudyData["Level"] = subject.level
    DataStore.StudyData["ChildLevelList"] = subject.ChildLevel
    SaveDataSetting("Study", DataStore.StudyData)

    if Var_Obj.IsJumpApp:
        # CameraAppAI(DataStore.SettingData["Camera"]).run()
        CameraAppAI(1).run()

    try:
        os.remove("StoreData\\sound.mp3")
    except:
        pass
    
    SaveFileFlashCard(flashcard.Data, Var_Obj.Store_FlashCard)