# 🏓 Enhanced Multiplayer Pong Game

A real-time multiplayer implementation of the classic Pong game using Python, Pygame, and socket programming, with enhanced visuals, sound effects, and gameplay features.

![Pong Game](https://multiplayer-pong.streamlit.app/)

## ✨ Features

- 🎮 Real-time multiplayer gameplay with customizable player names and paddle colors
- 🌐 Robust client-server architecture with improved error handling
- 🏆 Advanced score tracking with animations and particle effects
- 🎨 Professional-grade graphics with smooth animations and visual effects
- 🔊 Sound effects for game events (paddle hits, wall bounces, scoring)
- 🎁 Power-up system with special abilities (speed boost, paddle size, etc.)
- 📊 Statistics tracking and achievements system
- 🖥️ Streamlit web interface for game configuration and statistics
- � Responsive design with fullscreen support
- �🔄 Automatic ball reset after scoring with visual feedback
- 🎛️ Simple and intuitive controls with customizable settings

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
