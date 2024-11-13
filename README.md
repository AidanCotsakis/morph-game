# Morph

**Morph** is a grid-based puzzle game developed using Pygame. The objective is to navigate and manipulate a "blob" character through various levels filled with obstacles, goals, and dynamic mechanics. 

## **Features**
- **Grid-based Puzzle Mechanics:** Move your character through a grid, overcoming obstacles and reaching designated goals.
- **Sprite-based Graphics:** Each element, from walls to characters, is managed through sprite images for smooth visuals.
- **Customizable Levels:** Levels are loaded from an external file (`levels.txt`), allowing for easy customization and expansion.
- **Keyboard and Mouse Controls:** Supports WASD/arrow keys for movement and mouse for selection and interaction.
- **Dynamic Movement and Gravity:** Realistic movement mechanics with directional checks and gravity effects.

## **Installation**

1. **Clone the repository**.

2. **Install required dependencies**:
    ```bash
    pip install pygame
    ````
3. **Run the game**:
    ```bash
    python main.py
    ```

## **How to Play**
1. Launch the game to enter fullscreen mode.
2. Use arrow keys or WASD for movement.
3. Click on parts of the blob character to rearrange and manipulate sections to solve the puzzle.
4. Reach the end zone to complete each level.

## **Level Customization**
The game reads levels from `levels.txt`, where:

- Lines starting with * separate levels.
- Each grid cell's number represents different game elements, e.g., walls, blob parts, and goals.