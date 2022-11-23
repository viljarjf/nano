# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 14:35:43 2019

@author: Viljar Femoen
"""

#Initializes player name variables
player1='' 
player2=''


#Desc:      Prints out the board
#Input:     List of lists, all lenghts equal to 3
#Output:    None
#Comment:   Can be ignored if the players want to play blind
def printBoard(board):
    print('  - - - - - - -')
    i=3
    for x in board: #Iterates through the list of lists
        line=str(i)+' | ' #Starts with position index
        i-=1
        for y in x: #Iterates through the lists
            line+=y
            line+=' | '
        print(line)
        print('  - - - - - - -')
    print('    1   2   3') #Prints the indexes in the x-axis


#Desc:      Checks the board for wether a given player has won or not
#Input:     board: List of lists, all lenghts equal to 3
#           piece: Player to be checked, either 'X' or 'O'
#Output:    Boolean
#Comment:   piece input could be rewritten as a boolean, or as the actual player name.
def winCheck(board, piece):
    for x in board:
        if x[0]==x[1]==x[2]==piece: #Checks the three horizontal possibilities
            return True
    for x in range(3):
        if board[0][x]==board[1][x]==board[2][x]==piece: #Checks the three vertical possibilities
            return True
    if board[0][0]==board[1][1]==board[2][2]==piece: #Checks the first diagonal
             return True
    elif board[0][2]==board[1][1]==board[2][0]==piece: #Checks the second diagonal
             return True
    return False


#Desc:      One-time function to retrieve player names
#Input:     None
#Output:    None
#Comment:   Changes the global variables player1 and player2
def getPlayerNames():
    global player1
    global player2
    player1=input('Enter the name of player one: (X) ')
    player2=input('Enter the name of player two: (O) ')
    

#Desc:      Check wether a given move is legal
#Input:     pos: List of lists, all lengths equal to 2. Coordinates for the move
#           board: List of lists, all lenghts equal to 3
#Comment:   A move is legal if the cell is empty
def isLegalMove(pos, board):
    if board[pos[1]][pos[0]]==' ':
        return True
    return False


#Desc:      Check wether the attempted input is legal
#Input:     List
#Output:    Boolean
#Comment:   The only legal characters are 0, 1 and 2
def isLegalInput(string):
    for x in string:
        if x not in [1,2,0] and len(string)!=2:
            return False
    return True


#Desc:      Retrieves input from a player 
#Input:     player: str, player name, preferably player1 or player2
#           board: List of lists, all lenghts equal to 3
#Comment:   Retries untill a legal input is entered
#           Input must be on the form "x,y"
def getInput(player, board):
    inp=input('\n'+str(player)+', enter where you want your piece: ')
    inp=[int(x) for x in inp.split(',')] #The input is on the form "x,y". This line creates a list [x,y]
    inp[0]=inp[0]-1 #Reformats the x-input to 0-index
    inp[1]=3-inp[1] #Reformats the y-input to 0-index
    if isLegalInput(inp) and isLegalMove(inp, board): #Checks wether the input is legal
        return inp
    else:
        print('Please enter a legal move.')
        getInput(player, board) #Retries if the the input was illegal


#Desc:      Complete function for playing the game
#Input:     None
#Output:    None
#Comment:   Call once for each game. Terminates when a game is over. 
#           TODO: End game if board is full
def main():
    gameBoard=[[' ', ' ', ' '] for x in range(3)] #Initializes the board to be played on
    print('Checkers! First to three in a row wins!')
    print('When asked for a position, enter it on the form "x,y"')
    getPlayerNames() 
    playerList=[player1, player2]
    pieceList=['X','O']
    while True: #Loop while there are no winners
        win=0
        for x in range(2): #Iterate over both player 1 and player 2
            printBoard(gameBoard)
            inp=getInput(playerList[x], gameBoard) #Since getInput has integrated legality-check,
                                                   #this is not nessecary here
            gameBoard[inp[1]][inp[0]]=pieceList[x] #Changes the input position to the mark of the player
            if winCheck(gameBoard, pieceList[x]): 
                printBoard(gameBoard)
                print(playerList[x], 'won!')
                win=1 #Nessecary to terminate the outer loop
                break #Terminates the inner loop
        if win==1: #Terminates the outer loop
            break 

#TODO: End game if board is full
main()