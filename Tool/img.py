import os

from Tool.Variable import *
path = "Asset/Icon"
img_list = {}

image_list_game = {}

def adjust_scale_image(IMG, w,h):
    return pygame.transform.scale(IMG, (w,h))

IMGS_NOT_SCALE_LIST = ["MenuCamera.png", "Mire.jpg", "PigHanji.jpg","Carrot.jpg", "Camera.png","Setting.png"]

for file in os.listdir(path):
    IMG = pygame.image.load(f"{path}/{file}")

    img_list[file.replace(".png","")] = IMG
    img_list[file.replace(".jpg","")] = IMG

img_list["Camera"] = adjust_scale_image(img_list["Camera"],100,75)
img_list["Setting"] = adjust_scale_image(img_list["Setting"], 90, 75)