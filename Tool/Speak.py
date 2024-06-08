import pygame
import importlib
def speak(text):
    tts=importlib.import_module("gtts").gTTS(text=text,lang="en")
    tts.save("StoreData\\sound.mp3")
    s = pygame.mixer.Sound("StoreData\\sound.mp3")
    s.stop()
    pygame.mixer.Sound.play(s)
    s.set_volume(0.5)

ding = pygame.mixer.Sound("Asset/Sound/Yes.mp3")
wrong = pygame.mixer.Sound("Asset/Sound/No.mp3")
LevelComplete = pygame.mixer.Sound("Asset/Sound/LevelComplete.mp3")
Complete = pygame.mixer.Sound("Asset/Sound/Complete.mp3")