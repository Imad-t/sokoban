import pygame as pg

# percentage macro
pct = lambda x, d : (x*d/100)

def new_window(win_width:int = 800, win_height:int = 600, title:str = 'sokoban'):
    win_size = (win_width, win_height)
    pg.init()
    pg.display.set_caption(title)
    screen = pg.display.set_mode(win_size)
    
    #total height 100%h, total width 125%h
    margin_5 = pct(win_height, 5)
    margin_2 = pct(win_height, 2)
    margin_20 = pct(win_height, 20)
    margin_90 = pct(win_height, 90)
    
    board = {
        # reference height both times because fixed ascpect ratio is assumed
        # (relative)
        'pos' : (margin_5, margin_5),
        'size' : (margin_90, margin_90)
    }
    menu = {
        # reference height both times because fixed ascpect ratio is assumed
        # (relative)
        'pos' : (board['pos'][0] + margin_5, margin_5),
        'size' : (margin_20, margin_90)
    }
    
    timer = {
        # reference height both times because fixed ascpect ratio is assumed
        # (relative)
        'pos' : (menu['pos'][0] + margin_2, menu['pos'][0] + menu['size'][0] - margin_2),
        'size' : (margin_5, margin_20)
    }