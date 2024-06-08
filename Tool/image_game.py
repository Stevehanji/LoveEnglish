import os
# from Tool.Variable import *
import pygame

image_game = {}
path = "Asset\\Game"
for file in os.listdir(path):
    ImageFile = os.path.join(path,file)

    for InFile in os.listdir(ImageFile):
        IMG = pygame.image.load(os.path.join(ImageFile, InFile))
        image_game[file + "-" + InFile.replace(".png", "")] = IMG
        image_game[file + "-" + InFile.replace(".jpg", "")] = IMG