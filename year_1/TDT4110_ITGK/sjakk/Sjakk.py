#initiell setup av variabler og slikt
import tkinter
root=tkinter.Tk()
root.resizable(width=False, height=False)
screenwidth=str((root.winfo_screenwidth()-1200)//2)
root.geometry('1200x970+'+screenwidth+'+20')
root.title('Sjakk')
board_background=tkinter.Canvas(root, height=970, width=1090)
board_background.create_rectangle(0,0,1090, 970, fill='#794322')
board_background.place(x=0, y=0, anchor=tkinter.NW)
side_background=tkinter.Canvas(root, height=970, width=240, bd=0)
side_background.create_rectangle(0,0,240, 970, fill='gray')
side_background.place(x=970, y=0)
piece_picture_list={}
for i in ['kw', 'kb', 'dw', 'db', 'bw', 'bb', 'lw', 'lb', 'tw', 'tb', 'sw', 'sb']:
    piece_picture_list[i]=tkinter.PhotoImage(file=i+'.png')
piece_picture_list['N']=tkinter.PhotoImage(file='n.png')
main_menu_image=tkinter.PhotoImage(file='mainmenu.png')
textBox=tkinter.Text(root, height=2, width=20)
illegalTextBox=tkinter.Text(root, height=1, width=20)
moveWhiteTextBox=tkinter.Text(root, height=30, width=10)
moveBlackTextBox=tkinter.Text(root, height=30, width=10)
initialMove=[]
finalMove=[]
en_passant=[0,0,0]
castling_w=[]
castling_b=[]
move_list=[]
text=''
fucking_global_variable_1=[]
fucking_global_variable_2=[]
move_counter=0
white_moves='Hvite trekk:'
black_moves='Svarte trekk'


default_board='TSLDKLSTBBBBBBBB                                bbbbbbbbtsldklst'
patt_board='K         k          d'+' '*43



#matrise av input-strengen
def makeBoard(board_str):
    L=[]
    for y in range(8):
        l=[]
        for x in range(8):
            if board_str[8*y+x]==' ':
                l.append(None)
            else:
                l.append(board_str[8*y+x])
        L.append(l)
    return L

def getBoardString(board):
    boardstr=''
    for x in board:
        for y in x:
            if y==None:
                boardstr+=' '
            else:
                boardstr+=y
    return boardstr
#str
def getPiece(pos):
    global board
    return board[8-pos[1]][pos[0]-1]


#boolean
def isUpper(string):
    if string==string.upper():
        return True
    return False


#liste m/ [x, y] der hver [x,y] er lovlige trekk ifht pos
def getLegalMoves(pos):
    global board
    global en_passant
    piece=getPiece(pos)
    legal_moves=[]
    kill=[]
    move=[]
    x=pos[0]
    y=pos[1]
    if piece==None:
        return legal_moves
    if piece == 'b':
        if x != 8 and y>1:
            kill.append([x + 1, y + 1])
        if x != 1 and y>1:
            kill.append([x - 1, y + 1])

        if y != 8:
            move.append([x, y + 1])
        if y == 2 and getPiece([x, 3])==None:
            move.append([x, y + 2])

        for i in kill:
            if getPiece(i)!=None:
                if isUpper(getPiece(i)):
                    legal_moves.append(i)
        for i in move:
            if getPiece(i) == None:
                legal_moves.append(i)
        return legal_moves

    if piece == 'B':
        if x < 8 and y>1:
            kill.append([x + 1, y - 1])
        if x > 1 and y>1:
            kill.append([x - 1, y - 1])

        if y != 1:
            move.append([x, y - 1])
        if y == 7 and getPiece([x, 6])==None:
            move.append([x,y-2])
        for i in kill:
            if getPiece(i)!=None:
                if not isUpper(getPiece(i)):
                    legal_moves.append(i)
        for i in move:
            if getPiece(i) == None:
                legal_moves.append(i)
        return legal_moves

    if piece in 'Kk':
        if x!=1:
            move.append([x-1, y])
        if x!=8:
            move.append([x+1, y])
        if y!=1:
            move.append([x, y-1])
        if y!=8:
            move.append([x, y+1])
        if x!=1 and y!=1:
            move.append([x-1, y-1])
        if x != 8 and y != 8:
            move.append([x + 1, y + 1])
        if x != 8 and y != 1:
            move.append([x + 1, y - 1])
        if x != 1 and y != 8:
            move.append([x - 1, y + 1])

    if piece in 'tTdD':
        if x!=1:
            i=1
            while x-i>=1:
                move.append([x-i, y])
                if getPiece([x-i, y])!=None:
                    break
                i+=1
        if x!=8:
            i=1
            while x+i<=8:
                move.append([x+i, y])
                if getPiece([x+i, y])!=None:
                    break
                i+=1
        if y!=1:
            i=1
            while y-i>=1:
                move.append([x, y-i])
                if getPiece([x, y-i])!=None:
                    break
                i+=1
        if y!=8:
            i=1
            while y+i<=8:
                move.append([x, y+i])
                if getPiece([x, y+i])!=None:
                    break
                i+=1

    if piece in 'lLdD':
        if x!=1 and y!=1:
            i=1
            while y-i>=1 and x-i>=1:
                move.append([x-i, y-i])
                if getPiece([x-i, y-i])!=None:
                    break
                i+=1
        if x!=1 and y!=8:
            i=1
            while y+i<=8 and x-i>=1:
                move.append([x-i, y+i])
                if getPiece([x-i, y+i])!=None:
                    break
                i+=1
        if x!=8 and y!=1:
            i=1
            while y-i>=1 and x+i<=8:
                move.append([x+i, y-i])
                if getPiece([x+i, y-i])!=None:
                    break
                i+=1
        if x!=8 and y!=8:
            i=1
            while y+i<=8 and x+i<=8:
                move.append([x+i, y+i])
                if getPiece([x+i, y+i])!=None:
                    break
                i+=1

    if piece in 'sS':
        x_list=[-1, 1, 2, 2, 1, -1, -2, -2]
        y_list=[2, 2, 1, -1, -2, -2, -1, 1]
        for a in range(8):
            try:
                if x+x_list[a]>=1 and x+x_list[a]<=8 and y+y_list[a]>=1 and y+y_list[a]<=8:
                    move.append([x+x_list[a], y+y_list[a]])
            except:
                continue

    for i in move:
        if getPiece(i) == None:
            legal_moves.append(i)
        elif isUpper(piece):
            if not isUpper(getPiece(i)):
                legal_moves.append(i)
        else:
            if isUpper(getPiece(i)):
                legal_moves.append(i)
    return legal_moves


#lager og displayer brettet iht input
def initialDrawBoard():
    global root
    global button_list
    global textBox
    global board
    global illegalTextBox
    global moveWhiteTextBox
    global moveBlackTextBox
    button_list=[]
    y=1
    color = ['#ffce9e', '#d18b47']
    tall=[1,2,3,4,5,6,7,8]
    for a in board:
        l=[]
        x = 1
        for b in a:
            piece = str(b)[0]
            if b!=None:
                if isUpper(b):
                    piece+='b'
                else:
                    piece+='w'
                piece=piece.lower()
            l.append(tkinter.Button(root, image=piece_picture_list[piece], bg=color[(y+x)%2]))
            l[x-1].place(x=120*(x-1)+15, y=120*(y-1)+15)
            x+=1
        button_list.append(l)
        y+=1
    button_list[0][0].configure(command=lambda: buttonCommand([8 - 0, 1]), width=100, height=100, bd=2)
    button_list[0][1].configure(command=lambda: buttonCommand([8 - 0, 2]), width=100, height=100, bd=2)
    button_list[0][2].configure(command=lambda: buttonCommand([8 - 0, 3]), width=100, height=100, bd=2)
    button_list[0][3].configure(command=lambda: buttonCommand([8 - 0, 4]), width=100, height=100, bd=2)
    button_list[0][4].configure(command=lambda: buttonCommand([8 - 0, 5]), width=100, height=100, bd=2)
    button_list[0][5].configure(command=lambda: buttonCommand([8 - 0, 6]), width=100, height=100, bd=2)
    button_list[0][6].configure(command=lambda: buttonCommand([8 - 0, 7]), width=100, height=100, bd=2)
    button_list[0][7].configure(command=lambda: buttonCommand([8 - 0, 8]), width=100, height=100, bd=2)
    button_list[1][0].configure(command=lambda: buttonCommand([8 - 1, 1]), width=100, height=100, bd=2)
    button_list[1][1].configure(command=lambda: buttonCommand([8 - 1, 2]), width=100, height=100, bd=2)
    button_list[1][2].configure(command=lambda: buttonCommand([8 - 1, 3]), width=100, height=100, bd=2)
    button_list[1][3].configure(command=lambda: buttonCommand([8 - 1, 4]), width=100, height=100, bd=2)
    button_list[1][4].configure(command=lambda: buttonCommand([8 - 1, 5]), width=100, height=100, bd=2)
    button_list[1][5].configure(command=lambda: buttonCommand([8 - 1, 6]), width=100, height=100, bd=2)
    button_list[1][6].configure(command=lambda: buttonCommand([8 - 1, 7]), width=100, height=100, bd=2)
    button_list[1][7].configure(command=lambda: buttonCommand([8 - 1, 8]), width=100, height=100, bd=2)
    button_list[2][0].configure(command=lambda: buttonCommand([8 - 2, 1]), width=100, height=100, bd=2)
    button_list[2][1].configure(command=lambda: buttonCommand([8 - 2, 2]), width=100, height=100, bd=2)
    button_list[2][2].configure(command=lambda: buttonCommand([8 - 2, 3]), width=100, height=100, bd=2)
    button_list[2][3].configure(command=lambda: buttonCommand([8 - 2, 4]), width=100, height=100, bd=2)
    button_list[2][4].configure(command=lambda: buttonCommand([8 - 2, 5]), width=100, height=100, bd=2)
    button_list[2][5].configure(command=lambda: buttonCommand([8 - 2, 6]), width=100, height=100, bd=2)
    button_list[2][6].configure(command=lambda: buttonCommand([8 - 2, 7]), width=100, height=100, bd=2)
    button_list[2][7].configure(command=lambda: buttonCommand([8 - 2, 8]), width=100, height=100, bd=2)
    button_list[3][0].configure(command=lambda: buttonCommand([8 - 3, 1]), width=100, height=100, bd=2)
    button_list[3][1].configure(command=lambda: buttonCommand([8 - 3, 2]), width=100, height=100, bd=2)
    button_list[3][2].configure(command=lambda: buttonCommand([8 - 3, 3]), width=100, height=100, bd=2)
    button_list[3][3].configure(command=lambda: buttonCommand([8 - 3, 4]), width=100, height=100, bd=2)
    button_list[3][4].configure(command=lambda: buttonCommand([8 - 3, 5]), width=100, height=100, bd=2)
    button_list[3][5].configure(command=lambda: buttonCommand([8 - 3, 6]), width=100, height=100, bd=2)
    button_list[3][6].configure(command=lambda: buttonCommand([8 - 3, 7]), width=100, height=100, bd=2)
    button_list[3][7].configure(command=lambda: buttonCommand([8 - 3, 8]), width=100, height=100, bd=2)
    button_list[4][0].configure(command=lambda: buttonCommand([8 - 4, 1]), width=100, height=100, bd=2)
    button_list[4][1].configure(command=lambda: buttonCommand([8 - 4, 2]), width=100, height=100, bd=2)
    button_list[4][2].configure(command=lambda: buttonCommand([8 - 4, 3]), width=100, height=100, bd=2)
    button_list[4][3].configure(command=lambda: buttonCommand([8 - 4, 4]), width=100, height=100, bd=2)
    button_list[4][4].configure(command=lambda: buttonCommand([8 - 4, 5]), width=100, height=100, bd=2)
    button_list[4][5].configure(command=lambda: buttonCommand([8 - 4, 6]), width=100, height=100, bd=2)
    button_list[4][6].configure(command=lambda: buttonCommand([8 - 4, 7]), width=100, height=100, bd=2)
    button_list[4][7].configure(command=lambda: buttonCommand([8 - 4, 8]), width=100, height=100, bd=2)
    button_list[5][0].configure(command=lambda: buttonCommand([8 - 5, 1]), width=100, height=100, bd=2)
    button_list[5][1].configure(command=lambda: buttonCommand([8 - 5, 2]), width=100, height=100, bd=2)
    button_list[5][2].configure(command=lambda: buttonCommand([8 - 5, 3]), width=100, height=100, bd=2)
    button_list[5][3].configure(command=lambda: buttonCommand([8 - 5, 4]), width=100, height=100, bd=2)
    button_list[5][4].configure(command=lambda: buttonCommand([8 - 5, 5]), width=100, height=100, bd=2)
    button_list[5][5].configure(command=lambda: buttonCommand([8 - 5, 6]), width=100, height=100, bd=2)
    button_list[5][6].configure(command=lambda: buttonCommand([8 - 5, 7]), width=100, height=100, bd=2)
    button_list[5][7].configure(command=lambda: buttonCommand([8 - 5, 8]), width=100, height=100, bd=2)
    button_list[6][0].configure(command=lambda: buttonCommand([8 - 6, 1]), width=100, height=100, bd=2)
    button_list[6][1].configure(command=lambda: buttonCommand([8 - 6, 2]), width=100, height=100, bd=2)
    button_list[6][2].configure(command=lambda: buttonCommand([8 - 6, 3]), width=100, height=100, bd=2)
    button_list[6][3].configure(command=lambda: buttonCommand([8 - 6, 4]), width=100, height=100, bd=2)
    button_list[6][4].configure(command=lambda: buttonCommand([8 - 6, 5]), width=100, height=100, bd=2)
    button_list[6][5].configure(command=lambda: buttonCommand([8 - 6, 6]), width=100, height=100, bd=2)
    button_list[6][6].configure(command=lambda: buttonCommand([8 - 6, 7]), width=100, height=100, bd=2)
    button_list[6][7].configure(command=lambda: buttonCommand([8 - 6, 8]), width=100, height=100, bd=2)
    button_list[7][0].configure(command=lambda: buttonCommand([8 - 7, 1]), width=100, height=100, bd=2)
    button_list[7][1].configure(command=lambda: buttonCommand([8 - 7, 2]), width=100, height=100, bd=2)
    button_list[7][2].configure(command=lambda: buttonCommand([8 - 7, 3]), width=100, height=100, bd=2)
    button_list[7][3].configure(command=lambda: buttonCommand([8 - 7, 4]), width=100, height=100, bd=2)
    button_list[7][4].configure(command=lambda: buttonCommand([8 - 7, 5]), width=100, height=100, bd=2)
    button_list[7][5].configure(command=lambda: buttonCommand([8 - 7, 6]), width=100, height=100, bd=2)
    button_list[7][6].configure(command=lambda: buttonCommand([8 - 7, 7]), width=100, height=100, bd=2)
    button_list[7][7].configure(command=lambda: buttonCommand([8 - 7, 8]), width=100, height=100, bd=2)

    tkinter.Label(root, image=main_menu_image).place(x=1085, y=130, anchor=tkinter.CENTER)
    tkinter.Button(root, command=lambda:[resetBoard(), updateBoard(), updateMoveTextBox()], text='Start på nytt').place(x=1085, y=280, anchor=tkinter.CENTER)
    textBox.place(x=1085, y=330, anchor=tkinter.CENTER)
    illegalTextBox.place(x=1085, y=380, anchor=tkinter.CENTER)
    moveWhiteTextBox.place(x=1030, y=430, anchor=tkinter.N)
    moveBlackTextBox.place(x=1140, y=430, anchor=tkinter.N)

    root.mainloop()


#endrer initialmove eller finalmove iht knappens pos
def buttonCommand(pos):
    global initialMove
    global finalMove
    global move_counter
    pos=list(reversed(pos))# orker ikke endre i hver eneste linje som lager knappene
    if initialMove==[] and getPiece(pos)!=None:
        if move_counter%2==0 and isUpper(getPiece(pos)):
            return
        elif move_counter%2==1 and not isUpper(getPiece(pos)):
            return
    if finalMove==[] and initialMove!=[]:
        finalMove=pos
        movePiece(initialMove, finalMove)
        move_counter+=1
        updateBoard()
    elif finalMove!=[]:
        finalMove=[]
        initialMove=pos
        if getPiece(initialMove)==None:
            initialMove=[]
    else:
        initialMove=pos
        if getPiece(initialMove)==None:
            initialMove=[]
    updateMoveTextBox()




#endrer brettet som displayes til inputen
def updateBoard():
    global button_list
    global board
    resetMoves()
    y=1
    color = ['#ffce9e', '#d18b47']
    for a in board:
        x = 1
        for b in a:
            piece = str(b)[0]
            if b!=None:
                if isUpper(b):
                    piece+='b'
                else:
                    piece+='w'
                piece=piece.lower()
            button_list[y-1][x-1].configure(image=piece_picture_list[piece], bg=color[(y+x)%2])
            x+=1
        y+=1



#board oppdateres ifht input-trekk
#her er forøvrig også logikken for en passant og rokkade
def movePiece(initial_pos, pos):
    global board
    global en_passant
    global castling_w
    global castling_b
    global text
    global move_list
    global move_counter
    global white_moves
    global black_moves
    move_notation=''
    if initial_pos==[] or pos==[] or getPiece(initial_pos)==None:
        return
    if getPiece(initial_pos).lower()!='b':
        move_notation=getPiece(initial_pos).lower()
    move_notation+=' abcdefgh'[initial_pos[0]]+str(initial_pos[1])+'-'
    initial_move_notation=move_notation
    if isUpper(getPiece(initial_pos)):
        color='b'
    else:
        color='w'
    if pos in getLegalMoves(initial_pos):
        if (getPiece(initial_pos)=='b' and initial_pos[1]==2 and pos[1]==4) or (getPiece(initial_pos)=='B' and initial_pos[1]==7 and pos[1]==5):
            en_passant[0]=pos[0]
            en_passant[1]=pos[1]
        if getPiece(initial_pos).lower()=='t' and initial_pos[0] in [1,8] and initial_pos[1] in [1,8]:
            if isUpper(getPiece(initial_pos)):
                castling_b.append(str(initial_pos[0]))
            elif not isUpper(getPiece(initial_pos)):
                castling_w.append(str(initial_pos[0]))
        if getPiece(initial_pos)=='k':
            if len(castling_w)!=2:
                castling_w=['1','8']
        if getPiece(initial_pos)=='K':
            if len(castling_b)!=2:
                castling_b=['1','8']
        if getPiece(pos)!=None:
            move_notation+='x'
        move_notation+=' abcdefgh'[pos[0]]+str(pos[1])
        initial_piece=getPiece(initial_pos)
        final_piece=getPiece(pos)
        board[8 - pos[1]][pos[0] - 1] = initial_piece
        board[8 - initial_pos[1]][initial_pos[0] - 1] = None
        if isCheck(getKingPos(color), color):
            text = 'Ulovlig trekk'
            board[8 - initial_pos[1]][initial_pos[0] - 1] = initial_piece
            board[8 - pos[1]][pos[0] - 1] = final_piece
            move_counter-=1
            return
        if initial_piece.lower()=='b' and (pos[1]==8 or pos[1]==1):
            pawnUpgrade(pos)
            root.wait_window(menu)
    if en_passant[0]!=0:
        if en_passant[1]==initial_pos[1] and abs(en_passant[0]-initial_pos[0])==1 and pos[0]==en_passant[0]:
            if (isUpper(getPiece(initial_pos)) and pos[1]==3) or (not isUpper(getPiece(initial_pos)) and pos[1]==6):
                board[8 - pos[1]][pos[0] - 1] = getPiece(initial_pos)
                board[8 - initial_pos[1]][initial_pos[0] - 1] = None
                board[8-en_passant[1]][en_passant[0]-1] = None
                move_notation+=' abcdefgh'[pos[0]]+str(pos[1])+'e.p.'
    elif getPiece(initial_pos)=='k':
        if pos==[3,1] and not isCheck(pos, 'w') and not isCheck([4,1], 'w') and not isCheck(initial_pos, 'w') and getPiece(pos)==None and getPiece([4,1])==None and '1' not in castling_w:
            board[8 - pos[1]][pos[0] - 1] = getPiece(initial_pos)
            board[8 - initial_pos[1]][initial_pos[0] - 1] = None
            board[8-1][1-1]=None
            board[8-1][4-1]='t'
            move_notation='0-0-0'
            pos=[4,1]
        if pos==[7,1] and not isCheck(pos, 'w') and not isCheck([6,1], 'w') and not isCheck(initial_pos, 'w') and getPiece(pos)==None and getPiece([6,1])==None and '8' not in castling_w:
            board[8 - pos[1]][pos[0] - 1] = getPiece(initial_pos)
            board[8 - initial_pos[1]][initial_pos[0] - 1] = None
            board[8-1][8-1]=None
            board[8-1][6-1]='t'
            move_notation='0-0'
            pos=[6,1]
    elif getPiece(initial_pos)=='K':
        if pos==[3,8] and not isCheck(pos, 'b') and not isCheck([4,8], 'b') and not isCheck(initial_pos, 'b') and getPiece(pos)==None and getPiece([4,8])==None and '1' not in castling_b:
            board[8 - pos[1]][pos[0] - 1] = getPiece(initial_pos)
            board[8 - initial_pos[1]][initial_pos[0] - 1] = None
            board[8-8][1-1]=None
            board[8-8][4-1]='T'
            move_notation='0-0-0'
        if pos==[7,8] and not isCheck(pos, 'b') and not isCheck([6,8], 'b') and not isCheck(initial_pos, 'b') and getPiece(pos)==None and getPiece([6,8])==None and '8' not in castling_b:
            board[8 - pos[1]][pos[0] - 1] = getPiece(initial_pos)
            board[8 - initial_pos[1]][initial_pos[0] - 1] = None
            board[8-8][8-1]=None
            board[8-8][6-1]='T'
            move_notation='0-0'
    if getPiece(pos)!=None:
        if isUpper(getPiece(pos)):
            if isCheck(getKingPos('w'), 'w'):
                move_notation += '+'
                text='Sjakk'
                if checkMate('w'):
                    text+=' matt'
                    move_notation=move_notation[:-1]+'#'
        elif not isUpper(getPiece(pos)):
            if isCheck(getKingPos('b'), 'b'):
                move_notation += '+'
                text='Sjakk'
                if checkMate('b'):
                    text+=' matt'
                    move_notation = move_notation[:-1] + '#'
    if en_passant[2]!=0:
        en_passant=[0,0,0]
    if en_passant!=[0,0,0]:
        en_passant[2]=1
    if move_notation==initial_move_notation:
        move_notation=''
        text='Ulovlig trekk'
        move_counter-=1
    else:
        move_notation+='\n'
    if pattCheck():
        text='Patt'
    if move_counter%2==0:
        white_moves+=move_notation
    elif move_counter%2==1:
        black_moves+=move_notation




#initialmove=finalmove=0
def resetMoves():
    global initialMove
    global finalMove
    initialMove=[]
    finalMove=[]


#boolean
def isCheck(pos, color):
    for a in range(1,9):
        for b in range(1,9):
            if getPiece([b, a])!=None:
                if pos in getLegalMoves([b, a]) and getPiece(pos)!=None:
                    return True
                elif getPiece(pos)==None:
                    if color=='w':
                        if isUpper(getPiece([b, a])) and pos in getLegalMoves([b,a]):
                            return True
                    if color=='b':
                        if not isUpper(getPiece([b, a])) and pos in getLegalMoves([b,a]):
                            return True
    return False


#endrer tekstboks til initialMove
def updateMoveTextBox():
    global textBox
    global board
    global text
    global illegalTextBox
    global white_moves
    global moveWhiteTextBox
    global black_moves
    global moveBlackTextBox
    textBox.delete('1.0', tkinter.END)
    illegalTextBox.delete('1.0', tkinter.END)
    illegalTextBox.insert('0.0', text)
    text=''
    moveBlackTextBox.delete('1.0',tkinter.END)
    moveWhiteTextBox.delete('1.0', tkinter.END)
    moveWhiteTextBox.insert('1.0', white_moves)
    moveBlackTextBox.insert('1.0', black_moves)
    if initialMove==[]:
        return
    piece=getPiece(initialMove)
    piece_list=['bonde', 'konge', 'dronning', 'springer', 'løper', 'tårn']
    if piece!=None:
        if isUpper(piece):
            color='sort'
        elif not isUpper(piece):
            color='hvit'
        piece=piece.lower()
        x=' abcdefgh'[initialMove[0]]
        for i in piece_list:
            if i[0]==piece:
                piece=i
                break
        tekst=f'Flytt {color} {piece} fra {x}{initialMove[1]} til...\n'
        if tekst[20]==' ':
            tekst=tekst[:20]+tekst[21:]
        textBox.insert('0.0',tekst)


def pattCheck():
    if move_counter%2==0:
        color='b'
    else:
        color='w'
    piece_list = []
    for a in range(1, 9):
        for b in range(1, 9):
            if getPiece([b, a]) != None:
                if color == 'b' and isUpper(getPiece([b, a])):
                    piece_list.append([b, a])
                if color == 'w' and not isUpper(getPiece([b, a])):
                    piece_list.append([b, a])
    positions=[]
    for a in piece_list:
        for b in getLegalMoves(a):
            if not isCheck(b,color):
                positions.append(b)
    if len(positions)==0:
        return True
    return False

#boolean, skjekk om color er satt i matt
def checkMate(color):
    global board
    global fucking_global_variable_1
    global fucking_global_variable_2
    piece_list=[]
    for a in range(1, 9):
        for b in range(1, 9):
            if getPiece([b, a]) != None:
                if color=='b' and isUpper(getPiece([b,a])):
                        piece_list.append([b,a])
                if color=='w' and not isUpper(getPiece([b,a])):
                        piece_list.append([b,a])
    for i in piece_list:
        fucking_global_variable_1=getPiece(i)
        for j in getLegalMoves(i):
            fucking_global_variable_2=getPiece(j)
            board[8 - j[1]][j[0] - 1],board[8 - i[1]][i[0] - 1] = getPiece(i), None
            if not isCheck(getKingPos(color), color):
                board[8 - i[1]][i[0] - 1], board[8 - j[1]][j[0] - 1] = fucking_global_variable_1, fucking_global_variable_2
                return False
            board[8 - i[1]][i[0] - 1], board[8 - j[1]][j[0] - 1] =  fucking_global_variable_1, fucking_global_variable_2
    return True




#[x,y]
def getKingPos(color):
    global board
    if color=='w':
        for a in range(1,9):
            for b in range(1,9):
                if getPiece([a,b])=='k':
                    return [a,b]
    elif color=='b':
        for a in range(1,9):
            for b in range(1,9):
                if getPiece([a,b])=='K':
                    return [a,b]


def pawnUpgrade(pos):
    global menu
    if isUpper(getPiece(pos)):
        color='b'
    else:
        color='w'
    menu=tkinter.Toplevel(root)
    menu.title('Hva skal bonden bli til?')
    menu.geometry('500x140+'+str((root.winfo_screenwidth()-500)//2-90)+'+'+str((root.winfo_screenheight())//2-100))
    menu.resizable(width=False, height=False)
    background=tkinter.Canvas(menu, width=500, height=140)
    background.create_rectangle(0,0,500, 140, fill='#794322')
    background.place(x=0, y=0, anchor=tkinter.NW)
    queen_butt=tkinter.Button(menu, image=piece_picture_list['d'+color], command=lambda: pawnConverter(pos, 'd'+color), height=100, width=100, bg='#ffce9e')
    bishop_butt=tkinter.Button(menu, image=piece_picture_list['l'+color], command=lambda: pawnConverter(pos, 'l'+color), height=100, width=100, bg='#d18b47')
    knight_butt=tkinter.Button(menu, image=piece_picture_list['s'+color], command=lambda: pawnConverter(pos, 's'+color), height=100, width=100, bg='#ffce9e')
    tower_butt=tkinter.Button(menu, image=piece_picture_list['t'+color], command=lambda: pawnConverter(pos, 't'+color), height=100, width=100, bg='#d18b47')
    queen_butt.place(x=20, y=20, anchor=tkinter.NW)
    bishop_butt.place(x=140, y=20, anchor=tkinter.NW)
    knight_butt.place(x=260, y=20, anchor=tkinter.NW)
    tower_butt.place(x=380, y=20, anchor=tkinter.NW)
    menu.focus_set()

def pawnConverter(pos, piece):
    global board
    global menu
    if piece[1]=='w':
        board[8-pos[1]][pos[0]-1]=piece[0]
    elif piece[1]=='b':
        board[8-pos[1]][pos[0]-1]=piece[0].upper()
    menu.destroy()



#returnerer board til utgangsposisjonen
def resetBoard():
    global board
    global en_passant
    global castling_b
    global castling_w
    global white_moves
    global black_moves
    global move_counter
    white_moves='Hvit:\n'
    black_moves='Svart:\n'
    move_counter=0
    en_passant = [0,0,0]
    castling_w = []
    castling_b = []
    board=makeBoard(default_board)
    updateMoveTextBox()


resetBoard()

initialDrawBoard()

# TODO: (i synkende rekkefølge etter viktighet)
# remis både hvis bonde ikke flyttes på 50 trekk, og hvis samme posisjon 3 ganger(lagre alle brett etter forrige brikke ble slått, dvs tell antall None i board)
# scollbar på movebox
# få noen til å playteste så finner de sikkert masse bugs
# javascript wat
