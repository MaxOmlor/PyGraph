import pygame as pg
import enum

'''class Node(pg.sprite.Sprite):
    def __init__(self, title, pos=None):
        super().__init__()
        self.title = title
        self.color = 'grey'
        self.image = pg.Surface((50, 50))
        self.image.fill(self.color)

        self.rect = self.image.get_rect()
        pos = pos if pos else (0,0)
        self.rect.topleft = pos

        self.mouse_pos_dif = None

    def update(self):
        if self.mouse_pos_dif:
            mouse_pos = pg.mouse.get_pos()
            self.rect.center = (self.mouse_pos_dif[0] + mouse_pos[0], self.mouse_pos_dif[1] + mouse_pos[1])

    
    def clicked(self, mouse_pos):
        self.mouse_pos_dif = (self.rect.center[0] - mouse_pos[0], self.rect.center[1] - mouse_pos[1])
    
    def unclicked(self, mouse_pos):
        self.mouse_pos_dif = None'''

def add_tuples(*args):
    return tuple(sum(t) for t in zip(*args))
def sub_tuples(*args):
    return tuple(a-sum(t) for a,t in zip(args[0], zip(*args[1:])))
def mul_tuples(t1, t2):
    return tuple(a*b for a,b in zip(t1, t2))

def get_text_plus_background(font, text, text_size, text_col, bg_col=None, size=None, min_size=None, anchor=(.5, .5)):
    text_font = pg.font.Font(font, text_size)
    text_surf = text_font.render(text, True, text_col)
    bg_size = size if size else text_surf.get_size()
    bg_size = (
        min_size[0] if min_size and bg_size[0] < min_size[0] else bg_size[0],
        min_size[1] if min_size and bg_size[1] < min_size[1] else bg_size[1],
    )
    bg_surf = pg.Surface(bg_size)
    if bg_col: bg_surf.fill(bg_col)
    bg_surf.blit(text_surf, sub_tuples(mul_tuples(bg_surf.get_size(),anchor), mul_tuples(text_surf.get_size(), anchor)))
    return bg_surf



    
'''class Node:
    def __init__(self, title, pos=None):
        pos = pos if pos else (0,0)
        self.pos = pos
        self.title_sprite = Sprite_Text(title, self, 24, 'Black', 'White', size=(100, 50), anchor=(1, 1))

        self.mouse_pos_dif = None

        self.sprite_list = [self.title_sprite]

    def update(self):
        if self.mouse_pos_dif:
            mouse_pos = pg.mouse.get_pos()
            self.pos = add_tuples(self.mouse_pos_dif, mouse_pos)
        #print(self.pos)

    def clicked(self, mouse_pos):
        self.mouse_pos_dif = sub_tuples(self.pos, mouse_pos)
    
    def unclicked(self, mouse_pos):
        self.mouse_pos_dif = None

    def collidepoint(self, point):
        return self.title_sprite.rect.collidepoint(point)'''


class DivType(enum.Enum):
    CANVAS      = 1
    #FLEX_FIX    = 2
    FLEX_DYN    = 3
    #ROW_FIX     = 4
    ROW_DYN     = 5
    #COL_FIX     = 6
    #COL_DYN     = 7


class Sprite_Div(pg.sprite.Sprite):
    def __init__(self, child_list=[], offset=None, min_size=(10,10), scale=None, div_type=DivType.FLEX_DYN, bg_col_idle=None, bg_col_selected=None, on_click=None, selectable=False, event_mapping=None):
        super().__init__()
        self.parent = None
        self.child_list = child_list
        self.offset = offset if offset else (0,0)
        self.min_size = min_size
        self.scale = scale
        self.div_type = div_type
        self.bg_col_idle = bg_col_idle
        self.bg_col_selected = bg_col_selected
        self.on_click = on_click

        self.size = min_size
        self.rect = pg.Rect(self.offset, self.min_size)
        self.image = None

        self.selectable = selectable
        self.event_mapping = event_mapping
        self.selected_childs = []
    
    def update(self):
        for child in self.child_list:
            child.parent = self

        if not self.rect:
            raise ValueError('self.rect is None.')

        '''if self.div_type == DivType.CANVAS:
            for child in self.child_list:
                child.rect = pg.Rect(add_tuples(self.rect.topleft, child.offset), child.min_size)
        elif self.div_type == DivType.FLEX_DYN:
            current_offset = (0,0)
            width, height = self.rect.size
            line_max_y = 0
            for child in self.child_list:
                if current_offset[0]+child.min_size[0] > width:
                    current_offset = (0, current_offset[1]+line_max_y)
                    line_max_y = 0

                child.rect = pg.Rect(current_offset, child.min_size)
                current_offset = add_tuples(current_offset, (child.min_size[0], 0))
                line_max_y = line_max_y if line_max_y > child.min_size[1] else child.min_size[1]
            self.rect.size = (width, current_offset[1]+line_max_y)
        elif self.div_type == DivType.ROW_DYN:
            current_offset_y = 0
            max_x = 0
            for child in self.child_list:
                child.rect = pg.Rect((0,current_offset_y), child.min_size)
                current_offset_y += child.min_size[1]
                max_x = max_x if max_x > child.min_size[0] else child.min_size[0]
            self.rect.size = (max_x, current_offset_y)'''

        for child in self.child_list:
            child.size = None

        for child in self.child_list:
            child.update()
        
        if self.div_type == DivType.CANVAS:
            for child in self.child_list:
                child.rect = pg.Rect(add_tuples(self.rect.topleft, child.offset), child.size)
            self.size = self.size if self.size else self.min_size
        elif self.div_type == DivType.FLEX_DYN:
            current_offset = (0,0)
            width, height = self.rect.size
            line_max_y = 0
            for child in self.child_list:
                if current_offset[0]+child.size[0] > width:
                    current_offset = (0, current_offset[1]+line_max_y)
                    line_max_y = 0

                child.rect = pg.Rect(current_offset, child.size)
                current_offset = add_tuples(current_offset, (child.size[0], 0))
                line_max_y = line_max_y if line_max_y > child.size[1] else child.size[1]
            self.size = self.size if self.size else (width, current_offset[1]+line_max_y)
        elif self.div_type == DivType.ROW_DYN:
            current_offset_y = 0
            max_x = 0
            for child in self.child_list:
                child.rect = pg.Rect((0,current_offset_y), child.size)
                current_offset_y += child.size[1]
                max_x = max_x if max_x > child.size[0] else child.size[0]
            self.size = self.size if self.size else (max_x, current_offset_y)
            for child in self.child_list:
                child.rect.width = max_x

        self.image = pg.Surface(self.size)
        self.rect.size = self.size
            
        if self.bg_col_selected and self in self.parent.selected_childs:
            self.image.fill(self.bg_col_selected)
        elif self.bg_col_idle:
            self.image.fill(self.bg_col_idle)
        for child in self.child_list:
            self.image.blit(child.image, child.rect.topleft)
    
    def collidepoint(self, mouse_pos) -> bool:
        if self.rect.collidepoint(mouse_pos):
            for child in self.child_list:
                if child.collidepoint(sub_tuples(mouse_pos, self.rect.topleft)):
                    return True
            if self.on_click: self.on_click(self, mouse_pos)
            if self.selectable and self.parent:
                self.parent.select_child(self)
            return True
        return False
    
    def select_child(self, child):
        if child in self.child_list:
            if child in self.selected_childs:
                self.selected_childs.remove(child)
            self.selected_childs.append(child)

    def handle_events(self, mouse_pos, event_list):
        if not self.rect.collidepoint(mouse_pos):
            return False
        
        for child in self.child_list:
            if child.handle_events(sub_tuples(mouse_pos, self.rect.topleft), event_list):
                return True

        if not self.event_mapping:
            return False
        for event in event_list:
            key = (event.type, event.key, None) if hasattr(event, 'key') else (event.type, None, None)
            if key in self.event_mapping:
                self.event_mapping[key](self)
                #print(f'handle_events {self.child_list=}')
                return True
        return False
        

class Sprite_Text(pg.sprite.Sprite):
    def __init__(self, text, text_size='12', text_col='Black', offset=None, min_size=(10,10), scale=None, bg_col='White', anchor=(.5, .5)):
        super().__init__()
        self.parent = None
        self.text = text
        self.text_size = text_size
        self.text_col = text_col
        self.min_size = min_size
        self.size = min_size
        self.scale = scale
        self.bg_col = bg_col
        self.anchor = anchor
        self.image = None
        self.rect = None
        self.offset = offset if offset else (0,0)

    def update(self):
        self.image = get_text_plus_background(
            font=None,
            text=self.text,
            text_size=self.text_size,
            text_col=self.text_col,
            bg_col=self.bg_col,
            size=self.size,
            min_size=self.min_size,
            anchor=self.anchor)
        self.size = self.image.get_rect().size

    def collidepoint(self, mouse_pos) -> bool:
        return False

    def handle_events(self, mouse_pos, event_list):
        return False

class Sprite_InputField(pg.sprite.Sprite):
    def __init__(self, text='', text_size='12', text_col='Black', offset=None, min_size=(10,10), scale=None, bg_col='White', anchor=(.5, .5)):
        super().__init__()
        self.parent = None
        self.text = text
        self.text_size = text_size
        self.text_col = text_col
        self.min_size = min_size
        self.scale = scale
        self.bg_col = bg_col
        self.anchor = anchor
        self.image = None
        self.rect = None
        self.offset = offset if offset else (0,0)
        self.aktive = False

    def update(self):
        self.image = get_text_plus_background(None, self.text, self.text_size, self.text_col, self.bg_col, self.rect.size, self.anchor)

    def collidepoint(self, mouse_pos) -> bool:
        return False

    def handle_events(self, mouse_pos, event_list):
        return False

