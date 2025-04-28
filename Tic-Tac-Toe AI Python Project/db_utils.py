import sqlite3
import pandas as pd
from datetime import datetime

def init_db():
    """Initialize the database with required tables"""
    conn = sqlite3.connect('tictactoe.db')
    c = conn.cursor()
    
    # Create game history table
    c.execute('''
    CREATE TABLE IF NOT EXISTS game_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        difficulty TEXT,
        winner TEXT,
        moves INTEGER,
        duration REAL
    )
    ''')
    
    # Create achievements table
    c.execute('''
    CREATE TABLE IF NOT EXISTS achievements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        description TEXT,
        icon TEXT
    )
    ''')
    
    # Check if achievements already exist
    c.execute('SELECT COUNT(*) FROM achievements')
    count = c.fetchone()[0]
    
    # Insert default achievements if none exist
    if count == 0:
        achievements = [
            ('First Win', 'Win your first game against the AI', '🏆'),
            ('Master Strategist', 'Win a game on Hard difficulty', '🧠'),
            ('Speed Demon', 'Win a game in less than 10 seconds', '⚡'),
            ('Hat Trick', 'Win 3 games in a row', '🎩'),
            ('Persistence', 'Play 10 games', '🔄')
        ]
        c.executemany('INSERT INTO achievements (name, description, icon) VALUES (?, ?, ?)', achievements)
    
    # Create player achievements table
    c.execute('''
    CREATE TABLE IF NOT EXISTS player_achievements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        achievement_id INTEGER,
        date_earned TEXT,
        FOREIGN KEY (achievement_id) REFERENCES achievements (id)
    )
    ''')
    
    conn.commit()
    conn.close()

def save_game(difficulty, winner, moves, duration):
    """Save a completed game to the database"""
    conn = sqlite3.connect('tictactoe.db')
    c = conn.cursor()
    
    c.execute('''
    INSERT INTO game_history (date, difficulty, winner, moves, duration)
    VALUES (?, ?, ?, ?, ?)
    ''', (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 
          difficulty, 
          winner, 
          moves, 
          duration))
    
    conn.commit()
    conn.close()

def get_game_stats():
    """Retrieve game statistics from the database"""
    conn = sqlite3.connect('tictactoe.db')
    df = pd.read_sql_query("SELECT * FROM game_history", conn)
    conn.close()
    
    if len(df) == 0:
        return None
    
    stats = {
        "total_games": len(df),
        "wins": len(df[df['winner'] == 'Player']),
        "losses": len(df[df['winner'] == 'AI']),
        "draws": len(df[df['winner'] == 'Draw']),
        "avg_moves": df['moves'].mean(),
        "avg_duration": df['duration'].mean(),
        "win_rate": len(df[df['winner'] == 'Player']) / len(df) * 100 if len(df) > 0 else 0,
        "by_difficulty": df.groupby('difficulty')['winner'].value_counts().unstack().fillna(0).to_dict()
    }
    
    return stats

def get_achievements():
    """Get all achievements with earned status"""
    conn = sqlite3.connect('tictactoe.db')
    c = conn.cursor()
    
    c.execute('''
    SELECT a.id, a.name, a.description, a.icon, 
           CASE WHEN pa.id IS NULL THEN 0 ELSE 1 END as earned,
           pa.date_earned
    FROM achievements a
    LEFT JOIN player_achievements pa ON a.id = pa.achievement_id
    ORDER BY a.id
    ''')
    
    achievements = []
    for row in c.fetchall():
        achievements.append({
            "id": row[0],
            "name": row[1],
            "description": row[2],
            "icon": row[3],
            "earned": bool(row[4]),
            "date_earned": row[5]
        })
    
    conn.close()
    return achievements

def unlock_achievement(achievement_id):
    """Unlock a specific achievement"""
    conn = sqlite3.connect('tictactoe.db')
    c = conn.cursor()
    
    # Check if already earned
    c.execute('SELECT id FROM player_achievements WHERE achievement_id = ?', (achievement_id,))
    if c.fetchone() is None:
        # Not yet earned, so add it
        c.execute('INSERT INTO player_achievements (achievement_id, date_earned) VALUES (?, ?)', 
                 (achievement_id, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        
        # Get the achievement details
        c.execute('SELECT id, name, description, icon FROM achievements WHERE id = ?', (achievement_id,))
        achievement = c.fetchone()
        
        conn.commit()
        conn.close()
        return achievement
    
    conn.close()
    return None

def check_achievements(player_won, difficulty, game_duration, win_streak, games_played):
    """Check for newly unlocked achievements based on game results"""
    new_achievements = []
    
    # First Win
    if player_won:
        achievement = unlock_achievement(1)
        if achievement:
            new_achievements.append(achievement)
    
    # Master Strategist
    if player_won and difficulty == "Hard":
        achievement = unlock_achievement(2)
        if achievement:
            new_achievements.append(achievement)
    
    # Speed Demon
    if player_won and game_duration < 10:
        achievement = unlock_achievement(3)
        if achievement:
            new_achievements.append(achievement)
    
    # Hat Trick
    if win_streak >= 3:
        achievement = unlock_achievement(4)
        if achievement:
            new_achievements.append(achievement)
    
    # Persistence
    if games_played >= 10:
        achievement = unlock_achievement(5)
        if achievement:
            new_achievements.append(achievement)
    
    return new_achievements
