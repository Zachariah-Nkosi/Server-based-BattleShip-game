import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import * 
from PyQt5.QtMultimedia import *
import os
from GameClient import *
import random

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set the window title and size
        self.setWindowTitle("Game Window")
        self.setGeometry(200,200,1800, 1000)
        self.setWindowIcon(QIcon('black.png'))

        # Set the background image
        palette = self.palette()
        brush = QBrush(QPixmap("front.jpg").scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation))
        palette.setBrush(QPalette.Background, brush)
        self.setPalette(palette)

        # Add a "Play" button
        play_button = QPushButton("Play", self)
        play_button.setGeometry(500, 800, 200, 80)
        play_button.setStyleSheet("""
            QPushButton {
                background-color: #f3c623;
                border: 2px solid #f3c623;
                border-radius: 25px;
                color: #ffffff;
                font-weight: bold;
                font-size: 18px;
                text-align: center;
                padding: 10px;
                padding-left: 20px;
                padding-right: 20px;
                padding-top: 5px;
                padding-bottom: 5px;
                text-shadow: 1px 1px 1px rgba(0,0,0,0.5);
                border-style: outset;
                border-width: 4px;
            }
            
            QPushButton:hover {
                background-color: #f7d34b;
                border: 2px solid #f7d34b;
            }
            
            QPushButton:pressed {
                background-color: #e6b800;
                border: 2px solid #e6b800;
                border-style: inset;
            }
        """)
        play_button.setCursor(QCursor(Qt.PointingHandCursor))
        play_button.clicked.connect(self.start_game)


        # Add a "exit" button
        exit_button = QPushButton("Exit", self)
        exit_button.setGeometry(1200, 800, 200, 80)
        exit_button.setStyleSheet("""
            QPushButton {
                background-color: #f3c623;
                border: 2px solid #f3c623;
                border-radius: 25px;
                color: #ffffff;
                font-weight: bold;
                font-size: 18px;
                text-align: center;
                padding: 10px;
                padding-left: 20px;
                padding-right: 20px;
                padding-top: 5px;
                padding-bottom: 5px;
                text-shadow: 1px 1px 1px rgba(0,0,0,0.5);
                border-style: outset;
                border-width: 4px;
            }
            
            QPushButton:hover {
                background-color: #f7d34b;
                border: 2px solid #f7d34b;
            }
            
            QPushButton:pressed {
                background-color: #e6b800;
                border: 2px solid #e6b800;
                border-style: inset;
            }
        """)
        exit_button.setCursor(QCursor(Qt.PointingHandCursor))
        exit_button.clicked.connect(self.close_widget)


        

 
        # Add controls to reduce sound and to mute it
        sound_slider = QSlider(Qt.Horizontal, self)
        sound_slider.setGeometry(50, 50, 200, 30)
        sound_slider.setValue(100)
        sound_slider.setMaximum(100)
        sound_slider.setMinimum(0)
        sound_slider.valueChanged.connect(self.set_sound_volume)

        mute_button = QPushButton("Mute", self)
        mute_button.setGeometry(260, 50, 100, 30)
        mute_button.clicked.connect(self.toggle_mute)

        # Add background music
        self.background_music = QMediaPlayer()
        self.background_music.setMedia(QMediaContent(QUrl.fromLocalFile("background.mp3")))
        self.background_music.play()

    def start_game(self):
        # Open a new window with the game
        self.game_window = GameInterface()
        self.game_window.show()
        self.background_music.stop()  # Stop background music
        self.close()

    def set_sound_volume(self, volume):
        self.background_music.setVolume(volume)

    def toggle_mute(self):
        if self.background_music.isMuted():
            self.background_music.setMuted(False)
        else:
            self.background_music.setMuted(True)
    
    def close_widget(self):
        reply = QMessageBox.question(self, 'Quit', 'Are you sure you want to exit?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.close()    #exits the game
    

class HelpDialog(QDialog):   # created a subclass that will display the game description
    def __init__(self):
        super().__init__()
        self.setGeometry(250,250,800,400)
        self.setWindowTitle('Game Description')   # set the window title for description window
        self.label = QLabel("<font color='white'><b>1) Enter the server (enter localhost if you are the server or enter IP address of the server if you are the client), this is to connect to the game server.</b></font>",self)  
        self.label1 = QLabel("<font color='white'><b>2) Then press the connect button.</b></font>",self)
        self.label2 = QLabel("<font color='white'><b>3) You'll be assigned a role (C or G) and five boats will be placed randomly on the board.</b></font>",self)
        self.label3 = QLabel("<font color='white'><b>4) You will alternate with your opponent to choose a position on the board to fire a shot at sinking a boat.</b></font>",self)
        self.label4 = QLabel("<font color='white'><b>5) To make a move you must press on the board then it will be displayed on the board.</b></font>",self)
        self.label5 = QLabel("<font color='white'><b>6) Continue doing this until all 5 boats are sunk and the winner is shown on the text field.</b></font>",self)
        self.label6 = QLabel("<font color='white'><b>7) When done playing you can choose to play again by pressing the play again button or press the close button to exit the game.</b></font>",self)

        
        layout = QVBoxLayout(self)    # creating a vertical layout for the text labels
        layout.addWidget(self.label) 
        layout.addWidget(self.label1)
        layout.addWidget(self.label2)
        layout.addWidget(self.label3)
        layout.addWidget(self.label4)
        layout.addWidget(self.label5)
        layout.addWidget(self.label6)

        palette = self.palette()
        brush = QBrush(QPixmap("back.jpg")) 
        palette.setBrush(QPalette.Background, brush)
        self.setPalette(palette)



class Loopthread(QThread,GameClient):
    signal = pyqtSignal(str)
    
    def __init__(self):
        QThread.__init__(self)
        GameClient.__init__(self)
    
    def connect_(self,address):
        self.connect_to_server(address)
    
    def run(self):                 
        while True:
            msg = self.receive_message()
            if len(msg):
                self.signal.emit(msg)
            else:
                break
    
    def get_input(self, move):
        self.send_message(move)
    
    def disconnect_(self):
        if self.socket_:
            self.socket_.close()
            self.socket_ = None


class GameInterface(GameClient, QWidget):
    def __init__(self):
        GameClient.__init__(self)
        QWidget.__init__(self)
        self.setGeometry(200, 200, 1000, 800)
        self.setWindowTitle("Battleship Game!")  # Window Title
        self.setWindowIcon(QIcon('battle.jpg'))
        self.button_style = "background-color: #2B2D42; color: #F5F5F5; font-size: 16px; border-radius: 10px;"
        
        palette = self.palette()
        brush = QBrush(QPixmap("black.png"))  #
        palette.setBrush(QPalette.Background, brush)
        self.setPalette(palette)

        self.background_music = QMediaPlayer()
        self.background_music.setMedia(QMediaContent(QUrl.fromLocalFile("fight.mp3")))
        self.background_music.play()





        self.thread_ = Loopthread()    # Creating an instance
        self.game_main()

        


    def game_main(self):
        game_layout = QGridLayout()

        # Server icons
        server_label = QLabel("Enter server:")
        server_label.setStyleSheet("color: #0000FF; font-size: 14px;")

        self.server_edit = QLineEdit()
        self.server_edit.setStyleSheet("border: 1px solid #0000FF; border-radius: 5px;")

        self.server_button = QPushButton("Connect!")
        self.server_button.setStyleSheet("border: 1px solid #0000FF; border-radius: 10px; \
                                    background-color: #0000FF; color: #ffffff; \
                                    font-size: 14px; padding: 6px 12px;")
        self.server_button.clicked.connect(self.connect_server)

        self.combo_box = QComboBox()
        self.combo_box.addItem("Select Theme:")
        self.combo_box.addItem("Theme 1")
        self.combo_box.addItem("Theme 2")
        self.combo_box.addItem("Theme 3")
        self.combo_box.addItem("Theme 4")
        self.combo_box.addItem("Gray Theme")
        self.combo_box.addItem("Green Theme")
        self.combo_box.addItem("Black Theme")

        
        self.combo_box.setStyleSheet("border: 1px solid #0000FF; border-radius: 5px; \
                                background-color: #ffffff; font-size: 14px; \
                                padding: 6px 12px;")

        theme_button = QPushButton("CHANGE")
        theme_button.setStyleSheet("border: 1px solid #0000FF; border-radius: 10px; \
                                    background-color: #ffffff; color: #0000FF; \
                                    font-size: 14px; padding: 6px 12px;")
        
        theme_button.clicked.connect(self.themes)

        # Adding server icons to a server Grid Layout
        server_grid = QGridLayout()
        server_grid.addWidget(server_label, 0, 0)
        server_grid.addWidget(self.server_edit, 0, 1)
        server_grid.addWidget(self.combo_box, 0, 2)
        server_grid.addWidget(self.server_button, 1, 1)
        server_grid.addWidget(theme_button, 1, 2)


        game_layout.addLayout(server_grid, 0, 0)

        self.sever_signal = QTextEdit(self)
        self.sever_signal.setReadOnly(True)
        self.sever_signal.setStyleSheet("background-image: url(black.png); background-repeat: no-repeat; background-position: center center; font-family: Arial; font-size: 12px; color: #000000; border: 7px solid #FFFFFF;")


        #role_prompt = QLabel("c", self) # a label to specify the role


        help_ = QLabel("Click the help button below if you need help.", self)
        help_.setStyleSheet("font-size: 18px; color: white;")

        help_button = QPushButton("HELP??")
        help_button.clicked.connect(self.help)
        help_button.setFixedSize(100, 25)
        help_button.setStyleSheet("border: 1px solid #0000FF; border-radius: 10px; \
                                    background-color: #5cb85c; color: white; \
                                    font-size: 14px;font-weight:bold; padding: 6px 12px;")

        button_grid = QGridLayout()
        button_grid.addWidget(help_, 0, 0)
        button_grid.addWidget(help_button, 1, 0)

        button_vert = QVBoxLayout()
        button_vert.addLayout(button_grid)
        button_vert.addWidget(self.sever_signal)


        general_label = QLabel("General:", self) # a label for the general's score
        general_label.setStyleSheet("color: white; font-weight: bold;")
        captain_label = QLabel("Captain:", self) # a label for the captain's score
        captain_label.setStyleSheet("color: white; font-weight: bold;")
        self.general_score = QLineEdit(self)
        self.general_score.setReadOnly(True)
        self.general_score.setStyleSheet("font-family: Arial; font-size: 12px; color: #000000")

        self.captain_score = QLineEdit(self)
        self.captain_score.setReadOnly(True)
        self.captain_score.setStyleSheet("font-family: Arial; font-size: 12px; color: #000000")

        results_grid = QGridLayout()
        results_grid.addWidget(general_label, 0, 0)
        results_grid.addWidget(self.general_score, 0, 1)
        results_grid.addWidget(captain_label, 1, 0)
        results_grid.addWidget(self.captain_score, 1, 1)


        server_horizontal_layout = QHBoxLayout()
        server_horizontal_layout.addLayout(button_vert)
        #server_horizontal_layout.addWidget(role_prompt)

        # Adding the results grid layout to a separate vertical layout
        # to be added to the server_horizontal_layout
        sever_results_layout = QVBoxLayout()
        sever_results_layout.addLayout(results_grid)

        # Server messages
        self.sever_box = QGroupBox("Server Messages")
        self.sever_box.setAlignment(Qt.AlignCenter)
        self.sever_box.setStyleSheet("background-image: url('back.jpg'); border: 3px solid #2B2D42; font-weight: bold;")

        self.listwidget = QListWidget()

        sv_layout = QVBoxLayout()
        sv_layout.addWidget(self.listwidget)
        self.sever_box.setLayout(sv_layout)
        

        # Adding the server messages layout to the sever_results_layout
        sever_results_layout.addWidget(self.sever_box)

        # Adding the sever_results_layout to the server_horizontal_layout
        server_horizontal_layout.addLayout(sever_results_layout)

        game_layout.addLayout(server_horizontal_layout, 1, 0)

        board_layout = QGridLayout()

        # create 36 push button widgets and add them to the grid layout
        self.push_buttons = []

        # Create a list of colors to use for the buttons
        button_colors = ['#FF5733', '#DAF7A6', '#FFC300', '#C70039', '#900C3F', '#F6CED8',
                        '#2E86C1', '#F5B7B1', '#AED6F1', '#F9E79F', '#A3E4D7', '#EBDEF0',
                        '#7DCEA0', '#A569BD', '#F0B27A', '#73C6B6', '#D7BDE2', '#85C1E9',
                        '#F1948A', '#5499C7', '#FAD7A0', '#48C9B0', '#BB8FCE', '#5DADE2',
                        '#E59866', '#2471A3', '#F5CBA7', '#76D7C4', '#D2B4DE', '#5499C7',
                        '#DC7633', '#1B4F72', '#EDBB99', '#85C1E9', '#BB8FCE', '#5499C7']

        # create 36 push button widgets and add them to the grid layout

        for row in range(6):
            for col in range(6):
                self.push_button = QPushButton()
                self.push_button.row = row  # Set the row attribute of the push button
                self.push_button.col = col  # Set the col attribute of the push button
                self.push_button.setObjectName(str(row) + "," + str(col))
                self.push_buttons.append(self.push_button)
                
                # Set the background color of each push button widget
                self.push_button.setStyleSheet(f"background-color: {button_colors[row*6+col]}; border-radius: 10px;height:30px; border: 3px solid #FFFFFF;")
                board_layout.addWidget(self.push_button, row, col)

        # create the vertical layout and add the two grid layouts to it
        vertical_layout = QVBoxLayout()
        vertical_layout.addLayout(board_layout)

        # Adding the sever_results_layout to the horizontal_layout
        vertical_layout.addLayout(sever_results_layout)

        play_again_button = QPushButton("Play again!", self)
        play_again_button.setStyleSheet("QPushButton {background-color: #5cb85c; color: #fff; border-radius: 5px; padding: 10px;}"
                                        "QPushButton:hover {background-color: #4cae4c;}")
                        
        exit_button = QPushButton("Exit Game!", self)
        exit_button.setStyleSheet("QPushButton {background-color: #d9534f; color: #fff; border-radius: 5px; padding: 10px;}"
                                "QPushButton:hover {background-color: #c9302c;}")
                        
        close_button = QPushButton("Close", self)
        close_button.setStyleSheet("QPushButton {background-color: #d9534f; color: #fff; border-radius: 5px; padding: 10px;}"
                                    "QPushButton:hover {background-color: #c9302c;}")
        close_button.clicked.connect(self.close_)  # Closes the window when the button is clicked 

        button_horizontal_layout = QHBoxLayout()
        button_horizontal_layout.addWidget(play_again_button)
        button_horizontal_layout.addWidget(exit_button)
        button_horizontal_layout.addWidget(close_button)

        vertical_layout.addLayout(button_horizontal_layout)
        game_layout.addLayout(vertical_layout, 2, 0)
        # set the layout for the window
        self.setLayout(game_layout)
    
    def check_button(self):
        sender = self.sender()
        self.row = str(sender.row)
        self.col = str(sender.col)

        move = self.row+","+self.col
        self.thread_.get_input(move)
        sender.setEnabled(False)

        self.background_music = QMediaPlayer()
        self.background_music.setMedia(QMediaContent(QUrl.fromLocalFile("sounds/click.WAV")))
        self.background_music.play()

    def help(self):
        reply1 = QMessageBox.question(self, 'Help', 'Click the Yes button to proceed.', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply1 == QMessageBox.Yes:
            
            dialog = HelpDialog()  
            dialog.exec_()   # this executes the subclass and will open the window containing the game description

    
    def play_again(self):
        '''
        Executes when the user clicks the help button and show them the possible moves in the game
        with a dialogue box containing a help image
        '''
        play_again_dialog = QDialog(self)
        play_again_dialog.setWindowTitle("WINNER")
        play_again_dialog.setStyleSheet("background-color: black")
        
        # Add background image
        palette = self.palette()
        brush = QBrush(QPixmap("images/back.jpg"))  # Changed image filename
        palette.setBrush(QPalette.Background, brush)
        self.setPalette(palette) 

        if self.winner == "G":
            label = QLabel("<b><font color='white' style='font-size: 40px; font-family: Roboto;'>The winner is the General!!</font></b>", play_again_dialog)
        
        elif self.winner == "C":
            label = QLabel("<b><font color='white' style='font-size: 40px; font-family: Roboto;'>The winner is the Captain!</font></b>", play_again_dialog)
        
        label2 = QLabel("<b><font color='red' style='font-size: 20px; font-family: Roboto;'>Click Play again on the game if you want to restart.</font></b>", play_again_dialog)
        
        close_button_ = QPushButton("Close", play_again_dialog)
        close_button_.clicked.connect(play_again_dialog.close)
        
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(close_button_)
       
        
        play_again_dialog.setLayout(layout)
        play_again_dialog.setFixedSize(500, 500) 
        play_again_dialog.exec_()

    
    def handle_message(self,msg): 
        message_received = msg.split(",") # takes the message from the sever and creates a list of values seperated with a comma  

        if message_received[0] == "new game":  # if a message from server is "new game" do the following:
            self.sever_signal.append("<b><font color='red' style='font-size: 40px; font-family: Roboto;'>A New Game is About to Begin...</font></b>")
            self.sever_signal.append("<b><font color='red' style='font-size: 40px;'>""</font></b>")
            self.sever_signal.append("<b><font color='red' style='font-size: 40px;'>Your Role is {}</font></b>".format(message_received[1]))
            
            item = QListWidgetItem("{}".format(msg))
            font = QFont("Arial", 22)
            item.setFont(font)
            color = QColor(Qt.white)
            item.setForeground(color)

            self.listwidget.addItem(item)
        
        elif message_received[0] == "your move":
            self.sever_signal.append("<b><font color='red' style='font-size: 40px;'>Its' your turn to make a move!</font></b>")
            item = QListWidgetItem("{}".format(msg))
            font = QFont("Arial", 22)
            item.setFont(font)
            color = QColor(Qt.white)
            item.setForeground(color)
            
            for button in self.push_buttons:
                button.setEnabled(True)
                button.clicked.connect(self.check_button)
  
        elif message_received[0] == "opponents move":    # If the message from the sever is "opponent's move" the game must print/indicate to the player that's the opponen't turn to play/make a move
            self.sever_signal.append("<b><font color='red' style='font-size: 40px;'>Wait for your opponent to make a move!</font></b>")
            item = QListWidgetItem("{}".format(msg))
            font = QFont("Arial", 22)
            item.setFont(font)
            color = QColor(Qt.white)
            item.setForeground(color)

            self.listwidget.addItem(item)
            for button in self.push_buttons:
                button.setEnabled(False)

        elif message_received[0] == "valid move":
            self.sever_signal.append("<b><font color='Green' style='font-size: 40px;'>That was a valid move!</font></b>")
            player_role = message_received[1]  # Getting the player role
            row_position = int(message_received[2])       # getting row position from the sever
            colomn_position = int(message_received[3])     # getting column position from the sever
            captain_results = int(message_received[4])     # getting Captain's results from the sever
            general_results = int(message_received[5])     # getting General's results from the sever
            item = QListWidgetItem("{}".format(msg))
            font = QFont("Arial", 22)
            item.setFont(font)
            color = QColor(Qt.white)
            item.setForeground(color)

            self.listwidget.addItem(item)
            self.captain_score.setText("{}".format(captain_results))
            self.general_score.setText("{}".format(general_results))

            coord = f"{row_position},{colomn_position}"
            btn = self.findChild(QPushButton,coord)
            if btn is not None:
                btn.setText(player_role)
            
                if int(self.captain_score.text()) != captain_results:
                    sound = QSoundEffect()
                    sound.setSource(QUrl.fromLocalFile("sounds/score.mp3"))
                    sound.play()

                elif int(self.general_score.text()) != general_results:
                    sound = QSoundEffect()
                    sound.setSource(QUrl.fromLocalFile("sound/score.mp3"))
                    sound.play()


            color = QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 127)

            # Set the new color for the frame and button
            self.setStyleSheet(f"QMainWindow {{border: 10px solid {color.darker(150).name()};}}")

        elif message_received[0] == "invalid move":   
            self.sever_signal.append("<b><font color='Green' style='font-size: 40px;'>That was an invalid move!</font></b>")

        elif message_received[0] == "game over": 
            self.winner = message_received[1]

            self.sever_signal.append("<b><font color='Green' style='font-size: 40px;'>The Game is over! Check the new widget who the winner is!</font></b>")
            self.sever_signal.append("<b><font color='Green' style='font-size: 40px;'>Click Play again if you want to restart the Game!</font></b>")

            item = QListWidgetItem("{}".format(msg))
            font = QFont("Arial", 22)
            item.setFont(font)
            color = QColor(255, 0, 0)
            item.setForeground(color)
            self.listwidget.addItem(item)
            
            self.play_again()
        
        elif message_received[0] == "exit":
            self.sever_signal.append("<b><font color='Green' style='font-size: 40px;'>The other player has has exited the game!</font></b>")
            self.sever_signal.append("<b><font color='Green' style='font-size: 40px;'>Press 'Play again' to restart and close to close button to finish the game! </font></b>")

            item = QListWidgetItem("{}".format(msg))
            font = QFont("Arial", 22)
            item.setFont(font)
            color = QColor(255, 0, 0)
            item.setForeground(color)

            self.listwidget.addItem(item)


    
        elif self.received_message[0] == "play again":
                self.play_again()
                ans = self.input_play_again()   # storing the answer received from the user in the variable 'ans'
                if ans == "y":   #If the answer is 'y' that means the user wants to play again
                    self.clear_board()   # clears the board
                    self.send_message(ans)   # Send the answer from the user to the sever
                    print("Starting a new game...")
                    self.display_board()       # displaying the board for a new game
                else: 
                    self.send_message(ans)    # If the user no longer wants to play we send the answer from the user/player to the sever
        
    def connect_server(self):
        try:
            server = self.server_edit.text() # Retrieve server address from line edit
            self.thread_.connect_(server)   # giving an input to "connect_to_server" that is in the "Loopthread" class
            self.server_button.setText("Connected!")   # Change the button to "connected" if connected
            self.server_button.setEnabled(False)      # Disable the button
            #self.thread_.start()  # starting the thread
            self.background_music = QMediaPlayer()
            self.background_music.setMedia(QMediaContent(QUrl.fromLocalFile("sounds/connected.mp3")))
            self.background_music.play()
            

        
            self.thread_.signal.connect(self.handle_message)    # Sending a signal from Loopthred instance to the handle_message method

        except:
            self.sever_signal.append("<b><font color='Green' style='font-size: 40px;'>Error connecting to server, Please Try again!</font></b>")
           # error = QLabel("Error connecting to server!",self)
           # error.move(50,80)
        
        self.thread_.start()
    
    def close_(self):
        reply = QMessageBox.question(self, 'Quit', 'Are you sure you want to exit?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.close()    #exits the game

    
    def themes(self):
        '''
        Changes the background of the window if executed according to the selected color in the the combobox
        '''
        if self.combo_box.currentText() == 'Theme 1':     #green background
            palette = self.palette()
            brush = QBrush(QPixmap("images/Theme1.jpg"))  # Changed image filename
            palette.setBrush(QPalette.Background, brush)
            self.setPalette(palette)

        if self.combo_box.currentText() == 'Theme 2':     #cyan background
           palette = self.palette()
           brush = QBrush(QPixmap("images/Theme2.jpg"))  # Changed image filename
           palette.setBrush(QPalette.Background, brush)
           self.setPalette(palette) 

        if self.combo_box.currentText() == 'Theme 3':     #yellow background
            palette = self.palette()
            brush = QBrush(QPixmap("sever.jpg"))  # Changed image filename
            palette.setBrush(QPalette.Background, brush)
            self.setPalette(palette)   

        if self.combo_box.currentText() == 'Theme 4':     #no coloured background
            palette = self.palette()
            brush = QBrush(QPixmap("images/black.png")) 
            palette.setBrush(QPalette.Background, brush)
            self.setPalette(palette)

        if self.combo_box.currentText() == 'Gray Theme':     #gray background
            self.setAutoFillBackground(True)
            bg_color = self.palette()
            bg_color.setColor(self.backgroundRole(), Qt.gray)
            self.setPalette(bg_color)  

        if self.combo_box.currentText() == 'Green Theme':     #black background
            self.setAutoFillBackground(True)
            bg_color = self.palette()
            bg_color.setColor(self.backgroundRole(), Qt.green)
            self.setPalette(bg_color) 

        if self.combo_box.currentText() == 'Black Theme':     #black background
            self.setAutoFillBackground(True)
            bg_color = self.palette()
            bg_color.setColor(self.backgroundRole(), Qt.black)
            self.setPalette(bg_color) 



app = QApplication(sys.argv)
game = MainWindow()
game.show()
sys.exit(app.exec_())
