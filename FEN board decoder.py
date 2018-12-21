COLUMNS=["a","b","c","d","e","f","g","h"]
ROWS=["1","2","3","4","5","6","7","8"]

WHITE=set(["P","K","Q","B","N","R"])
BLACK=set(["p","k","q","b","n","r"])
SCORE={"P":1,"K":0,"Q":9,"B":3,"N":3,"R":5,"p":-1,"k":0,"q":-9,"b":-3,"n":-3,"r":-5," ":0}



def get_score (board):
    ret=0
    for i in range(0,8):
        for j in range(0,8):
            ret+=SCORE[board[i][j]]
    return ret


def minmax(board,to_move,layer):
    if layer>6:
        return get_score(board)
    best=[]
    best_value=to_move*-1*1000000000000
    in_check=False
    for i in range(0,8):
        if in_check==True:
            break
        for j in range(0,8):
            if in_check==True:
                break
            if to_move==1 and board[i][j] in WHITE:
                if board[i][j]=="K" and check_check(board,i,j,to_move)==True:
                    in_check=True
                    possible=king_move(board,i,j,1)
                    if possible==[]:
                        return -1000000
                    else:
                        for k in range(0,len(possible)):
                            new_board=make_move(board,[i,j],possible[k])
                            comp_score=minmax(new_board,to_move*-1,layer+1)
                            if coomp_score[0]>best_value:
                                best_value=comp_score
                                best=possible[k]
                elif board[i][j]=="N":
                    #ADD OTHER PIECES
                    possible=knight_move(board,i,j,1)
                    for k in range(0,len(possible)):
                        new_board=make_move(board,[i,j],possible[k])
                        comp_score=minmax(new_board,to_move*-1,layer+1)
                        if coomp_score[0]>best_value:
                            best_value=comp_score
                            best=possible[k]                    
            elif to_move==-1 and board[i][j] in BLACK:
                if board[i][j]=="k" and check_check(board,i,j,to_move)==True:
                    in_check=True
                    possible=king_move(board,i,j,-1)
                    if possible==[]:
                        return 1000000
                    else:
                        for k in range(0,len(possible)):
                            new_board=make_move(board,[i,j],possible[k])
                            comp_score=minmax(new_board,to_move*-1,layer+1)
                            if coomp_score[0]>best_value:
                                best_value=comp_score[0]
                                best=possible[k]
                elif board[i][j]=="n":
                    possible=knight_move(board,i,j,-1)
                    for k in range(0,len(possible)):
                        new_board=make_move(board,[i,j],possible[k])
                        comp_score=minmax(new_board,to_move*-1,layer+1)
                        if coomp_score[0]>best_value:
                            best_value=comp_score
                            best=possible[k]
    return [best_value,best]
                        

                            


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
    
def check_check(board,startx,starty,to_move):
    for x in range(0,8):
        for y in range(0,8):
            #ADD IN OTHER PIECES LATER
            if to_move==1:
                if board[x][y] in WHITE or board[x][y]==" ":
                    continue
                if board[x][y]=="n":
                    possible=knight_move(board,x,y,-1)
                    if[startx,starty] in possible:
                        return True
                elif board[x][y]=="k":
                    possible=king_move(board,x,y,-1)
                    if[startx,starty] in possible:
                        return True                    
            else:
                if board[x][y] in BLACK or board[x][y]==" ":
                    continue
                if board[x][y]=="N":
                    possible=knight_move(board,x,y,1)
                    if[startx,starty] in possible:
                        return True
                elif board[x][y]=="K":
                    possible=king_move(board,x,y,-1)
                    if[startx,starty] in possible:
                        return True                  
    return False



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

print(main("rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2"))