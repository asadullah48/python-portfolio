import streamlit as st
import random
import time
from minesweeper import Minesweeper

def create_game_board(game):
    # Get cell display values
    cell_values = []
    for r in range(game.size):
        row = []
        for c in range(game.size):
            if (r, c) in game.revealed:
                if (r, c) in game.bomb_positions:
                    row.append("💣")
                else:
                    bomb_count = game._count_adjacent_bombs(r, c)
                    row.append(str(bomb_count) if bomb_count > 0 else " ")
            elif (r, c) in game.flagged:
                row.append("🚩")
            else:
                row.append("□")
        cell_values.append(row)
    
    return cell_values

def main():
    st.set_page_config(page_title="Minesweeper", page_icon="💣")
    
    st.title("🎮 Minesweeper Game 🎮")
    st.markdown("### Try to clear the board without hitting any bombs!")
    
    # Game settings
    col1, col2 = st.columns(2)
    with col1:
        size = st.slider("Board Size", min_value=5, max_value=15, value=8)
    with col2:
        bomb_count = st.slider("Number of Bombs", min_value=1, max_value=size*size//3, value=size)
    
    difficulty = st.radio("Difficulty", ["Easy", "Medium", "Hard"], horizontal=True)
    if difficulty == "Easy":
        bomb_count = size  # Approximately size bombs
    elif difficulty == "Medium":
        bomb_count = size * 2  # Approximately size*2 bombs
    else:  # Hard
        bomb_count = size * 3  # Approximately size*3 bombs
    
    bomb_count = min(bomb_count, size*size-1)  # Ensure we don't fill the entire board
    
    # Initialize or reset game
    if 'game' not in st.session_state or st.button("New Game"):
        st.session_state.game = Minesweeper(size=size, bombs=bomb_count)
        st.session_state.start_time = time.time()
        st.session_state.moves = 0
    
    game = st.session_state.game
    
    # Game stats
    if game.game_over or game.won:
        elapsed_time = int(time.time() - st.session_state.start_time)
        st.markdown(f"**Time:** {elapsed_time} seconds | **Moves:** {st.session_state.moves}")
    else:
        elapsed_time = int(time.time() - st.session_state.start_time)
        st.markdown(f"**Time:** {elapsed_time} seconds | **Moves:** {st.session_state.moves} | **Bombs:** {game.bombs}")
    
    # Game board
    cell_values = create_game_board(game)
    
    # Render board using a grid of buttons
    cols = st.columns(game.size)
    
    for r in range(game.size):
        for c in range(game.size):
            cell_key = f"cell_{r}_{c}"
            
            # Handle game completion
            if game.game_over:
                if cell_values[r][c] == "💣":
                    cols[c].button("💣", key=cell_key, disabled=True, use_container_width=True)
                else:
                    cols[c].button(cell_values[r][c], key=cell_key, disabled=True, use_container_width=True)
            elif game.won:
                if (r, c) in game.bomb_positions:
                    cols[c].button("🚩", key=cell_key, disabled=True, use_container_width=True)
                else:
                    cols[c].button(cell_values[r][c], key=cell_key, disabled=True, use_container_width=True)
            else:
                # Game in progress
                if (r, c) in game.revealed:
                    cols[c].button(cell_values[r][c], key=cell_key, disabled=True, use_container_width=True)
                else:
                    # Handle cell click
                    left_click = cols[c].button(cell_values[r][c], key=cell_key, use_container_width=True)
                    
                    if left_click:
                        # Left-click behavior
                        if st.session_state.get('flag_mode', False):
                            game.toggle_flag(r, c)
                        else:
                            game.reveal(r, c)
                            st.session_state.moves += 1
                        
                        st.rerun()
        
        # Add line break between rows
        st.write("")
    
    # Controls
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Reveal Mode" if st.session_state.get('flag_mode', False) else "Flag Mode"):
            st.session_state.flag_mode = not st.session_state.get('flag_mode', False)
            st.rerun()
    
    with col2:
        mode_txt = "🚩 Flag Mode" if st.session_state.get('flag_mode', False) else "🔍 Reveal Mode"
        st.info(mode_txt)
    
    # Game over message
    if game.game_over:
        st.error("💣 BOOM! Game Over! You hit a bomb!")
    elif game.won:
        st.success("🎉 Congratulations! You cleared the board!")

if __name__ == "__main__":
    main()