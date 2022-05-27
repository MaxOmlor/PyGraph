import pygame as pg
import sys
from sys import exit

from Packages.PyGameAddOnsPackage.PyGameAddOns import MouseSprite
from Packages.NodesPackage.PyNodes import Sprite_Div, Sprite_Text, DivType

win_caption = "PyGraph"
win_size = (800,400)
fps = 60

pg.init()
pg.display.set_caption(win_caption)
screen = pg.display.set_mode(win_size)
clock = pg.time.Clock()

#mouse_idle_path = 'res/images/mouse/mouse_idle.png'
#mouse_clicked_path = 'res/images/mouse/mouse_clicked.png'
#mouse = MouseSprite(mouse_idle_path, mouse_clicked_path)
#mouse_group = pg.sprite.Group()
#mouse_group.add(mouse)

node_list = []
selection = []
clickable_sprites = []
clicked_sprite = None

def close_window():
    pg.quit()
    exit()

def add_node():
    global node_list, clickable_sprites, clicked_sprite
    print('add new node')
    mouse_pos = pg.mouse.get_pos()

    new_node = Node('New Node', mouse_pos)
    node_list.append(new_node)
    clickable_sprites.append(new_node)

    new_node.clicked(mouse_pos)
    clicked_sprite = new_node

event_func_mapper = {
    (pg.QUIT, None, None): close_window,
    (pg.KEYDOWN, pg.K_a, None): add_node
}


'''while True:
    for event in pg.event.get():
        #print(event)
        key = (event.type, event.key, None) if hasattr(event, 'key') else (event.type, None, None)
        if key in event_func_mapper: event_func_mapper[key]()

        if event.type == pg.MOUSEBUTTONDOWN:
            for s in clickable_sprites:
                if s.collidepoint(event.pos):
                    s.clicked(event.pos)
                    clicked_sprite = s
                    break
        if event.type == pg.MOUSEBUTTONUP:
            if clicked_sprite: clicked_sprite.unclicked(event.pos)

    screen.fill('black')

    node_group = pg.sprite.Group()
    for node in node_list:
        node.update()
        for s in node.sprite_list:
            node_group.add(s)
    node_group.update()
    node_group.draw(screen)
    

    #mouse_group.update()
    #mouse_group.draw(screen)

    pg.display.update()
    clock.tick(fps)'''


background_div = Sprite_Div(
    child_list=[
        Sprite_Div(
            child_list=[
                Sprite_Text('Hallo Welt!', 18, min_size=(80,24), bg_col='White'),
                Sprite_Text('123', 18, min_size=(50,24), bg_col='White'),
                Sprite_Text('abc', 18, min_size=(50,24), bg_col='White'),
            ],
        div_type=DivType.ROW_DYN, min_size=(100,200), offset=(20,20),
        selectable=True, bg_col_idle='Black', bg_col_selected='Grey'),
        Sprite_Div(
            child_list=[
                Sprite_Text('Hallo Welt!', 18, min_size=(80,24), bg_col='White'),
                Sprite_Text('123', 18, min_size=(50,24), bg_col='White'),
                Sprite_Text('abc', 18, min_size=(50,24), bg_col='White'),
            ],
        div_type=DivType.ROW_DYN, min_size=(100,200), offset=(20,200),
        selectable=True, bg_col_idle='Black', bg_col_selected='Grey'),
    ],
    min_size=(300,300), div_type=DivType.CANVAS, bg_col_idle='Blue',
    event_mapping={
        (pg.KEYDOWN, pg.K_ESCAPE, None): lambda div: div.selected_childs.clear(),
    })

while True:
    event_list = pg.event.get()
    for event in event_list:
        #print(event)
        #key = (event.type, event.key, None) if hasattr(event, 'key') else (event.type, None, None)
        #if key in event_func_mapper: event_func_mapper[key]()
        if event.type == pg.QUIT:
            close_window()

        if event.type == pg.MOUSEBUTTONDOWN:
            background_div.collidepoint(event.pos)

    background_div.handle_events(pg.mouse.get_pos(), event_list)

    screen.fill('black')
    
    background_div.update()
    screen.blit(background_div.image, background_div.offset)

    pg.display.update()
    clock.tick(fps)