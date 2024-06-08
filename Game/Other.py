from Tool.Variable import *
from Tool.image_game import *
# from googletrans import Translator
import importlib

translator = importlib.import_module("googletrans").Translator()

class JumpScare:
    def __init__(self):
        self.JumpScareSound = pygame.mixer.Sound("Asset/Sound/JumpScare.MP3")
        self.Maxscale = 800
        self.ResetAll()
    
    def ResetAll(self):
        self.CurrentScale = 1
        self.solan = 0
        self.JumpScareSound.stop()

    def run(self):
        screen.fill("black")

        if self.solan == 0:
            self.JumpScareSound.play()
            self.solan = 1

        if self.CurrentScale < self.Maxscale:
            self.CurrentScale += self.CurrentScale * 5


        else:
            self.CurrentScale = self.Maxscale

        IMG = pygame.transform.scale(image_game["Other-JumpScare1"], (self.CurrentScale,self.CurrentScale))
        screen.blit(IMG, (screen_width // 2 - IMG.get_width() // 2,
                          screen_height // 2 - IMG.get_height() // 2))

def TranslateToVietNam(text):
    return translator.translate(text, dest="vi", src = "en").text

Jump_Scare = JumpScare()