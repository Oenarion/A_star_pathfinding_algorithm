import pygame as pg

pg.init()
screen = pg.display.set_mode((640, 480))
COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')
FONT = pg.font.Font(None, 32)

class InputBox:

    def __init__(self, x, y, w, h,limit, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color,(0,0,0))
        self.active = False
        self.limit=limit

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    print(self.text)
                    self.text =''
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if(event.unicode>='0' and event.unicode<='9'):
                        self.text += event.unicode
                        self.text = str(min(int(self.text),self.limit))
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(self.rect.w, self.txt_surface.get_width()+10)
        self.rect.w = width
        
    def updateLimit(self,limit):
        self.limit=limit

    def draw(self, screen):
        # Blit the rect.
        pg.draw.rect(screen,(0,0,0),self.rect)
        pg.draw.rect(screen, self.color, self.rect, 2)
        
        # Blit the text.
        half_of_rect_x=((self.rect.x+(self.rect.x+self.rect.w)+5)//2)
        
        half_of_rect_y=((self.rect.y+(self.rect.y+self.rect.h)-20)//2)
        offset=(5*(len(self.text)+1))
        screen.blit(self.txt_surface, (half_of_rect_x-offset, half_of_rect_y))
        