from Tool.Variable import *
from Tool.AdjustCenterVariable import *


from Tool.img import *

class Button:
    def __init__(self, x, y, w, h, color):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.clicked = False
        self.color_old = color
    
    def create_rect_button(self, rect, color_hover, mouse = 1):
        result = False
        pos = pygame.mouse.get_pos()
        if rect.collidepoint(pos):
            if color_hover != None:
                self.color = color_hover

            if pygame.mouse.get_pressed()[0] == mouse and self.clicked == False:
                self.clicked = True
                result = True

        else:
            self.color = self.color_old

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        
        return result

    def create_border(self, border, color_hover):
        if len(border) > 0:
            border += [0] * (4 - len(border))

            border_color = border[0]

            if (self.color != self.color_old) and color_hover != None:
                border_color = color_hover

            if border[1] != None:
                pygame.draw.rect(screen, border_color, (self.x - border[1],
                                                    self.y - border[1],
                                                    self.w + border[1] * 2,
                                                    self.h + border[1] * 2),
                                                    border_radius=border[2])
   
    def draw_Button_with_text(self, text : str, size : int, 
                              color : tuple = (255,255,255),
                              color_hover = None,
                              border : list = []) -> bool:
        """
            border:

            0 : color_border
            1 : border_width
            2 : border_raidus
        """
        # Create Border
        # if len(border) > 0:
        self.create_border(border, color_hover)

        # Create Button
        Button_rect = pygame.draw.rect(screen,self.color,(self.x, self.y, self.w, self.h), border_radius=border[2])

        font(text, size, color, rect=(self.x, self.y, self.w, self.h))
        return self.create_rect_button(Button_rect, color_hover)
    
    def draw_Button_with_image(self, img, color_hover = None,
                            padding = 0,
                              border : list = [], dx = 0):
        
        self.create_border(border, color_hover)
        img = pygame.transform.scale(img, (self.w - padding * 2, self.h - padding * 2))

        Button_rect = pygame.draw.rect(screen,self.color,(self.x, self.y, self.w, self.h))
        screen.blit(img, (self.x + padding + dx, self.y + padding))
        return self.create_rect_button(Button_rect, color_hover)



    # Custome Box Button
    def DrawBoxFlashCard(self, index, name):
        action = False
        pos = pygame.mouse.get_pos()

        if self.x == None or self.y == None or self.w == None or self.h == None:
            raise Exception("biến pos bằng giá trị None")
        
        img = pygame.transform.scale(img_list["FlashCardImg"], (100,100)).convert_alpha()
        dx = (index - 1) * 400
        pygame.draw.rect(screen, self.color, (self.x + dx, self.y, self.w, self.h), border_radius=10)

        screen.blit(img, (adjust_center_width(img, (self.x + dx, self.w)),
                          adjust_center_height(img,(self.y, self.h)) - 70))

        # Viết Tiêu đề
        font(name, 25, "black",(0, 20), (self.x + dx, self.y,self.w,self.h))

        # Vẽ Nút Học
        x_detail = adjust_center_width(style = (self.x + dx, self.w), o = 150)
        y_detail = adjust_center_height(style = (self.y, self.h), o = 50) + 70
        detail = pygame.draw.rect(screen, "#242628", (x_detail, y_detail + 30, 150, 50), border_radius=10)
        font("Học", 25, "white",(0, 30), (x_detail, y_detail, 150, 50))
        
        # Nếu bấm nút học
        if detail.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
        
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        return action

class Button1:
    def __init__(self):
        self.clicked = False
    
    def Is_Clicked(self, surface):
        pos = pygame.mouse.get_pos()
        result = False
        if surface.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                result = True
        
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        
        return result
    
    def Is_Hover(self, surface):
        pos = pygame.mouse.get_pos()
        if surface.collidepoint(pos):
            return True

B = Button1()