import pygame as pg

class MouseSprite(pg.sprite.Sprite):
    def __init__(self, image_idle_path, image_clicked_path=None):
        super().__init__()
        self.image_idle = pg.image.load(image_idle_path)
        image_clicked_path = image_clicked_path if image_clicked_path else image_clicked_path
        self.image_clicked = pg.image.load(image_clicked_path)

        self.image = self.image_idle
        self.rect = self.image.get_rect()

    def clicked(self, clicked):
        self.image = self.image_clicked if clicked else self.image_idle
    def update(self):
        self.rect.center = pg.mouse.get_pos()
        self.clicked(any(pg.mouse.get_pressed()))

