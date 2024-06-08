from Tool.Variable import *
import os

pygame.init()

Sound_List = {}

path = "Asset\\Sound"
SoundListFile = os.listdir(path)

for Sound in SoundListFile:
    S = pygame.mixer.Sound(os.path.join(path, Sound))
    Sound_List[Sound.replace(".mp3","")] = S
    Sound_List[Sound.replace(".MP3","")] = S
    Sound_List[Sound.replace(".wav","")] = S