# APP NAME
Flopy Blox

# GitHub Repository
The source code for this project is available on GitHub: https://github.com/mek51453/Floppy_Blox

## Identification
- Kittamet Promthanakit
- P456524
- IY499 Introduction to Programming 

## Declaration of Own Work
This project was created by Kittamet Promthanakit, I confirm that this assignment is my own work.
Where I have referred to academic sources, I have provided in-text citations and included the sources in the final reference list.

## Introduction
This game is a simple platformer where the player controls a character (referred to as "blox") who can jump and shoot to defeat monster blocks. The goal is to avoid obstacles, defeat enemies, and reach the highest possible score.

## Installation
Requirements: Before running the game, make sure you have the following installed
Python (>= 3.6)
Pygame (for the game logic and rendering)
To install Pygame, you can use the following pip command:
pip install -r

## How to Play
Objective : Try to control the character to avoid obstacles that move from right to left, without letting the character fall or collide with any obstacles.
Controls :
- Press the Spacebar or click the mouse to make the character jump or fly upwards.
- The character will float up and gradually fall due to gravity.
- Avoid falling to the ground or colliding with obstacles.
Pass Obstacles : When you see a gap between obstacles, press the jump button at the right moment to pass through.

Game Over : 
- Colliding with Obstacles: If the character collides with an obstacle moving from the right, the game will end immediately.
- Falling to the Ground: If the character falls to the ground, the game will end as well.
- Restart: Once the game is over, you can restart by pressing the Restart button or Spacebar to play again.

### Running the Game
python main_menu.py

## Game Elements
- Player Character (Blox): The main character that the player controls. It can jump and shoot using the keyboard inputs.
- Monster Blox: Enemies that the player must shoot to defeat. These enemies move across the screen. If player collide with a monster, the game ends immediately.
- Obstacles: Static or dynamic obstacles that the player must jump over. Hitting with an obstacle will end the game for the player.
- Score: Players will receive points for crossing obstacles. The score will be displayed on the game screen after the game ends.

## Libraries Used
The following libraries are used in this project:
- Pygame: For creating the game environment, handling user input, and rendering graphics.
- Unittest: For running unit tests to ensure the game functions correctly.

## Project Structure
The project consists of the following main components:
main_menu.py : Manages the game's main menu. It handles user input for the player name, displays the rank leaderboard, and shows tips.
- main_menu(): Displays the main menu and handles user input for starting the game, viewing the leaderboard, and exiting.
- load_scores(), save_scores(): Load and save player scores from the scores.json file.
- draw_button(): Helper function to draw buttons on the screen.
game.py : Contains the main game logic, including the bird’s movement, collision detection, pipe generation, shooting mechanics, and monster interactions.
- Bird: Controls the player's character, including its movement and jumping mechanics.
- Pipe: Represents obstacles the bird must navigate through.
- Monster: Represents enemies that the player can shoot at.
- Bullet: Handles bullets shot by the player.
- Game: Manages the game loop, scoring, and collision detection.
scores.json : A JSON file that stores the names and scores of players.

## Citations
CHAT GPT