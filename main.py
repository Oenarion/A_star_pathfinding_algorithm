import pygame
import sys
import inputBox as inp
import button
import node
import time
import heapq
from tkinter import *
from tkinter import messagebox

pygame.init()

WIDTH=600
HEIGHT=600

GRID_SIZE=(WIDTH,HEIGHT)
WIN = pygame.display.set_mode(size=GRID_SIZE)

WHITE=(255,255,255)
BLACK=(0,0,0)
RED=(220,0,0)
BLUE=(0,0,220)
GREEN=(0,220,0)
PURPLE=(128,0,128)
ORANGE=(255,165,0)

WIN.fill(WHITE)
FONT = pygame.font.Font(None, 32)

rows,cols=0,0
cell_size=0

starting_point=(0,0)
goal_point=(2,2)


#  A* Search Algorithm
# 1.  Initialize the open list
# 2.  Initialize the closed list
#     put the starting node on the open 
#     list (you can leave its f at zero)

# 3.  while the open list is not empty
#     a) find the node with the least f on 
#        the open list, call it "q"

#     b) pop q off the open list
  
#     c) generate q's 8 successors and set their 
#        parents to q
   
#     d) for each successor
#         i) if successor is the goal, stop search
        
#         ii) else, compute both g and h for successor
#           successor.g = q.g + distance between 
#                               successor and q
#           successor.h = distance from goal to 
#           successor

#           successor.f = successor.g + successor.h

#         iii) if a node with the same position as 
#             successor is in the OPEN list which has a 
#            lower f than successor, skip this successor

#         iV) if a node with the same position as 
#             successor  is in the CLOSED list which has
#             a lower f than successor, skip this successor
#             otherwise, add  the node to the open list
#      end (for loop)
  
#     e) push q on the closed list
#     end (while loop)


def astar(maze, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = node.Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = node.Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = set()                # <-- closed_list must be a set

    # Add the start node
    heapq.heapify(open_list)
    heapq.heappush(open_list, start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = heapq.heappop(open_list)

        for item in open_list:
            if item.f < current_node.f:
                current_node = item


        # Pop current off open list, add to closed list
        closed_list.add(current_node)     # <-- change append to add

        # Found the goal
        if current_node == end_node:
            cost=current_node.f
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            print("returning ",path[::-1],cost)
            return path[::-1],cost # Return reversed path and cost

        # Generate children
        children=get_neighbors(current_node,maze)

        # Loop through children
        for child in children:

            # Child is on the closed list
            if child in closed_list:              # <-- remove inner loop so continue takes you to the end of the outer loop
                continue

            # Create the f, g, and h values
            heuristic(child,current_node,end_node)

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            heapq.heappush(open_list,child)
    return [],-1


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
def update_board(curr_pos,visitable_points):
    if visitable_points[curr_pos[0]][curr_pos[1]]==False:
        pygame.draw.rect(WIN,BLACK,((cell_size*curr_pos[0])+2,(cell_size*curr_pos[1])+2,cell_size-1,cell_size-1))
        visitable_points[curr_pos[0]][curr_pos[1]]=True
    else:
        if curr_pos!=starting_point and curr_pos!=goal_point:
            pygame.draw.rect(WIN,WHITE,((cell_size*curr_pos[0])+2,(cell_size*curr_pos[1])+2,cell_size-1,cell_size-1))
        visitable_points[curr_pos[0]][curr_pos[1]]=False
    return visitable_points
    
    
#simple heuristic for the computation    
def heuristic(child,current_node,end_node):
    child.g = current_node.g + 1
    child.h = abs(((child.position[0] - end_node.position[0]))) + abs(((child.position[1] - end_node.position[1])))
    child.f = child.g + child.h

def get_neighbors(current_node,maze):
    children = []
    for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]: # Adjacent squares

        # Get node position
        node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

        # Make sure within range
        if node_position[0] > (rows - 1) or node_position[0] < 0 or node_position[1] > (cols -1) or node_position[1] < 0:
            continue

        # Make sure walkable terrain
        if maze[node_position[0]][node_position[1]] == False:
            continue

        # Create new node
        new_node = node.Node(current_node, node_position)

        # Append
        children.append(new_node)

    return children

# def draw_current_path(open_list,node):
#     # if node!=starting_point:
#     pygame.draw.rect(WIN,PURPLE,((cell_size*node.position[0])+2,(cell_size*node.position[1])+2,cell_size-1,cell_size-1))
#     for possible_nodes in open_list:  
#         pygame.draw.rect(WIN,ORANGE,((cell_size*possible_nodes[1].position[0])+2,(cell_size*possible_nodes[1].position[1])+2,cell_size-1,cell_size-1))
#     pygame.display.update()
#     time.sleep(1)

def draw_path(path):
    for i in range(1,len(path)-1):
        pygame.draw.rect(WIN,GREEN,((cell_size*path[i][0])+2,(cell_size*path[i][1])+2,cell_size-1,cell_size-1))
    pygame.display.update()
        
        
def main():
    draw_initial_board(rows,cols)
    
    maze=[[True for i in range(cols)] for i in range(rows)]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    path,cost=astar(maze,starting_point,goal_point)
                    if cost==-1:
                        messagebox.showerror('ERROR','NO PATH POSSIBLE')
                        main_menu()
                        
                    draw_path(path)
                    messagebox.showinfo('COST','total cost is: '+str(cost))
                    main_menu()
                # if event.key == pygame.K_q:
                #     path,cost=draw_find_path(start,goal,visitable_points)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos=pygame.mouse.get_pos()
                maze=update_board((mouse_pos[0]//cell_size,mouse_pos[1]//cell_size),maze)
            
        pygame.display.update()

def main_menu():
    global rows,cols,starting_point,goal_point
    
    #resize if we going back to main menu
    WIN = pygame.display.set_mode(size=(WIDTH,HEIGHT))
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
    