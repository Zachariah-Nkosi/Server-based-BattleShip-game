###########################
# DO NOT MODIFY THIS FILE #
# VERSION 2 (BUGFIX)      #
###########################

from GameServer import *
from random import *
import sys, traceback

class BattleShipGameServer(GameServer):
    
    def __init__(self):
        GameServer.__init__(self)
        self.board = None
        self.ship_hits = None
        self.current_player = None
        self.current_shape = None
        self.captain_score = None
        self.general_score = None
        self.hits = None
        self.winner = None

    def place_ships(self):
        ship_num = 0
        while ship_num < 5:
            row_start = randint(0,4)
            col_start = randint(0,4)
            if randint(0,1):
                row_end = row_start + 1
                col_end = col_start
            else:
                row_end = row_start
                col_end = col_start + 1
            if self.board[row_start][col_start] == ' ' and self.board[row_end][col_end] == ' ':
                self.board[row_start][col_start] = str(ship_num)
                self.board[row_end][col_end] = str(ship_num)
                ship_num += 1

    def is_move_valid(self,move):
        move_list = move.split(',')
        if len(move_list) == 2 and move_list[0].isdigit() and move_list[1].isdigit():
            row = int(move_list[0])
            col = int(move_list[1])
            return 0 <= row <= 5 and 0 <= col <= 5 and not self.board[row][col].isalpha()
        else: return False

    def make_move_get_score(self,move):
        move_list = move.split(',')
        row = int(move_list[0])
        col = int(move_list[1])
        if self.board[row][col] == ' ':
            self.board[row][col] = self.current_shape.lower()
            return 0
        elif self.board[row][col].isdigit():
            ship_num = int(self.board[row][col])
            self.board[row][col] = self.current_shape.upper()
            self.ship_hits[ship_num] = self.ship_hits[ship_num] + 1
            self.hits += 1
            return self.ship_hits[ship_num]

    def play_loop(self):
        while True:
            try:
                self.output('Play loop started.')
                self.accept_clients()
                while True:
                    self.board = [x[:] for x in [[' ']*6]*6]
                    self.place_ships()
                    self.ship_hits = [0,0,0,0,0]
                    self.current_player = randint(0,1)
                    self.current_shape = 'G' if randint(0,1) else 'C'
                    self.captain_score = 0
                    self.general_score = 0
                    self.hits = 0
                    self.winner = None
                    self.send_message(self.current_player,'new game,' + self.current_shape)
                    self.send_message(self.current_player ^ 1,'new game,' + ('G' if self.current_shape == 'C' else 'C'))
                    while self.hits < 10:
                        self.send_message(self.current_player,'your move')
                        self.send_message(self.current_player ^ 1,'opponents move')
                        move = self.receive_message(self.current_player)
                        if not self.is_move_valid(move):
                            self.send_message(self.current_player,'invalid move')
                        else:
                            score = self.make_move_get_score(move)
                            if self.current_shape == 'G': self.general_score += score
                            else: self.captain_score += score
                            valid_move_str = 'valid move,' + self.current_shape + ',' + move + ',' + str(self.captain_score) + ',' + str(self.general_score)
                            self.send_message(self.current_player, valid_move_str)
                            self.send_message(self.current_player ^ 1, valid_move_str)
                            self.current_player = self.current_player ^ 1
                            self.current_shape = 'G' if self.current_shape == 'C' else 'C'
                    if self.captain_score > self.general_score:
                        self.winner = 'C'
                    else:
                        self.winner = 'G'
                    self.send_message(self.current_player,'game over,' + self.winner)
                    self.send_message(self.current_player ^ 1,'game over,' + self.winner)
                    self.send_message(self.current_player,'play again')
                    self.send_message(self.current_player ^ 1,'play again')
                    play_again_current = self.receive_message(self.current_player)[0].lower()
                    play_again_opponent = self.receive_message(self.current_player ^ 1)[0].lower()
                    if play_again_current != 'y' or play_again_opponent != 'y': 
                        self.send_message(self.current_player,'exit game')
                        self.send_message(self.current_player ^ 1,'exit game')
                        self.close_clients()
                        break
            except Exception as e:
                self.output(traceback.format_exc())
                self.output('ERROR:' + str(e) + '\n\nGame Server is being restarted.\n')
            
def main():
    bgs = BattleShipGameServer()
    bgs.play_loop()

main()