from Tool.Button import *

b1 = Button(100,100,300,100,button_color)
Nut_Hoc = Button(60, 750, 250, 100, button_color)
Nut_Flash_Card = Button(370, 750, 250, 100, button_color)
Nut_Choi = Button(680, 750, 250, 100, button_color)

# Flash Card
def adjust_center(width1, width2):
    return width1 // 2 - width2 // 2

ButtonBack = Button(50, 50, 50, 50, "white")

w_nut_flash_card_menu = 475
h_nut_flash_card_menu = 150
Nut_hoc_FlashCard_Theo_Chu_de = Button(adjust_center(screen_width, w_nut_flash_card_menu + 70) - 300,200,
                            w_nut_flash_card_menu + 70,h_nut_flash_card_menu, button_color)
Nut_tao_flash_card = Button(adjust_center(screen_width, w_nut_flash_card_menu),200,
                            w_nut_flash_card_menu,h_nut_flash_card_menu, button_color)
Nut_Flash_Card_Cua_Ban = Button(adjust_center(screen_width, w_nut_flash_card_menu) - 300,460
                                , w_nut_flash_card_menu, h_nut_flash_card_menu, button_color)

Nut_Hoc_Flash_Card_Cua_Ban = Button(adjust_center(screen_width, w_nut_flash_card_menu + 80),460
                                , w_nut_flash_card_menu + 80, h_nut_flash_card_menu, button_color)

Nut_light_and_dark = Button1()

# Create Box FlashCard
# "#f2726a"

# "#242628"
BoxFlashCard = Button(100,250,300,325, "#f2726a")
# BoxFlashCard = Button(60,200,225,250, "white")

TrashBinButton = Button(screen_width - 100, screen_height // 2 - 75 // 2, 75, 75, "white")

# NhanDienQuaHinhAnhButton = Button(600, 375, 500, 75, button_color)
NhanDienQuaCameraButton = Button(600, 400, 500, 75, button_color)

CreateButton = Button(screen_width - 125, 50, 75,75, "gray")

SaveCreateWorldButton = Button(screen_width - 200,50,100,50, "lime")