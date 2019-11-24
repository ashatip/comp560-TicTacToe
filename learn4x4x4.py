import numpy as np
import random

import sys


#original global declaration at top of code

### this finds if the oppoent has three in a row, not the main person
isThreeInRow_x = False
threeInRowLoc_x = np.array([-1,-1,-1])
isThreeInRow_o = False
threeInRowLoc_o = np.array([-1,-1,-1])



def setThreeInRow(val, loc,sign):
    if sign==.1:
        global isThreeInRow_x
        global threeInRowLoc_x
        isThreeInRow_x = val
        threeInRowLoc_x = loc
    else:
        global isThreeInRow_o
        global threeInRowLoc_o
        isThreeInRow_o = val
        threeInRowLoc_o = loc




def getThreeInRow(sign):
    if (sign==.1):
        global isThreeInRow_x
        global threeInRowLoc_x
        return isThreeInRow_x, threeInRowLoc_x
    else:
        global isThreeInRow_o
        global threeInRowLoc_o
        return isThreeInRow_o, threeInRowLoc_x
    
#playes the game a number of times with a learning parameter
def play_game(num):
    learn_rate=.9
    discount_rate=.95
    x_board=[]
    x_score=[]
    o_board=[]
    o_score=[]
    for i in range(0,num):
        grid,x_board,x_score,o_board,o_score=setupGame(x_board,x_score,o_board,o_score,learn_rate,discount_rate,
                                                       print_=False,move_type="learn")
    return (x_board,x_score,o_board,o_score)

#pathX or pathO is a gird with each location has a number where X and O is played
def update_path(loc,current_path,move_num):
    current_path[loc[0],loc[1],loc[2]]=move_num
    return current_path
    
    
def setupGame(x_board,x_score,o_board,o_score,learn_rate,discount_rate,print_=False,move_type="learn"):
    ## X is .1
    ## O is -.1
    #setup grid
    
    grid=np.zeros(shape=(4,4,4),dtype=np.dtype('float64'))
    #there can be max 64 plays
    x_move=1
    o_move=1
    x_path=np.zeros(shape=(4,4,4),dtype=np.dtype('i4'))
    o_path=np.zeros(shape=(4,4,4),dtype=np.dtype('i4'))
    for i in range(0,32):
        # x moves
        if move_type=="rand":
            grid,loc=rand_move(grid,.1)
        elif move_type=="learn":
            grid,loc=learn_move(grid,.1,x_board,x_score)
        #check if game is over
        x_path=update_path(loc,x_path,x_move)
        x_move=x_move+1
        solved,direction=checkWinner(grid,.1,loc)
        if solved:
            if print_:
                print("X wins")
                print("loc= ")
                print(loc)
                print("direction= ")
                print(direction)
            x_board,x_score=first_update_learn(x_path.copy(),o_path.copy(),grid.copy(),"winner",x_board,x_score,learn_rate,discount_rate)
            o_board,o_score=first_update_learn(o_path.copy(),x_path.copy(),grid.copy(),"loser",o_board,o_score,learn_rate,discount_rate)
            return (grid,x_board,x_score,o_board,o_score)
        # o moves
        if move_type=="rand":
            grid,loc=rand_move(grid,-.1)
        elif move_type=="learn":
            grid,loc=learn_move(grid,-.1,o_board,o_score)
        o_path=update_path(loc,o_path,o_move)
        o_move=o_move+1
        solved,direction=checkWinner(grid,-.1,loc)
        if solved:
            
            if print_:
                print("O wins")
                print("loc= ")
                print(loc)
                print("direction= ")
                print(direction)
            x_board,x_score=first_update_learn(x_path.copy(),o_path.copy(),grid.copy(),"loser",x_board,x_score,learn_rate,discount_rate)
            o_board,o_score=first_update_learn(o_path.copy(),x_path.copy(),grid.copy(),"winner",o_board,o_score,learn_rate,discount_rate)
            return (grid,x_board,x_score,o_board,o_score)
    if print_:
        print("tie")
    x_board,x_score=first_update_learn(x_path.copy(),o_path.copy(),grid.copy(),"tie",x_board,x_score,learn_rate,discount_rate)
    o_board,o_score=first_update_learn(o_path.copy(),x_path.copy(),grid.copy(),"tie",o_board,o_score,learn_rate,discount_rate)
    return (grid,x_board,x_score,o_board,o_score)

def rand_move(grid,sign):
    #dummy move, used for setup testing
    i=0
    while(True):
        x=random.randint(0,3)
        y=random.randint(0,3)
        z=random.randint(0,3)
        if not grid[x,y,z]:
            grid[x,y,z]=sign
            return (grid,list([x,y,z]))
        
        
def learn_move(grid,sign,board,score):
    ##
    ###dom place
    ##
#     isThreeInRow, threeInRowLoc=getThreeInRow()
#     if isThreeInRow:
#         grid[threeInRowLoc[0],threeInRowLoc[0],threeInRowLoc[0]]=sign
#         setThreeInRow(False,(0,0,0))
#         return (grid,threeInRowLoc)
    ##add if find a 3 in a row for itself use it
    ## add if it finds a opponets 3 in a row, get the place
    ## add if it finds a possible fork, with one move, make 3 in a row without any oppent blocking it
    ## add if it finds an oppenent possible fork, with one move the oppenent can make 3 in a row without you blocking it
    
    #if we are in new board: pick a random spot
    if sign==.1:
        not_sign=-.1
    else:
        not_sign=.1
    val_s,loc_s=getThreeInRow(sign)
    val_n,loc_n=getThreeInRow(not_sign)
    if val_s:
        grid[loc_s[0],loc_s[1],loc_s[2]]=sign
        return (grid,loc_s)
    elif val_n:
        grid[loc_n[0],loc_n[1],loc_n[2]]=sign
        return (grid,loc_n)
    if (len(board)==0):
        return rand_move(grid,sign)
    elif (np.array_equal(board,grid)):
        new_index=0
    new_index=np.where((board == grid).all(axis=1).all(axis=1).all(axis=1))[0]
    if len(new_index)==0:
        return rand_move(grid,sign)
    else:
        i_a,j_a,k_a=np.where(score[new_index[0]] == np.max(score[new_index[0]]))
        x=np.random.choice(len(i_a), 1)
        i=i_a[x][0]
        j=j_a[x][0]
        k=k_a[x][0]
        grid[i,j,k]=sign
        return (grid,list([i,j,k]))
    #the moves that learns

    
def checkWinner(grid,sign,loc):
    #goes through every direction in x,y,z directions
    spot=grid[loc[0],loc[1],loc[2]]
    for i in [0,1]:
        for j in [0,1]:
            for k in [0,1]:
                if(i==j==k==0):
                    next
                #some directions can have negative chooses so dealing with that
                else:
                    solved,direction=setDirection(grid,sign,loc,[i,j,k])
                    if solved:
                        return (True, direction)
    return (False,0)

#changes vector's part to negative if needed
def setDirection(grid,sign,loc,direction):
    #one direction, 
    if sum(direction)==1:
        return checkDirection(grid,sign,loc,direction)
    if sum(direction)==2:
        #trying to find the zero
        for i in range(0,3):
            if direction[i]==0:
                break
        # i is the location of the zero:
        # based on my studying:
        #even direction is when both dimesions are positive
        #odd direction is when one of the dimesions are negative
        #based on studies:
        ## if both the dimesions that have nonzero direction are the same then the:
            ###direction is positive
        ## if the dimesions that have nonzero direction have the sum of three 
            ###direction is negative
        loc=list(loc)
        new_loc=loc.copy()
        new_loc.pop(i)
        if new_loc[0]==new_loc[1]:
            return checkDirection(grid,sign,loc,direction)
        elif sum(new_loc)%4==3:
                if i==0:
                    direction[1]=direction[1]*-1
                else:
                    direction[0]=direction[0]*-1
                return checkDirection(grid,sign,loc,direction)
        #else, it does not work for that side
        return (False,0)
    else:
        #so the direction is based on where are the two equal values are located
            ##the direction of the equal values should be the same but the other dimension
        #direction is (1,1,1): values are all the same
        ###if they are all not equal then there is no 3d directional diagonal
        if len(set(loc))==1:
            return checkDirection(grid,sign,loc,direction)
        elif len(set(loc))==2:
            for i in range(len(direction)):
                loc=list(loc)
                new_loc=loc.copy()
                new_loc.pop(i)
                if len((new_loc))==1:
                    direction[i]=direction[i]*-1
                    break
            if (loc[i]+loc[(i+1)%3])%4==3:        
                return checkDirection(grid,sign,loc,direction)
            else:
                return (False, 0)
        else:
            return (False,0)
#updated check direction
def checkDirection(grid,sign,loc,direction):
    #checks if the blocks in that direction have the same sign
    let =np.zeros(shape=(3),dtype=np.int)
    hasBlank = False
    for i in range(0,4):
        for j in range(len(direction)):
            #used mod because I did not want to check the opposite direction
            let[j]=(direction[j]*(i)+loc[j])%4
        if grid[let[0],let[1],let[2]]!=sign:
            if (grid[let[0],let[1],let[2]] == 0 and not hasBlank):
                hasBlank = True
                blankLoc = (let[0], let[1], let[2])
            else:
                setThreeInRow(False, (-1,-1,-1),sign)
                return False,0

    
    if(hasBlank):
        setThreeInRow(True, blankLoc,sign)
        return False, 0
    else:
        setThreeInRow(False, (-1,-1,-1),sign)
        return True,direction

    
def q_update_learn(current_path,other_current_path,grid,board,score,learn_rate,index,discount_rate):
    #not the starting update learn function but a recursive one
    #find the last step of other player
    e_a,f_a,g_a=np.where(other_current_path == np.max(other_current_path))
    #set that spot empty to go back in time
    e=e_a[0]
    f=f_a[0]
    g=g_a[0]
    grid[e,f,g]=0
    other_current_path[e,f,g]=0
    
    #find latest step
    i_a,j_a,k_a=np.where(current_path == np.max(current_path))
    #set that spot empty to go back in time
    i=i_a[0]
    j=j_a[0]
    k=k_a[0]
    grid[i,j,k]=0
    current_path[i,j,k]=0
    #go to next latest step
    x,y,z=np.where(current_path == np.max(current_path))
    #check if the current board is in the playing boards
    if np.array_equal(board,grid):
        new_index=[0]
        print("this should not run")
    if len(board.shape)!=4:
            board=np.append([board],[grid],axis=0)
            cur_score=np.zeros(shape=(4,4,4),dtype=np.dtype('float64'))
            cur_score[x,y,z]=np.max(score)*learn_rate*discount_rate
            score=np.append([score],[cur_score],axis=0)
            new_index=np.where((board == grid).all(axis=1).all(axis=1).all(axis=1))
    elif len(np.where((board == grid).all(axis=1).all(axis=1).all(axis=1))[0])==0:
            board=np.append(board,[grid],axis=0)
            cur_score=np.zeros(shape=(4,4,4),dtype=np.dtype('float64'))
            cur_score[x,y,z]=np.max(score[index])*learn_rate*discount_rate

            score=np.append(score,[cur_score],axis=0)
            new_index=np.where((board == grid).all(axis=1).all(axis=1).all(axis=1))
    else:
        new_index=np.where((board == grid).all(axis=1).all(axis=1).all(axis=1))[0]
        score[new_index[0]][x[0]][y[0]][z[0]]=np.max(score[index])*learn_rate*discount_rate+score[new_index[0]][x[0]][y[0]][z[0]]*(1-learn_rate)
    if np.max(current_path)>1:
        return q_update_learn(current_path,other_current_path,grid,board,score,learn_rate,new_index[0],discount_rate)
    else:
        return (board,score)    
#the first learning function that is called
def first_update_learn(current_path,other_current_path,grid,status,board,score,learn_rate,discount_rate):
    len_board=False
    if not (len(board)>0):
        index=[]
        len_board=True
    else:
        index=np.where((board == grid).all(axis=1).all(axis=1).all(axis=1))
    #if o wins, x and o played the same number of moves
    #if x wins, x played one more move
    #if tie, o and x played the same number
    #alogrithm default is x wins or tie
    if np.max(current_path)<np.max(other_current_path):
        x,y,z=np.where(other_current_path == np.max(other_current_path))
        grid[x[0]][y[0]][z[0]]=0
        other_current_path[x[0]][y[0]][z[0]]=0
    if status=="winner":
        #location of the last move
        i,j,k=np.where(current_path == np.max(current_path))
        #checks if it is previously had an example

        #if not
        if len(index)==0:
            #add the grid to the boards
            if len_board:
                board=grid.copy()
            else:
                board=np.append(board,[grid],axis=0)
            #add the scoring board
            cur_score=np.zeros(shape=(4,4,4),dtype=np.dtype('float64'))
            cur_score[i,j,k]=1
            if len_board:
                score=cur_score.copy()
                index=[0]
            else:
                score=np.append(score,[cur_score],axis=0)
                index=np.where((board == grid).all(axis=1).all(axis=1).all(axis=1))
        else:
            if len(index[0])==0:
                board=np.append(board,[grid],axis=0)
                cur_score=np.zeros(shape=(4,4,4),dtype=np.dtype('float64'))
                cur_score[i,j,k]=1
                score=np.append(score,[cur_score],axis=0)
                index=np.where((board == grid).all(axis=1).all(axis=1).all(axis=1))[0]
            score[index[0]][i[0]][j[0]][k[0]]=score[index[0]][i[0]][j[0]][k[0]]*(1-learn_rate)+1*learn_rate*discount_rate
        
        return q_update_learn(current_path,other_current_path,grid,board,score,learn_rate,index[0],discount_rate)
    #same thing as winner but instead of adding one to the score, it takes away from it 
    elif status=="loser":
        i,j,k=np.where(current_path == np.max(current_path))
        if len(index)==0:
            if len_board:
                board=grid.copy()
            else:
                board=np.append(board,[grid],axis=0)
            cur_score=np.zeros(shape=(4,4,4),dtype=np.dtype('float64'))
            cur_score[i,j,k]=-1
            if len_board:
                score=cur_score.copy()
                index=[0]
            else:
                score=np.append(score,[cur_score],axis=0)
                index=np.where((board == grid).all(axis=1).all(axis=1).all(axis=1))
        else:
            if len(index[0])==0:
                board=np.append(board,[grid],axis=0)
                cur_score=np.zeros(shape=(4,4,4),dtype=np.dtype('float64'))
                cur_score[i,j,k]=-1
                score=np.append(score,[cur_score],axis=0)
                index=np.where((board == grid).all(axis=1).all(axis=1).all(axis=1))[0]               
            else:
                score[index[0]][i[0]][j[0]][k[0]]=score[index[0]][i[0]][j[0]][k[0]]*(1-learn_rate)-1*learn_rate*discount_rate
    
        return q_update_learn(current_path,other_current_path,grid,board,score,learn_rate,index[0],discount_rate)
    else:
        ##tie
        i,j,k=np.where(current_path == np.max(current_path))
        if len(index)==0:
            if len_board:
                board=grid.copy()
            else:
                board=np.append(board,[grid],axis=0)
            cur_score=np.zeros(shape=(4,4,4),dtype=np.dtype('float64'))
            cur_score[i,j,k]=0
            if len_board:
                score=cur_score.copy()
                index=[0]
            else:
                score=np.append(score,[cur_score],axis=0)
                index=np.where((board == grid).all(axis=1).all(axis=1).all(axis=1))
        else:
            if len(index[0])==0:
                board=np.append(board,[grid],axis=0)
                cur_score=np.zeros(shape=(4,4,4),dtype=np.dtype('float64'))
                cur_score[i,j,k]=0
                score=np.append(score,[cur_score],axis=0)
                index=np.where((board == grid).all(axis=1).all(axis=1).all(axis=1))[0]  
            score[index[0]][i[0]][j[0]][k[0]]=score[index[0]][i[0]][j[0]][k[0]]*(1-learn_rate)
        
        return q_update_learn(current_path,other_current_path,grid,board,score,learn_rate,index[0],discount_rate)
    
    
if len(sys.argv) > 1:
    print(sys.argv)
    for i in sys.argv:
        if (i =='learn4x4x4.py'):
            next
        else:
            print(play_game(int(float(i))))
