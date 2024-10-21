Overview
Welcome to the Battleship Game! This game is a classic naval combat game where two players take turns guessing the locations of each other's ships on a grid. The objective is to sink all of your opponent's ships before they sink yours.

Getting Started
Requirements
Ensure you have the necessary Python environment set up with PyQt5 for the graphical interface.
Audio files (fight.mp3, click.WAV, score.mp3) and images (battle.jpg, black.png, back.jpg) should be in the same directory as the game script.
Installation
Clone this repository to your local machine.
Navigate to the project directory.
Install the required packages (if not already installed):
bash
Copy code
pip install PyQt5
Running the Game
Open a terminal and navigate to the game directory.

Run the main game script:

bash
Copy code
python game_script.py
(Replace game_script.py with the actual filename of your game script)

Once the game window opens, you'll see the following components:

Server Input: Enter the server address to connect.
Theme Selection: Choose a theme from the dropdown menu.
Game Board: A grid of buttons representing the ocean where ships are hidden.
How to Play
Connecting to the Server:

Enter the server address in the "Enter server" field and click "Connect!".
Choosing a Theme:

Select a desired theme from the dropdown menu and click "CHANGE" to apply it.
Making a Move:

Once it's your turn (indicated in the server messages), click on the buttons in the grid to make your move.
Each button corresponds to a coordinate on the board. When you click a button, it sends your move to the server.
Game Notifications:

The game will provide feedback on your moves in the server messages area, informing you if a move is valid, invalid, or if it's your opponent's turn.
When the game is over, a message will display the winner, and you will have the option to play again.
Getting Help:

If you need assistance, click the "HELP??" button, and a help dialog will provide further instructions.
Controls
Play again!: Restart the game.
Exit Game!: Exit the game application.
Close: Close the game window.
Troubleshooting
Ensure your server is running and accessible from your local machine.
If you encounter any issues, check the console for error messages and ensure all files are in the correct directories.

