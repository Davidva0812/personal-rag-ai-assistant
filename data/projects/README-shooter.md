#  🎃 Undead Shooter Halloween Game 🦇

A simple 2D arcade-style shooter game built with **Pygame**,
where your goal is to defeat waves of enemies like bats, zombies, skeletons, and more. 
The longer you survive, the faster and tougher the enemies become!

---

## 🎮 Gameplay
- **Shoot enemies** by clicking on them with your mouse.
- Survive as long as possible while increasing your score.
- If an enemy reaches the bottom of the screen, the game is over.
- Press `R` to restart the game after a game over.
- Press `E` to exit.
- Press `SPACE` in the main menu to start the game.

## 🧟 Enemy Types
| Enemy     | HP | Speed | Appears after |
|-----------|----|--------|----------------|
| Bat       | 1  | Fast   | Immediately    |
| Skeleton  | 2  | Medium | Immediately    |
| Zombie    | 3  | Slow   | Immediately    |
| Wraith    | 2  | Fast   | Score ≥ 100    |
| Jack      | 4  | Fast   | Score ≥ 200    |

Killing Jack grants **30 points**, all others give **10 points**.

## 🔊 Audio & Music

- Click the speaker icon in the top-left to mute/unmute background music.
- Music stops on game over.

## 🏆 High Score

- Your highest score is saved locally in a file named `highscore.txt`.
- If your new score exceeds the high score, it gets updated automatically.

## 🖥️ Requirements

- **Python 3.x**
- **Pygame**

## **Screenshots**
![screenshot](screenshots/menu.png)
![screenshot](screenshots/main.png)
![screenshot](screenshots/game_over.png)

## 📦 Install dependencies:

```bash
pip install pygame
```

## 🧩 Files Overview
- main.py – Main game loop and logic
- settings_and_ui.py – Constants, images, sounds, UI elements
- highscore.txt – Automatically created to store your best score

## ✨ Future improvements
- Add movement patterns or pathfinding instead of linear falling.
- Introduce a visible character with health or weapons.
- Save high scores to a server and show global rankings.
- Translate menus and texts to multiple languages.
- Add unit tests

## ⚖️ License
This project is not licensed under any open-source license.  
All rights reserved. Please do not copy, use, or distribute the code without explicit permission.

All assets used (images, fonts, audio) are either original or licensed 
under CC0 / free for commercial use.

This project is public for portfolio viewing only. No part of it may be copied or reused.





