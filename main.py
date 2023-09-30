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
RED=(220,0,0)
BLUE=(0,0,220)

WIN.fill(WHITE)
FONT = pygame.font.Font(None, 32)

rows,cols=0,0
cell_size=0

starting_point=(0,0)
goal_point=(2,2)

#DRAWS THE BOXES FOR ALGORITHM
def draw_initial_board(rows,cols):
    print(starting_point,goal_point)
    global cell_size
    cell_x,cell_y=WIDTH//rows,HEIGHT//cols
    cell_size=min(cell_x,cell_y)
    WIN = pygame.display.set_mode(size=(cell_size*rows,cell_size*cols))
    WIN.fill(WHITE)
    
    for i in range(rows):
        for j in range(cols):
            pygame.draw.rect(WIN,BLACK,((cell_size*i)+2,(cell_size*j+2),cell_size-1,cell_size-1))
    pygame.draw.rect(WIN,WHITE,((cell_size*rows)-1,0,1,(cell_size*cols)))
    pygame.draw.rect(WIN,WHITE,(0,(cell_size*cols)-1,(cell_size*rows),1))
    
    pygame.draw.rect(WIN,RED,((cell_size*starting_point[0])+2,(cell_size*starting_point[1])+2,cell_size-1,cell_size-1))
    pygame.draw.rect(WIN,BLUE,((cell_size*goal_point[0])+2,(cell_size*goal_point[1])+2,cell_size-1,cell_size-1))
    

#updates the current grid, if we want to create some walls
def update_board(curr_pos):
    if curr_pos!=starting_point and curr_pos!=goal_point:
        pygame.draw.rect(WIN,WHITE,((cell_size*curr_pos[0])+2,(cell_size*curr_pos[1])+2,cell_size-1,cell_size-1))
    
#TO DO..
#A* ALGO
def find_path():
    ...
        
def main():
    draw_initial_board(rows,cols)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.K_SPACE:
                find_path()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos=pygame.mouse.get_pos()
                update_board((mouse_pos[0]//cell_size,mouse_pos[1]//cell_size))
            
        pygame.display.update()

def main_menu():
    global rows,cols,starting_point,goal_point
    
    WIDTH_BOX=150
    HEIGHT_BOX=50
    
    inp_box1=inp.InputBox((WIDTH//4)-(WIDTH_BOX//2),(HEIGHT//2)-3*HEIGHT_BOX,WIDTH_BOX,HEIGHT_BOX,70,"2")
    inp_box2=inp.InputBox((WIDTH//4)-(WIDTH_BOX//2),(HEIGHT//2)-HEIGHT_BOX,WIDTH_BOX,HEIGHT_BOX,70,"2")
    
    start_box1=inp.InputBox(((WIDTH//2))+WIDTH_BOX//2,(HEIGHT//2)-3*HEIGHT_BOX,WIDTH_BOX//2,HEIGHT_BOX,1,"0")
    start_box2=inp.InputBox(((WIDTH//2))+WIDTH_BOX,(HEIGHT//2)-3*HEIGHT_BOX,WIDTH_BOX//2,HEIGHT_BOX,1,"0")
    
    end_box1=inp.InputBox(((WIDTH//2))+WIDTH_BOX//2,(HEIGHT//2)-HEIGHT_BOX,WIDTH_BOX//2,HEIGHT_BOX,1,"1")
    end_box2=inp.InputBox(((WIDTH//2))+WIDTH_BOX,(HEIGHT//2)-HEIGHT_BOX,WIDTH_BOX//2,HEIGHT_BOX,1,"1")
    
    start_button=button.Button((WIDTH//2)-50,(HEIGHT//2),100,50,"GO")

    boxes=[inp_box1,inp_box2,start_box1,start_box2,end_box1,end_box2]

    text1="rows"
    text2="cols"
    text3="starting coord"
    text4="goal coord"

    txt_surface1 = FONT.render(text1, True,(0,0,0))
    txt_surface2 = FONT.render(text2, True,(0,0,0))
    txt_surface3 = FONT.render(text3, True,(0,0,0))
    txt_surface4 = FONT.render(text4, True,(0,0,0))
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            #update limits of coordinates, changes color of selected box
            for i in range(len(boxes)):
                boxes[i].handle_event(event)
                if i==0 and boxes[i].text!='':
                    start_box1.updateLimit(int(boxes[i].text)-1)
                    end_box1.updateLimit(int(boxes[i].text)-1)
                if i==1 and boxes[i].text!='':
                    start_box2.updateLimit(int(boxes[i].text)-1)
                    end_box2.updateLimit(int(boxes[i].text)-1)
                    
            #starts the A* algorithm
            if start_button.handle_event(event):
                rows=inp_box1.text
                cols=inp_box2.text
                if rows!='' and cols!='':
                    rows=int(rows)
                    cols=int(cols) 
                    if start_box1.text!='' and start_box2.text!='' and end_box1.text!='' and end_box2.text!='':
                        starting_point=(int(start_box1.text),int(start_box2.text))
                        goal_point=(int(end_box1.text),int(end_box2.text))
                    if rows>1 and cols>1 and starting_point!=goal_point:
                        print(starting_point,goal_point)
                        main()
            start_button.update_hover()

        #updates the box if needed
        for box in boxes:
            box.update()
            
        #redraws the board
        WIN.fill(WHITE)
        
        WIN.blit(txt_surface1, ((WIDTH//4)-22, ((HEIGHT//2) - 4*HEIGHT_BOX)+20))
        WIN.blit(txt_surface2, ((WIDTH//4)-22, ((HEIGHT//2) - 2*HEIGHT_BOX)+20))
        
        WIN.blit(txt_surface3, ((WIDTH//2)+75, ((HEIGHT//2) - 4*HEIGHT_BOX)+20))
        WIN.blit(txt_surface4, ((WIDTH//2)+90, ((HEIGHT//2) - 2*HEIGHT_BOX)+20))
        
        for box in boxes:
            box.draw(WIN)
            
        start_button.draw(WIN)
        pygame.display.update()

if __name__ == "__main__":
    main_menu()
    