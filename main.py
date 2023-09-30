import pygame
import sys
import inputBox as inp
import button

pygame.init()

WIDTH=600
HEIGHT=600

GRID_SIZE=(WIDTH,HEIGHT)
WIN = pygame.display.set_mode(size=GRID_SIZE)

WHITE=(255,255,255)
BLACK=(0,0,0)

WIN.fill(WHITE)
FONT = pygame.font.Font(None, 32)

rows,cols=0,0

def draw_initial_board(rows,cols):
    cell_x,cell_y=WIDTH//rows,HEIGHT//cols
    WIN = pygame.display.set_mode(size=(cell_x*rows,cell_y*cols))
    WIN.fill(WHITE)
    for i in range(rows):
        for j in range(cols):
            pygame.draw.rect(WIN,BLACK,((cell_x*i)+2,(cell_y*j+2),cell_x-1,cell_y-1))
    pygame.draw.rect(WIN,WHITE,((cell_x*rows)-1,0,1,(cell_y*cols)))
    pygame.draw.rect(WIN,WHITE,(0,(cell_y*cols)-1,(cell_x*rows),1))
def main():
    draw_initial_board(rows,cols)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                ...
        pygame.display.update()

def main_menu():
    global rows,cols
    
    WIDTH_BOX=150
    HEIGHT_BOX=50
    
    inp_box1=inp.InputBox((WIDTH//2)-(WIDTH_BOX//2),(HEIGHT//2)-2*HEIGHT_BOX,WIDTH_BOX,HEIGHT_BOX)
    inp_box2=inp.InputBox((WIDTH//2)-(WIDTH_BOX//2),(HEIGHT//2)-HEIGHT_BOX,WIDTH_BOX,HEIGHT_BOX)
    start_button=button.Button((WIDTH//2)-50,(HEIGHT//2),100,50,"GO")

    boxes=[inp_box1,inp_box2]

    text1="rows"
    text2="cols"

    txt_surface1 = FONT.render(text1, True,(0,0,0))
    txt_surface2 = FONT.render(text2, True,(0,0,0))
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            for box in boxes:
                box.handle_event(event)
            if start_button.handle_event(event):
                rows=inp_box1.text
                cols=inp_box2.text
                if rows!='' and cols!='':
                    rows=int(rows)
                    cols=int(cols) 
                    if rows>0 and cols>0:
                        main()
            start_button.update_hover()

        for box in boxes:
            box.update()
        WIN.fill(WHITE)
        WIN.blit(txt_surface1, (145, 210))
        WIN.blit(txt_surface2, (150, 265))
        
        for box in boxes:
            box.draw(WIN)
            
        start_button.draw(WIN)
        pygame.display.update()

if __name__ == "__main__":
    main_menu()
    