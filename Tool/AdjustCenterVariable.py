from Tool.Variable import *

def adjust_center_width(img = None, style = (None, screen_width), o = None):
    """
        style[0] : x
        style[1] : width
    """
    if img != None:
        if style[0] == None:
            return style[1] // 2 - img.get_width() // 2
        
        if style[0] != None:
            return style[0] + style[1] // 2 - img.get_width() // 2
    
    if img == None:
        if o == None:
            return style[1] // 2 - style[0] // 2
        
        if o != None:
            return style[0] + style[1] // 2 - o // 2
    
def adjust_center_height(img = None, style = (None, screen_height), o = None):
    """
        style[0] : x
        style[1] : width
    """
    if img != None:
        if style[0] == None:
            return style[1] // 2 - img.get_height() // 2
        
        if style[0] != None:
            return style[0] + style[1] // 2 - img.get_height() // 2
    
    if img == None:
        if o == None:
            return style[1] // 2 - style[0] // 2
    
        if o != None:
            return style[0] + style[1] // 2 - o // 2