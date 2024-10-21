from GameClient import *

class BattleShipTextClient(GameClient):

    def __init__(self):
        GameClient.__init__(self)
        self.board = [x[:] for x in [[' ']*6]*6] # creates 6x6 game board
        self.role = None # role C (for captain) or G (for general)
        
    def clear_board(self):
        self.board = [x[:] for x in [[' ']*6]*6]
        
    def input_server(self):
        return input('enter server:')
     
    def input_move(self):
        return input('enter move(0-5,0-5):')
     
    def input_play_again(self):
        return input('play again(y/n):')

    def display_board(self):
       
        counter = 0    
        print("\n    0    1    2    3    4    5")    # Column positions
        print()
        for i in self.board:
            print(str(counter) + " ", end='')      # Row positions
            print(i, end='')
            print()
            counter +=1                               # Incrementing the row position
 
    def handle_message(self,msg):
    
        self.received_message = msg.split(",") # takes the message from the sever and creates a list of values seperated with a comma 

        if self.received_message[0] == "new game":
            print("A game is about to begin:",self.received_message[1])
            self.display_board()  # displays the board to the user

        
        elif self.received_message[0] == "your move":
            print("It's your turn to move!")
            move_ = self.input_move()  # get the move from the user
            self.send_message(move_)   # send the move received from the user to the sever
            
            
        elif self.received_message[0] == "opponents move":    # If the message from the sever is "opponent's move" the game must print/indicate to the player that's the opponen't turn to play/make a move
            print("Wait for your opponent to make a move!") 
            
        
        elif self.received_message[0] == "valid move":
            player_role = self.received_message[1]             # Getting the player role
            row_position = int(self.received_message[2])       # getting row position from the sever
            colomn_position = int(self.received_message[3])     # getting column position from the sever
            captain_results = int(self.received_message[4])     # getting Captain's results from the sever
            general_results = int(self.received_message[5])     # getting General's results from the sever
            print(str(player_role)+","+str(row_position)+","+str(colomn_position)+","+ str(captain_results)+","+str(general_results)) # Printing out the role, row&column position, captain & general's results
        
            self.board[row_position][colomn_position] = player_role # this updates the board
            
            self.display_board()  # THIS DISPLAYS THE UPDATED BOARD
            
         # If the sever says the move was invalid the game must indicate by printing the below
        elif self.received_message[0] == "invalid move":   
            print("That was an invalid move!")
            
            
        # If the message from sever says it's game over then the game must indicate to the user by printing the game is over and who is the winner.
        elif self.received_message[0] == "game over": 
            print("Game over!,The winner is {} ".format(self.received_message[1]))
             
        
        elif self.received_message[0] == "play again":
            ans = self.input_play_again()   # storing the answer received from the user in the variable 'ans'
            if ans == "y":   #If the answer is 'y' that means the user wants to play again
                self.clear_board()   # clears the board
                self.send_message(ans)   # Send the answer from the user to the sever
                print("Starting a new game...")
                self.display_board()       # displaying the board for a new game
            else: 
                self.send_message(ans)    # If the user no longer wants to play we send the answer from the user/player to the sever
                
                
        elif self.received_message[0] == "exit":    # if the message from the sever is exit, the game must print/indicate to the player remaining that the other player has left the game.
            print("The other player has has exited the game!")
                
       
            
    def play_loop(self):
        while True:
            msg = self.receive_message()
            if len(msg): self.handle_message(msg)
            else: break
            
def main():
    bstc = BattleShipTextClient()
    while True:
        try:
            bstc.connect_to_server(bstc.input_server())
            break
        except:
            print('Error connecting to server!')
    bstc.play_loop()
    input('Press enter to exit.')
        
main()