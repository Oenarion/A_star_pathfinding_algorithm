import pygame as pg

pg.init()
COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')
FONT = pg.font.Font(None, 32)

class Button:
    
    def __init__(self, x, y, w, h, text):
        self.rect=pg.Rect(x,y,w,h)
        self.text=text
        self.color=COLOR_INACTIVE
        self.text_surface=FONT.render(self.text,True,self.color,(0,0,0))
        self.active = False
        
    def handle_event(self,event):
        if event.type==pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                return True 
            return False
    
    def update_hover(self):
        mouse_pos_x,mouse_pos_y=pg.mouse.get_pos()
        if mouse_pos_x>=self.rect.x and mouse_pos_x<=self.rect.x+self.rect.w and mouse_pos_y>=self.rect.y and mouse_pos_y<=self.rect.y+self.rect.h:
            self.active=True
            self.color=COLOR_ACTIVE
        else:
            self.active=False
            self.color=COLOR_INACTIVE
        self.text_surface=FONT.render(self.text,True,self.color,(0,0,0))
    
    def draw(self, screen):
        # Blit the rect.
        pg.draw.rect(screen,(0,0,0),self.rect)
        pg.draw.rect(screen, self.color, self.rect, 2)
        
        # Blit the text.
        half_of_rect_x=((self.rect.x+(self.rect.x+self.rect.w))//2)
        half_of_rect_y=((self.rect.y+(self.rect.y+self.rect.h)-20)//2)
        offset=(5*(len(self.text)+1))
        screen.blit(self.text_surface, (half_of_rect_x-offset, half_of_rect_y))