import copy
import time

COLUMNS=["a","b","c","d","e","f","g","h"]
ROWS=["1","2","3","4","5","6","7","8"]

WHITE=set(["P","K","Q","B","N","R"])
BLACK=set(["p","k","q","b","n","r"])
SCORE={"P":1,"K":0,"Q":9,"B":3,"N":3,"R":5,"p":-1,"k":0,"q":-9,"b":-3,"n":-3,"r":-5," ":0}
MATE=99999999




reached=set([])

flag1=False
flag2=False

def get_score (board):
    ret=0
    for i in range(0,8):
        for j in range(0,8):
            ret+=SCORE[board[i][j]]
    return ret


def minmax(board,to_move,layer):
    global flag1
    global flag2
    #if flag1==True and flag2==True:
    #    for i in range(7,-1,-1):
    #        print(board[i])    
    #    flag2=False
    if layer>6:
        return [get_score(board),[],[]]    
    if str(board) in reached:                       #ACCOUNT FOR FINAL LINE LATER
        return [to_move*10000000000000,[],[]]

    else:
        reached.add(str([board,layer]))
    best=[]
    start=[]
    best_value=to_move*-1*1000000000000
    found_move=False
    f=False
    ki=-1
    kj=-1
    if to_move==1:
        for i in range(0,8):
            if "K" in board[i]:
                j=board[i].index("K")
                if board[i][j]=="K":
                    ki=i
                    kj=j
                    f=True
                    break
                    
    else:
        for i in range(0,8):
            if "k" in board[i]:
                j=board[i].index("k")
                if board[i][j]=="k":
                    ki=i
                    kj=j
                    f=True
                    break
    #if ki==-1 or kj==-1:
    #    for i in range(7,-1,-1):
    #        print(board[i])    
    #    print(to_move)
    #    print(layer)
    for i in range(0,8):
        for j in range(0,8):
            if board[i][j]==" ":
                continue
            if to_move==1 and board[i][j] in WHITE:
                if board[i][j]=="K":
                    possible=king_move(board,i,j,1)
                    for k in range(0,len(possible)):
                        new_board=make_move(copy.deepcopy(board),[i,j],possible[k])
                        if check_check(new_board,possible[k][0],possible[k][1],to_move)==True:
                            continue
                        found_move=True
                        comp_score=minmax(new_board,to_move*-1,layer+1)
                        if comp_score[0]==MATE:
                            return [MATE,[i,j],possible[k]]
                        if comp_score[0]>best_value:
                            best_value=comp_score[0]
                            best=possible[k]
                            start=[i,j]
                elif board[i][j]=="N":
                    #ADD OTHER PIECES
                    possible=knight_move(board,i,j,1)
                    #if layer==5:
                    #    print("found")
                    #    for l in range(7,-1,-1):
                    #        print(board[l])    
                    #    print(to_move)
                    #    print(layer)                        
                    for k in range(0,len(possible)):
                        #if possible[k]==[5,2] and layer==1:
                            #print("found")
                            #print(best_value)
                        #    flag1=True
                        #if layer==3 and j==7 and flag1==True and k==1 and board[5][2]=="N":
                            #print(board[5][2])
                            #print("next")
                        #    flag2=True
                        new_board=make_move(copy.deepcopy(board),[i,j],possible[k])
                        if check_check(new_board,ki,kj,to_move)==True:
                            continue                        
                        found_move=True
                        comp_score=minmax(new_board,to_move*-1,layer+1)
                        if comp_score[0]==MATE:
                            return [MATE,[i,j],possible[k]]                        
                        if comp_score[0]>best_value:
                            best_value=comp_score[0]
                            best=possible[k]
                            start=[i,j]
            
            elif to_move==-1 and board[i][j] in BLACK:
                if board[i][j]=="k":
                    possible=king_move(board,i,j,-1)
                    for k in range(0,len(possible)):
                        new_board=make_move(copy.deepcopy(board),[i,j],possible[k])
                        if check_check(new_board,possible[k][0],possible[k][1],to_move)==True:
                            continue
                        found_move=True
                        comp_score=minmax(new_board,to_move*-1,layer+1)
                        if comp_score==-MATE:
                            return [-MATE,[i,j],possible[k]]                            
                        if comp_score[0]<best_value:
                            best_value=comp_score[0]
                            best=possible[k]
                            start=[i,j]
                elif board[i][j]=="n":
                    #ADD OTHER PIECES
                    possible=knight_move(board,i,j,-1)
                    for k in range(0,len(possible)):
                        if k==3 and possible[k]==[5,5] and flag1==True and layer==2:
                            flag2=True
                        new_board=make_move(copy.deepcopy(board),[i,j],possible[k])
                        if check_check(new_board,ki,kj,to_move)==True:
                            continue                         
                        found_move=True
                        comp_score=minmax(new_board,to_move*-1,layer+1)
                        if comp_score==-MATE:
                            return [-MATE,[i,j],possible[k]]                        
                        if comp_score[0]<best_value:
                            best_value=comp_score[0]
                            best=possible[k]
                            start=[i,j]
    if found_move==False:
        #print(f,ki,kj)
        if check_check(board,ki,kj,to_move)==False:
            return [0,[],[]]
        else:
            return [MATE*to_move*-1,[],[]]
    return [best_value,start,best]
                        

                            


def make_move(board,start,end):
    to_move=board[start[0]][start[1]]
    board[start[0]][start[1]]=" "
    board[end[0]][end[1]]=to_move
    return board

def knight_move(board,startx,starty,to_move):
    possible=[]
    x_val=[-2,-2,-1,-1,1,1,2,2]
    y_val=[-1,1,-2,2,-2,2,-1,1]
    curr=""
    currx=-1
    curry=-1
    for i in range(0,8):
        currx=startx+x_val[i]
        curry=starty+y_val[i]
        if currx>7 or curry>7 or currx<0 or curry<0:
            continue
        curr=board[currx][curry]
        if to_move==1:
            #ADD IN PINS LATER
            if curr in WHITE:
                continue
            else:
                possible.append([currx,curry])
        else:
            if curr in BLACK:
                continue
            else:
                possible.append([currx,curry])
    return possible

def king_move(board,startx,starty,to_move):
    possible=[]
    x_val=[-1,-1,-1,0,0,1,1,1]
    y_val=[1,0,-1,-1,1,1,0,-1]
    curr=""
    currx=-1
    curry=-1
    for i in range(0,8):
        currx=startx+x_val[i]
        curry=starty+y_val[i]
        if currx>7 or curry>7 or currx<0 or curry<0:
            continue
        curr=board[currx][curry]
        if to_move==1:
            if curr in WHITE or check_check(board,currx,curry,to_move)==True:
                continue
            else:
                possible.append([currx,curry])
        else:
            if curr in BLACK or check_check(board,currx,curry,to_move)==True:
                continue
            else:
                possible.append([currx,curry])
    return possible    


def rook_move(board,startx,starty,to_move):
    possible=[]
    x_val=[1,-1,0,0]
    y_val=[0,0,-1,1]
    curr=""
    for i in range(0,4):
        currx=startx
        curry=starty
        for j in range(1,8):
            currx+=x_val[i]
            curry+=y_val[i]
            if currx>7 or curry>7 or currx<0 or curry<0:
                break
            curr=board[currx][curry]
            if to_move==1:
                if check_check(board,currx,curry,to_move)==True:
                    continue
                elif curr in WHITE:
                    break
                else:
                    possible.append([currx,curry])
            else:
                if check_check(board,currx,curry,to_move)==True:
                    continue                
                if curr in BLACK:
                    break
                else:
                    possible.append([currx,curry])            
    return possible


def bishop_move(board,startx,starty,to_move):
    possible=[]
    x_val=[1,1,-1,-1]
    y_val=[-1,1,-1,1]
    curr=""
    for i in range(0,4):
        currx=startx
        curry=starty
        for j in range(1,8):
            currx+=x_val[i]
            curry+=y_val[i]
            if currx>7 or curry>7 or currx<0 or curry<0:
                break
            curr=board[currx][curry]
            if to_move==1:
                if check_check(board,currx,curry,to_move)==True:
                    continue
                elif curr in WHITE:
                    break
                else:
                    possible.append([currx,curry])
            else:
                if check_check(board,currx,curry,to_move)==True:
                    continue                
                if curr in BLACK:
                    break
                else:
                    possible.append([currx,curry])           
    return possible



def check_check(board,startx,starty,to_move):
    #ADD OTHER SHIT LATER
    x_val=[-1,-1,-1,0,0,1,1,1]
    y_val=[1,0,-1,-1,1,1,0,-1]    
    if to_move==1:
        possible=knight_move(board,startx,starty,1)
        for i in range(0,len(possible)):
            if board[possible[i][0]][possible[i][1]]=="n":
                return True
        currx=-1
        curry=-1
        for i in range(0,8):
            currx=startx+x_val[i]
            curry=starty+y_val[i]
            if currx>7 or curry>7 or currx<0 or curry<0:
                continue
            if board[currx][curry]=="k":
                return True
    else:
        possible=knight_move(board,startx,starty,-1)
        for i in range(0,len(possible)):
            if board[possible[i][0]][possible[i][1]]=="N":
                return True
        currx=-1
        curry=-1
        for i in range(0,8):
            currx=startx+x_val[i]
            curry=starty+y_val[i]
            if currx>7 or curry>7 or currx<0 or curry<0:
                continue
            if board[currx][curry]=="K":
                return True        
    return False
    #for x in range(0,8):
    #    for y in range(0,8):
    #        #ADD IN OTHER PIECES LATER
    #        if to_move==1:
    #            if board[x][y] in WHITE or board[x][y]==" ":
    #                continue
    #            if board[x][y]=="n":
    #                possible=knight_move(board,x,y,-1)
    #                if[startx,starty] in possible:
    #                    return True
    #            elif board[x][y]=="k":
    #                if abs(startx-x)<=1 and abs(starty-y)<=1:
    #                    return True
    #        else:
    #            if board[x][y] in BLACK or board[x][y]==" ":
    #                continue
    #            if flag1==True and flag2==True:
    #                print(board[x][y])
    #            if board[x][y]=="N":
    #                possible=knight_move(board,x,y,1)
    #                if[startx,starty] in possible:
    #                    return True
    #            elif board[x][y]=="K":
    #                if abs(startx-x)<=1 and abs(starty-y)<=1:
    #                    return True                 
    #return False



input_str=""
def main(inp):
    board=[[" " for i in range(8)]for i in range(8)]
    curr=0
    #construct board
    for i in range(0,8):
        count=0
        while True:
            if inp[curr]=="/" or inp[curr]==" ":
                break
            else:
                cs=inp[curr]
                if str.isdigit(cs)==True:
                    curr+=1
                    count+=int(cs)
                else:
                    board[-i-1][count]=cs
                    count+=1
                    curr+=1
        curr+=1
    #figure out who to move
    board.append([])
    if inp[curr]=="w":
        to_move=1
    else:
        to_move=-1
    board[-1].append(to_move)
    curr+=2
    #castling
    if inp[curr]=="-":
        curr+=2
        for i in range(0,4):
            board[-1].append(False)
    else:
        REFERENCE=["K","Q","k","q"]
        count=0
        for i in range(0,5):
            print(board[-1])
            if inp[curr+i]==" ":
                for j in range(count,5):
                    if j!=count:
                        board[-1].append(False)
                curr+=i+1
                break
            else:
                for j in range(int(count),4):
                    count+=1
                    if inp[curr+i]==REFERENCE[j]:
                        board[-1].append(True)
                        break
                    else:
                        board[-1].append(False)

        
    
    
    #en passent
    if inp[curr]=="-":
        board[-1].append(False)
        curr+=2
    else:
        ep_square=[COLUMNS.index(inp[curr]),int(inp[curr+1])-1]
        board[-1].append(ep_square)
        curr+=3
    print(board[-1])
    #move counters
    board[-1].append(int(inp[curr]))
    curr+=2
    board[-1].append(int(inp[curr]))
    return board

#print(main("rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2"))
test=main("7k/8/3nN1KN/8/8/8/8/8 w - - 1 0")
t2=main("6k1/8/6KN/8/2n5/8/2N5/8 w - - 1 0")
#for i in range(7,-1,-1):
#    print(test[i])
#print(test[3][6])
#print(knight_move(test,4,4,1))
#print(king_move(test,1,5,1))
print(check_check(t2,7,6,-1))
s=time.time()
print(minmax(test,1,1))
e=time.time()
print(e-s)
#[99999999, [5, 4], [4, 6]]