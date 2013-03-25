# Program to illustrate minimax algorithm using the example of the classic Tic-Tac-Toe game.
# Author : Piyush Verma
# File : ttt.py


#class TICTACTOEGAME
#contains all the methods related to the game and
# that are used in marking the positions in the game and
# getting and settings the various states of the game. 
class TICTACTOEGAME:
    #constructor for the class
    def __init__(self):
        '''Initialize parameters - the game board, moves stack and winner'''

        self.board = [ '-' for i in range(0,9) ]
        self.lastmoves = []
        self.winner = None
    
    #function to display the contents of the board
    def displayBoard(self):
        '''Print the current game board'''
       
        print "\nCurrent board:"

        for j in range(0,9,3):
            for i in range(3):
                if self.board[j+i] == '-':
                    print "- |",
                else:
                    print "%s |" %self.board[j+i],
   
            print "\n",
    
    #calculate empty positions on the board        
    def getFreePositions(self):
        '''Get the list of available positions'''

        moves = []
        for i,v in enumerate(self.board):
            if v=='-':
                moves.append(i)
        return moves
    
    #mark an X or an O at the specified position on the board
    def markPosition(self,marker,position):
        '''Mark a position with marker X or O'''
        self.board[position] = marker
        self.lastmoves.append(position)
    
    #function to undo the last move 
    def revertLastMove(self):
        '''Reset the last move'''

        self.board[self.lastmoves.pop()] = '-'
        self.winner = None
    
    #function to check if all the squares on the board are filled
    # if yes, then game over, otherwise not.
    def isGameOver(self):
        '''Test whether game has ended'''

        win_positions = [(0,1,2), (3,4,5), (6,7,8), (0,3,6),(1,4,7),(2,5,8), (0,4,8), (2,4,6)]

        for i,j,k in win_positions:
            if self.board[i] == self.board[j] == self.board[k] and self.board[i] != '-':
                self.winner = self.board[i]
                return True

        if '-' not in self.board:
            self.winner = '-'
            return True

        return False
    
    #function to play the move by the current player.
    def playMove(self,player1,player2):
        '''Execute the game playMove with players'''

        self.p1 = player1
        self.p2 = player2
   
        for i in range(9):

            self.displayBoard()
           
            if i%2==0:
                if self.p1.type == 'H':
                    print "\t\t[HumanPlayer's Move]"
                else:
                    print "\t\t[Computer's Move]"

                self.p1.move(self)
            else:
                if self.p2.type == 'H':
                    print "\t\t[HumanPlayer's Move]"
                else:
                    print "\t\t[Computer's Move]"

                self.p2.move(self)

            if self.isGameOver():
                self.displayBoard()
                if self.winner == '-':
                    print "\nYou drew the game this time Human, but I will get you next time!"
                else:
                    if(self.winner == player1.marker):
                        print "\nYou managed to defeat me Human, you have my respect! "
                    else:
                        print "\nYou cannot win from me Human! Mwahaha!"
                return


#class for the human player
class HumanPlayer:
    '''Class for player 1 (Human)'''

#constructor for the class
    def __init__(self,marker):
        self.marker = marker
        self.type = 'H'
        
        
   #function to play the current move by the human player
    def move(self, gameinstance):

        while True:
       
            m = raw_input("Input position (0-8):")

            try:
                m = int(m)
            except:
                m = -1
       #checks if value is already filled
            if m not in gameinstance.getFreePositions():
                print "Invalid move." 
                print str(m) + " is already filled. Enter another value!"
            else:
                break
   
        gameinstance.markPosition(self.marker,m)
         
#Class defined for the computer's player
class ComputerPlayer:
    '''Class for Player2 (Computer)'''

#constructor for the class.
    def __init__(self, marker):
        self.marker = marker
        self.type = 'C'
        self.treeNodes = 0

        if self.marker == 'X':
            self.opponentmarker = 'O'
        else:
            self.opponentmarker = 'X'
            
#play the current move by the computer's player
    def move(self,gameinstance):
        alpha = None
        beta = None
        move_position,score = self.maxMove(gameinstance, alpha, beta)
        gameinstance.markPosition(self.marker,move_position)
        print ("\t\t[" + str(self.treeNodes) + " Nodes generated]")
        self.treeNodes = 0
        
#function to calculate the max move of the minimax algorithm.
    def maxMove(self, gameinstance, alpha, beta):
        ''' Find maximized move'''    
        bestscore = None
        bestmove = None
        
        for m in gameinstance.getFreePositions():
            gameinstance.markPosition(self.marker,m)
            
            if gameinstance.isGameOver():
                self.treeNodes = self.treeNodes + 1
                score = self.getScore(gameinstance)
            else:
                move_position,score = self.minMove(gameinstance, alpha, beta)
                
            gameinstance.revertLastMove()
           
            if bestscore == None or score > bestscore:
                bestscore = score
                bestmove = m
                
            if beta is not None and score >= beta:
                return beta, bestmove
            
            if alpha is not None and score > alpha:
                return alpha, bestmove
                
           
        return bestmove, bestscore
    
#function to calculate the min value of the minimax algorithm

    def minMove(self, gameinstance, alpha, beta):
        ''' Find the minimized move'''

        bestscore = None
        bestmove = None
        
        for m in gameinstance.getFreePositions():
            gameinstance.markPosition(self.opponentmarker,m)
       
            if gameinstance.isGameOver():
                self.treeNodes = self.treeNodes + 1
                score = self.getScore(gameinstance)
            else:
                move_position,score = self.maxMove(gameinstance, alpha, beta)
                
       
            gameinstance.revertLastMove()
           
            if bestscore == None or score < bestscore:
                bestscore = score
                bestmove = m
            
            if alpha is not None and score <= alpha:
                return alpha, bestmove
            
            if beta is not None and score < beta:
                return beta, bestmove

        return bestmove, bestscore
#
#returns the current score of the current player.
    def getScore(self,gameinstance):
        if gameinstance.isGameOver():
            if gameinstance.winner  == self.marker:
                return 1 # Won
            elif gameinstance.winner == self.opponentmarker:
                return -1 # Opponent won
        return 0 # Draw
       

#execute the main script on the port of entry of the code. 
if __name__ == '__main__':
    game=TICTACTOEGAME()
    isChoice = -1
    while(isChoice < 0):
         
        choice = raw_input("Choose 'X' or 'O' : ")
        if(choice == 'X' or choice == 'x'):
            player1 = HumanPlayer("X")
            player2 = ComputerPlayer("O")
            isChoice = isChoice + 1
        elif(choice == 'o' or choice == 'O'):
            player1 = HumanPlayer("O")
            player2 = ComputerPlayer("X")
            isChoice = isChoice + 1
        else:
            print "Invalid Choice! \nPlease Enter Again! \n"
        
    game.playMove( player1, player2)
