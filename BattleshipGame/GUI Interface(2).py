import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from GameClient import *

class Loopthread(QThread,GameClient):  #inheriting Gameclient and QThred
    signal = pyqtSignal(str)          # Creating a signal
    
    def __init__(self):                # Calling the QThread and Gameclient constructor
        QThread.__init__(self)
        GameClient.__init__(self)
    
    def connect_(self,address):              # This one is responsible of connecting to the server using the "connect_to_server" method from gameclient
        self.connect_to_server(address)
    
    def run(self):                 
        while True:
            msg = self.receive_message()
            if len(msg):            # Checking is the message from the server is not an empty string and emiting a signal if it's not
                self.signal.emit(msg)   # emiting a signal
            
            else:
                break     # If the message from server is an empty string it breaks
              

class GameInterface(QWidget,GameClient):
    def __init__(self):
        GameClient.__init__(self)
        QWidget.__init__(self)
        self.setGeometry(200,200,700,340)
        self.setWindowTitle("Batleship Game!") # Set window title
        self.setStyleSheet("background-color: #f2f2f2;") # Set background color
        self.gameboard()
        self.messages_from_sever()
        self.buttons_and_labels()
        self.button_style = "background-color: #2B2D42; color: #F5F5F5; font-size: 16px; border-radius: 10px;"
        
        self.thread_ = Loopthread()    # Creating an instance
        
        
    def gameboard(self):
        #hori = 50
        #vert = 130
        colors = ['#ffffff', '#f0f0f0']  # two colors to alternate
        
    
        for i in range(6):      # Create 6 rows
            for x in range(6):    # Create 6 columns
                edit = QLineEdit(self)
                edit.setMaximumWidth(55)   # Set the maximum width of the blocks
               # edit.move(hori, vert)      # Move the edit line horizontally and vertically
                #edit.setReadOnly(True)
                edit.setStyleSheet("background-color: {};".format(colors[x % 2]))  # Set edit box color
                #hori += 50
                
            #vert += 20
            #hori = 50 
            
    def messages_from_sever(self):            
        self.chat_box = QTextEdit(self)        # Create a text field for the messages from the server
        self.chat_box.setGeometry(380, 130, 300, 125)
        self.chat_box.setReadOnly(True)
        self.chat_box.setStyleSheet("background-color: #ffffff; font-family: Arial; font-size: 12px; color: #000000")
        self.chat_box.append("<b><font color='red'>Messages from the server:</font></b>")  # Set title for text field    
        
    def buttons_and_labels(self):
        self.server_label = QLabel("Enter server:",self)
        self.server_label.move(50,20)
        self.server_label.setStyleSheet("color: #0000FF; font-size: 14px;") # Set label color and font size
        self.server_edit = QLineEdit(self)   # a line edit to enter the server
        self.server_edit.setGeometry(130,20,85,18)
        
        self.server_button = QPushButton("Connect!",self) # Create a button to connect
        self.server_button.setStyleSheet("border-radius: 10px; background-color: #0000FF; color: #ffffff;") # Set button color and text color        
        self.server_button.setGeometry(130,40,85,22)
        
        self.server_button.clicked.connect(self.connect_server) # Connect button to method
        
        self.message = QLabel("                                       ",self)
        self.message.move(50,90)
        
        
        self.role_prompt = QLabel("                             ",self) # a label to specify the role
        self.role_prompt.move(50,110)
        self.role_prompt.setStyleSheet("color: #000000; font-size: 14px; font-weight: bold;") # Set label color, font size and font weight
        self.role_label = QLabel("            ",self) # a label to specify the role
        self.role_label.move(150,106)
        self.role_label.setStyleSheet("color: red; font-size: 20px;font-weight: bold;") # Set label color and font size
        
        self.score = QLabel("               ",self)  # a label for the scores
        self.score.setStyleSheet("color: #000000; font-size: 18px; font-weight: bold;")
        self.score.move(430,90)
        
        
        self.general = QLabel("                 ",self) # a label for the general's score
        self.general.move(510,80)
        self.general_score = QLabel("     ",self)
        self.general_score.move(580,80)    
        
        self.captain = QLabel("                         ",self)  # a label for the captain's score 
        self.captain.move(510,110)
        self.captain_score = QLabel("     ",self)
        self.captain_score.move(580,110)        
        
        self.play_again_button = QPushButton("Play again!",self)  # Create a button to play again
        self.play_again_button.setGeometry(50,280,85,24)
        self.play_again_button.setStyleSheet("border-radius: 10px; background-color: #008000; color: #ffffff;") # Set button color and text color
              
        
        self.exit_button = QPushButton("Exit Game!",self) # Create a button to exit the game
        self.exit_button.setGeometry(160,280,85,24)
        self.exit_button.setStyleSheet("border-radius:10px; background-color: #FF0000; color: #ffffff;") # Set button color and text color
        
        close = QPushButton("Close",self)  # Create a button to close the window
        close.setGeometry(400,280,85,24)
        close.setStyleSheet("border-radius: 10px; background-color: #FF0000; color: #ffffff;") 
        close.clicked.connect(self.close_)  # Closes the window when the button is clicked 
    
    def handle_message(self,msg): 
        self.received_message = msg.split(",") # takes the message from the sever and creates a list of values seperated with a comma    
        
        self.chat_box.append("\n" + msg)

        if self.received_message[0] == "new game":  # if a message from server is "new game" do the following:
            self.message.setText("A game is about to begin:")  # set a self.message varial to the text indicated
            self.sever_signal.append("<b><font color='red'>A new game is about to begin:</font></b>")  # Set title for text field    

            self.role_prompt.setText("YOUR ROLE:")   # set a self.role_prompt variable to the text indicated
            self.role_label.setText(self.received_message[1])   # getting a role from the server
            self.general_score.setText("0")
            self.captain_score.setText("0")
            self.score.setText("SCORE:")  # set a label for the scores        
            self.general.setText("General: ") # set a label for the general's score
            self.captain.setText("Captain:")  # set a label for the captain's score 
            
            
        
    def connect_server(self):
        try:
            server = self.server_edit.text() # Retrieve server address from line edit
            self.thread_.connect_(server)   # giving an input to "connect_to_server" that is in the "Loopthread" class
            self.server_button.setText("Connected!")   # Change the button to "connected" if connected
            self.server_button.setEnabled(False)      # Disable the button
            self.thread_.start()  # starting the thread
            self.thread_.signal.connect(self.handle_message)    # Sending a signal from Loopthred instance to the handle_message method

        except:
            error = QLabel("Error connecting to server!",self)
            error.move(50,80)
        
        self.thread_.start()
        
    def close_(self):  
        
       #Executes if the exit button is clicked and asks the user if they really want to exit the game 
       
        reply = QMessageBox.question(self, 'Quit', 'Are you sure you want to exit?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.close()    #exits the game 
            
    def colors(self):
        '''
        Changes the background of the window if executed according to the selected color in the the combobox
        '''
        if self.col_combo.currentText() == 'Green':     #green background
            self.setAutoFillBackground(True)
            bg_color = self.palette()
            bg_color.setColor(self.backgroundRole(), Qt.green)
            self.setPalette(bg_color) 
        if self.col_combo.currentText() == 'Cyan':     #cyan background
            self.setAutoFillBackground(True)
            bg_color = self.palette()
            bg_color.setColor(self.backgroundRole(), Qt.cyan)
            self.setPalette(bg_color)    
        if self.col_combo.currentText() == 'Yellow':     #yellow background
            self.setAutoFillBackground(True)
            bg_color = self.palette()
            bg_color.setColor(self.backgroundRole(), Qt.yellow)
            self.setPalette(bg_color)    
        if self.col_combo.currentText() == 'White':     #no coloured background
            self.setAutoFillBackground(True)
            bg_color = self.palette()
            bg_color.setColor(self.backgroundRole(), Qt.white)
            self.setPalette(bg_color)    
            
        if self.col_combo.currentText() == 'Gray':     #gray background
            self.setAutoFillBackground(True)
            bg_color = self.palette()
            bg_color.setColor(self.backgroundRole(), Qt.gray)
            self.setPalette(bg_color)    
        
        
    
   
        
        
             
app = QApplication(sys.argv)
game = GameInterface()
game.show()
sys.exit(app.exec_())