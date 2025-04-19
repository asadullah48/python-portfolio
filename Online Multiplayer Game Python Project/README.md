# 🏓 Multiplayer Pong Game

A real-time multiplayer implementation of the classic Pong game using Python, Pygame, and socket programming.

![Pong Game](https://user-images.githubusercontent.com/74038190/238200431-7d8f6f99-9c66-4fff-a9a6-534fb9d66d37.gif)

## ✨ Features

- 🎮 Real-time multiplayer gameplay
- 🌐 Client-server architecture
- 🏆 Score tracking
- 🎨 Smooth animations and graphics
- 🔄 Automatic ball reset after scoring
- 📱 Simple and intuitive controls

## 🚀 Getting Started

### Prerequisites

- Python 3.7+
- Pygame library

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/asadullah48/multiplayer-pong.git
   cd multiplayer-pong
   ```

2. Install required packages:
   ```
   pip install pygame
   ```

### Running the Game

1. First, start the server:
   ```
   python server.py
   ```

2. Then, launch the client (can be on the same or different machines):
   ```
   python client.py
   ```

3. For multiplayer, launch a second client on another computer or another instance on the same computer.

## 🎮 How to Play

### Controls

- **Player 1**:
  - W: Move paddle up
  - S: Move paddle down

- **Player 2**:
  - Up Arrow: Move paddle up
  - Down Arrow: Move paddle down

- **General**:
  - R: Reconnect if disconnected
  - ESC: Quit the game

## 🔧 Configuration

You can customize the game by modifying the constants at the top of each file:

- `WIDTH`, `HEIGHT`: Game window dimensions
- `FPS`: Frames per second (game speed)
- `SERVER`, `PORT`: Network configuration

## 📝 Implementation Details

This multiplayer Pong game is built with the following technologies:

- **Python**: Core programming language
- **Pygame**: Game engine for graphics and input handling
- **Socket Programming**: For network communication between clients and server
- **Threading**: To handle multiple connections and game updates simultaneously
- **JSON**: For data serialization between client and server

## 🧩 Project Structure

```
multiplayer-pong/
├── client.py       # Game client with UI and controls
├── server.py       # Game server handling game logic and state
├── README.md       # This file
└── LICENSE         # MIT License
```

## 📊 Future Improvements

- Add game menu and options
- Implement matchmaking system
- Add power-ups and special abilities
- Create different game modes
- Add sound effects and music

## 👨‍💻 Author

- **Asadullah** - [GitHub Profile](https://github.com/asadullah48)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspiration from the classic Atari Pong game
- Thanks to the Pygame community for the excellent game development library"# multiplayer-pong" 
