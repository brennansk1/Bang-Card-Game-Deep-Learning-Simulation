# Bang Game Project

This project implements a simplified version of the classic **Bang!** card game, where players take turns drawing and playing cards that affect their health, attack other players, and use various actions like healing and evading damage. The game is designed to simulate a multiplayer experience, where the goal is to be the last player standing.

## Project Structure

Here’s an overview of the core files in the project:

### 1. **bang_game.py**
Contains the primary game logic, including managing the game state, turns, and determining the winner. The game logic is implemented with checks for player actions, card effects, and game-ending conditions.

### 2. **card.py**
Defines the different types of cards available in the game (e.g., `Bang!`, `Beer`, `Cat Balou`, `Panic!`). Each card has a specific effect, such as dealing damage or healing a player.

### 3. **character_data.py**
Stores character data for each player, such as their health, hand of cards, and whether they have been eliminated from the game. This helps track the state of each player.

### 4. **deck.py**
Handles the deck of cards used in the game. It defines the deck's functionality, such as drawing cards, shuffling, and replenishing cards when needed.

### 5. **distance.py**
Calculates and manages the distance between players in certain card actions (e.g., when a player performs a ranged attack with a `Bang!` card).

### 6. **enums.py**
Defines the necessary enumerations for player states and actions. This is used to define actions like `Miss`, `Bang!`, and other gameplay-related enums to simplify the game logic.

### 7. **game.py**
Manages the gameplay itself, including processing player actions, updating the game state, and ensuring the correct effects of each card are applied.

### 8. **game_logger.py**
Logs important events during the game (e.g., player actions, health changes, and eliminations). It’s useful for debugging and tracking the flow of the game.

### 9. **main.py**
Serves as the entry point for the game. It initializes the game, manages player interactions, and runs the game loop. It’s also responsible for generating actions and processing the game turns.

### 10. **player.py**
Defines the player class, including attributes like the player’s hand, health, and status (whether they are alive or eliminated). It includes methods for handling player actions and card usage.

### 11. **run_training.py**
Contains logic for training AI agents to play the game. This script simulates many games, letting the AI learn the best actions and strategies to use in different game states.

## How to Play

1. **Game Setup:**
   - Players are initialized with cards and health points.
   - Each player takes turns performing actions such as playing cards or attacking other players.
   - Players can attack, heal, and use various cards with special effects.

2. **Turn Mechanics:**
   - The game progresses in turns, with each player selecting a card to play.
   - Actions include attacking with `Bang!`, healing with `Beer`, or stealing a card with `Cat Balou`.
   - Players are eliminated when their health reaches zero.

3. **Winning the Game:**
   - The last player remaining in the game wins.
   - The game ends when only one player is left or when the maximum number of turns is reached.

4. **Card Effects:**
   - **Bang!**: Deal damage to another player.
   - **Beer**: Heal yourself by 1 health point.
   - **Cat Balou**: Discard a card from another player’s hand.
   - **Panic!**: Steal a card from another player.
   - **Indians!**: All players except the one who played this card must discard a card.
   - **Duel**: Challenge another player to a duel; both players play cards until one loses.
   - **Stagecoach**: Draw two cards from the deck.
   - **Wells Fargo**: Draw three cards from the deck.

## Installation and Usage

To run the game, follow these steps:

1. Clone or download the repository.
2. Ensure you have Python 3.x installed.
3. Install any dependencies (if provided in a `requirements.txt` file or needed for the game to run).
4. Run the game by executing:

```bash
python main.py
