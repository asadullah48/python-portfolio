import streamlit as st
import os
import base64
import zipfile
import io
import tempfile

def main():
    st.set_page_config(
        page_title="Space Invaders Game",
        page_icon="🚀",
        layout="centered"
    )

    st.title("🚀 Space Invaders")
    st.markdown("""
    ### A classic arcade space shooter game built with Pygame
    
    This web page allows you to download and play the Space Invaders game.
    """)

    # Game description
    st.header("About the Game")
    st.markdown("""
    **Space Invaders** is a classic arcade game where you control a spaceship to defend Earth from alien invaders.

    ### Features:
    - 🎮 Simple and intuitive controls
    - 👾 Progressive difficulty with advancing levels
    - 🛡️ Power-ups (Shield, Extra Life, Rapid Fire)
    - 💥 Explosion effects and sound
    - 🏆 Score tracking and level progression
    """)

    # Instructions
    st.header("How to Play")
    st.markdown("""
    1. Use **Left/Right Arrow Keys** to move your spaceship
    2. Press **Space** to shoot
    3. Press **ESC** to pause
    4. Collect power-ups for special abilities:
       - 🔵 Blue: Shield
       - 🟢 Green: Extra Life
       - 🟡 Yellow: Rapid Fire
    """)

    # Download options
    st.header("Download Game")
    st.warning("Note: You'll need Python and Pygame installed to run this game.")

    if st.button("📥 Download Game Files"):
        # Create the download files
        zip_bytes = create_download_zip()
        
        # Create a download button for the generated ZIP file
        st.download_button(
            label="📦 Download Space Invaders Game",
            data=zip_bytes,
            file_name="space_invaders_game.zip",
            mime="application/zip",
            help="Download all the game files as a ZIP archive"
        )
        
        st.success("Game files ready for download!")
        
    # Installation instructions
    st.header("Installation Instructions")
    st.markdown("""
    1. Download and extract the ZIP file
    2. Make sure you have Python installed (3.6 or higher)
    3. Install required packages:
       ```
       pip install pygame
       ```
    4. Navigate to the extracted folder and run:
       ```
       python space_invaders.py
       ```
    """)
    
    # Screenshots
    st.header("Game Screenshots")
    st.markdown("*Game screenshots will appear here when available*")
    
    # Footer
    st.markdown("---")
    st.markdown("Developed by [Asadullah](https://github.com/asadullah48) | [GitHub Repository](https://github.com/asadullah48/space-invaders)")

def create_download_zip():
    """Create a zip file containing all the game files."""
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
        # Add the main game file
        zipf.writestr("space_invaders/space_invaders.py", get_game_code())
        
        # Add README
        zipf.writestr("space_invaders/README.md", get_readme_content())
        
        # Add LICENSE
        zipf.writestr("space_invaders/LICENSE", get_license_content())
        
        # Add requirements.txt
        zipf.writestr("space_invaders/requirements.txt", "pygame>=2.0.0\n")
        
        # Create assets folder
        zipf.writestr("space_invaders/assets/placeholder.txt", "Create your own assets or download them from the repository.")
        
        # Add placeholder files for the assets with instructions
        zipf.writestr("space_invaders/assets/README.txt", get_assets_readme())
    
    zip_buffer.seek(0)
    return zip_buffer.getvalue()

def get_game_code():
    """Return the game code as a string."""
    return """# Space Invaders Game
# Enhanced version with power-ups, levels, and more
# See GitHub repo: https://github.com/asadullah48/space-invaders

import pygame
import random
import sys
import os
import math
from typing import List, Tuple

# Initialize pygame
pygame.init()
pygame.mixer.init()  # Initialize sound mixer

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders")

# Asset handling with error checking
def load_image(path: str, size: Tuple[int, int] = None):
    try:
        img = pygame.image.load(path)
        if size:
            return pygame.transform.scale(img, size)
        return img
    except pygame.error:
        print(f"Warning: Could not load image {path}")
        # Create a placeholder surface
        surf = pygame.Surface((64, 64))
        surf.fill((255, 0, 255))  # Magenta for missing textures
        return surf

# Load assets
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')

# Images
player_img = load_image(os.path.join(ASSETS_DIR, 'player.png'), (64, 64))
enemy_img = load_image(os.path.join(ASSETS_DIR, 'enemy.png'), (64, 64))
icon = load_image(os.path.join(ASSETS_DIR, 'space_icon.png'))
pygame.display.set_icon(icon)

# Create bullet image
bullet_img = pygame.Surface((4, 20))
bullet_img.fill((255, 255, 0))

# Try to load sounds
try:
    laser_sound = pygame.mixer.Sound(os.path.join(ASSETS_DIR, 'laser.wav'))
    explosion_sound = pygame.mixer.Sound(os.path.join(ASSETS_DIR, 'explosion.wav'))
    game_over_sound = pygame.mixer.Sound(os.path.join(ASSETS_DIR, 'game_over.wav'))
    background_music = os.path.join(ASSETS_DIR, 'background.mp3')
    sound_enabled = True
except pygame.error:
    print("Warning: Sound files could not be loaded")
    sound_enabled = False

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Game states
MENU = 0
PLAYING = 1
GAME_OVER = 2

# Player Class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed = 5
        self.lives = 3
        self.shoot_cooldown = 0
        self.invulnerable = 0
        self.original_image = self.image.copy()
    
    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
        
        # Handle cooldowns
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
            
        if self.invulnerable > 0:
            self.invulnerable -= 1
            # Flashing effect when invulnerable
            if self.invulnerable % 10 < 5:
                self.image = self.original_image.copy()
                self.image.set_alpha(128)
            else:
                self.image = self.original_image.copy()
        else:
            self.image = self.original_image.copy()
    
    def shoot(self):
        if self.shoot_cooldown == 0:
            bullet = Bullet(self.rect.centerx, self.rect.top)
            bullets.add(bullet)
            self.shoot_cooldown = 15  # 15 frames cooldown
            if sound_enabled:
                laser_sound.play()
            return True
        return False
    
    def hit(self):
        if self.invulnerable <= 0:
            self.lives -= 1
            self.invulnerable = 120  # 2 seconds of invulnerability
            return True
        return False

class Enemy(pygame.sprite.Sprite):
    def __init__(self, level=1):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-150, -40)
        self.speed_x = random.choice([-1, 1]) * random.uniform(0.5, 2) * (1 + level * 0.1)
        self.speed_y = random.uniform(1, 3) * (1 + level * 0.1)
        self.health = math.ceil(level / 3)  # Enemies get stronger with level
        self.shoot_chance = 0.005 * level  # Increases with level
        
    def update(self):
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x
        
        # Bounce off the edges
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.speed_x *= -1
        
        # Reset if off screen
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            
    def try_shoot(self):
        if random.random() < self.shoot_chance:
            return EnemyBullet(self.rect.centerx, self.rect.bottom)
        return None

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -10
    
    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((4, 20))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.speed = 7
    
    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.images = []
        # Create a simple explosion animation
        for size in range(20, 0, -4):
            surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            pygame.draw.circle(surf, (255, 165, 0), (size, size), size)
            self.images.append(surf)
        
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0
    
    def update(self):
        self.counter += 1
        if self.counter >= 2:  # Update every 2 frames
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.images[self.index]
                self.rect = self.image.get_rect()
                self.rect.center = center

class Powerup(pygame.sprite.Sprite):
    SHIELD = 0
    LIFE = 1
    RAPID_FIRE = 2
    
    def __init__(self, x, y, powerup_type):
        super().__init__()
        self.type = powerup_type
        
        # Create different colors for different powerups
        colors = {
            self.SHIELD: BLUE,
            self.LIFE: GREEN,
            self.RAPID_FIRE: YELLOW
        }
        
        self.image = pygame.Surface((20, 20))
        self.image.fill(colors[powerup_type])
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 3
        
    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

class Game:
    def __init__(self):
        # Create sprite groups
        self.reset()
        
        # Fonts
        self.font_large = pygame.font.SysFont(None, 64)
        self.font_medium = pygame.font.SysFont(None, 36)
        self.font_small = pygame.font.SysFont(None, 24)
        
        # Game variables
        self.level = 1
        self.rapid_fire = 0
        
        # Start background music if available
        if sound_enabled:
            try:
                pygame.mixer.music.load(background_music)
                pygame.mixer.music.play(-1)  # Loop forever
            except pygame.error:
                print("Warning: Could not play background music")
    
    def reset(self):
        self.player = Player()
        self.player_group = pygame.sprite.Group(self.player)
        self.bullets = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.score = 0
        self.game_state = MENU
        self.level = 1
        self.rapid_fire = 0
        
        # Spawn initial enemies
        for _ in range(6):
            self.enemies.add(Enemy(self.level))
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if self.game_state == MENU and event.key == pygame.K_RETURN:
                    self.game_state = PLAYING
                
                elif self.game_state == GAME_OVER and event.key == pygame.K_RETURN:
                    self.reset()
                    self.game_state = PLAYING
                
                elif self.game_state == PLAYING:
                    if event.key == pygame.K_SPACE:
                        if self.rapid_fire > 0:
                            # Triple shot when rapid fire is active
                            self.player.shoot()
                            offset = 20
                            bullet_left = Bullet(self.player.rect.left + offset, self.player.rect.top)
                            bullet_right = Bullet(self.player.rect.right - offset, self.player.rect.top)
                            self.bullets.add(bullet_left, bullet_right)
                        else:
                            self.player.shoot()
                    
                    if event.key == pygame.K_ESCAPE:
                        self.game_state = MENU
        
        return True
    
    def update(self):
        if self.game_state == PLAYING:
            # Update player
            keys = pygame.key.get_pressed()
            self.player.update(keys)
            
            # Update bullets
            self.bullets.update()
            self.enemy_bullets.update()
            
            # Update enemies
            self.enemies.update()
            
            # Level progression
            if len(self.enemies) < 5 + self.level:
                for _ in range(2):
                    self.enemies.add(Enemy(self.level))
            
            # Enemy shooting
            for enemy in self.enemies:
                bullet = enemy.try_shoot()
                if bullet:
                    self.enemy_bullets.add(bullet)
            
            # Update powerups and effects
            self.powerups.update()
            if self.rapid_fire > 0:
                self.rapid_fire -= 1
            
            # Update explosions
            self.explosions.update()
            
            # Check collisions
            self.check_collisions()
            
            # Check game over condition
            if self.player.lives <= 0:
                self.game_state = GAME_OVER
                if sound_enabled:
                    game_over_sound.play()
    
    def check_collisions(self):
        # Player bullets hitting enemies
        for bullet in self.bullets:
            hits = pygame.sprite.spritecollide(bullet, self.enemies, False)
            for enemy in hits:
                enemy.health -= 1
                if enemy.health <= 0:
                    # Create explosion at enemy position
                    self.explosions.add(Explosion(enemy.rect.centerx, enemy.rect.centery))
                    enemy.kill()
                    
                    # Possibly drop a powerup (10% chance)
                    if random.random() < 0.1:
                        powerup_type = random.choice([Powerup.SHIELD, Powerup.LIFE, Powerup.RAPID_FIRE])
                        self.powerups.add(Powerup(enemy.rect.centerx, enemy.rect.centery, powerup_type))
                    
                    # Add score
                    self.score += 10 * self.level
                    
                    # Every 500 points, level up
                    if self.score > 0 and self.score % 500 == 0:
                        self.level += 1
                    
                    # Create a new enemy
                    self.enemies.add(Enemy(self.level))
                    
                    if sound_enabled:
                        explosion_sound.play()
                
                bullet.kill()
        
        # Enemy bullets hitting player
        hits = pygame.sprite.spritecollide(self.player, self.enemy_bullets, True)
        if hits and self.player.hit():
            self.explosions.add(Explosion(self.player.rect.centerx, self.player.rect.centery))
        
        # Enemies colliding with player
        hits = pygame.sprite.spritecollide(self.player, self.enemies, False)
        if hits and self.player.hit():
            for enemy in hits:
                enemy.kill()
                self.explosions.add(Explosion(enemy.rect.centerx, enemy.rect.centery))
                self.enemies.add(Enemy(self.level))
        
        # Player collecting powerups
        hits = pygame.sprite.spritecollide(self.player, self.powerups, True)
        for powerup in hits:
            if powerup.type == Powerup.SHIELD:
                self.player.invulnerable = 600  # 10 seconds of invulnerability
            elif powerup.type == Powerup.LIFE:
                self.player.lives = min(self.player.lives + 1, 5)  # Max 5 lives
            elif powerup.type == Powerup.RAPID_FIRE:
                self.rapid_fire = 300  # 5 seconds of rapid fire
    
    def draw(self):
        screen.fill(BLACK)
        
        if self.game_state == MENU:
            self.draw_menu()
        elif self.game_state == PLAYING:
            self.draw_game()
        elif self.game_state == GAME_OVER:
            self.draw_game_over()
        
        pygame.display.flip()
    
    def draw_menu(self):
        # Title
        title = self.font_large.render("SPACE INVADERS", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 100))
        
        # Instructions
        instruction = self.font_medium.render("Press ENTER to Start", True, WHITE)
        screen.blit(instruction, (SCREEN_WIDTH//2 - instruction.get_width()//2, 300))
        
        # Controls
        controls1 = self.font_small.render("Arrow Keys to Move", True, WHITE)
        controls2 = self.font_small.render("Space to Shoot", True, WHITE)
        controls3 = self.font_small.render("ESC to Pause", True, WHITE)
        
        screen.blit(controls1, (SCREEN_WIDTH//2 - controls1.get_width()//2, 400))
        screen.blit(controls2, (SCREEN_WIDTH//2 - controls2.get_width()//2, 430))
        screen.blit(controls3, (SCREEN_WIDTH//2 - controls3.get_width()//2, 460))
    
    def draw_game(self):
        # Draw sprites
        self.player_group.draw(screen)
        self.bullets.draw(screen)
        self.enemy_bullets.draw(screen)
        self.enemies.draw(screen)
        self.explosions.draw(screen)
        self.powerups.draw(screen)
        
        # Draw UI
        # Score
        score_text = self.font_medium.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        # Lives and level
        lives_text = self.font_medium.render(f"Lives: {self.player.lives}", True, WHITE)
        level_text = self.font_medium.render(f"Level: {self.level}", True, WHITE)
        screen.blit(lives_text, (10, 50))
        screen.blit(level_text, (SCREEN_WIDTH - level_text.get_width() - 10, 10))
        
        # Powerup indicators
        if self.player.invulnerable > 0:
            shield_text = self.font_small.render("SHIELD", True, BLUE)
            screen.blit(shield_text, (SCREEN_WIDTH - shield_text.get_width() - 10, 50))
        
        if self.rapid_fire > 0:
            rapid_text = self.font_small.render("RAPID FIRE", True, YELLOW)
            screen.blit(rapid_text, (SCREEN_WIDTH - rapid_text.get_width() - 10, 80))
    
    def draw_game_over(self):
        # Game over text
        game_over = self.font_large.render("GAME OVER", True, RED)
        screen.blit(game_over, (SCREEN_WIDTH//2 - game_over.get_width()//2, 200))
        
        # Final score
        final_score = self.font_medium.render(f"Final Score: {self.score}", True, WHITE)
        screen.blit(final_score, (SCREEN_WIDTH//2 - final_score.get_width()//2, 300))
        
        # Restart instructions
        restart = self.font_medium.render("Press ENTER to Restart", True, WHITE)
        screen.blit(restart, (SCREEN_WIDTH//2 - restart.get_width()//2, 400))

def main():
    # Main game loop
    game = Game()
    clock = pygame.time.Clock()
    running = True
    
    while running:
        # Process events
        running = game.handle_events()
        
        # Update game state
        game.update()
        
        # Draw everything
        game.draw()
        
        # Cap the frame rate
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
"""

def get_readme_content():
    """Return the README.md content as a string."""
    return """# 🚀 Space Invaders

A classic arcade space shooter game built with Pygame.

![Game Screenshot](https://github.com/asadullah48/space-invaders/raw/main/screenshots/gameplay.png)

## 📋 Features

- 🎮 Simple and intuitive controls
- 👾 Progressive difficulty with advancing levels
- 🛡️ Power-ups (Shield, Extra Life, Rapid Fire)
- 💥 Explosion effects and sound
- 🏆 Score tracking and level progression

## 🔧 Installation

1. Ensure you have Python 3.6+ installed
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the game:
   ```bash
   python space_invaders.py
   ```

## 🎮 Controls

- **Left/Right Arrow Keys**: Move spaceship
- **Space**: Shoot
- **ESC**: Pause/Menu
- **Enter**: Start game / Restart after game over

## 🚀 Power-ups

Collect power-ups to gain special abilities:
- 🔵 Blue Circle: Shield
- 🟢 Green Circle: Extra Life
- 🟡 Yellow Circle: Rapid Fire

## 🛠️ Development

This game was built with:
- Python 3.8+
- Pygame 2.0.0+

## 🔄 Future Improvements

- [ ] Add different enemy types
- [ ] Implement boss battles
- [ ] Add local high score system
- [ ] Create more power-ups
- [ ] Implement levels with unique backgrounds

## 💻 Deployment

The game can also be launched through a Streamlit web interface:

```bash
pip install streamlit
streamlit run app.py
```

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Asadullah** - [GitHub Profile](https://github.com/asadullah48)

---

Feel free to contribute to this project by submitting pull requests or opening issues!
"""

def get_license_content():
    """Return the LICENSE content as a string."""
    return """MIT License

Copyright (c) 2025 Asadullah

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""

def get_assets_readme():
    """Return the assets README content as a string."""
    return """# Game Assets

This folder should contain the following files:

1. player.png - Your spaceship image (64x64 recommended)
2. enemy.png - Enemy spaceship image (64x64 recommended)
3. space_icon.png - Game icon (32x32 recommended)
4. laser.wav - Sound effect for shooting
5. explosion.wav - Sound effect for explosions
6. game_over.wav - Sound effect for game over
7. background.mp3 - Background music

## How to get assets

You can:
1. Create your own assets
2. Download free assets from sites like OpenGameArt.org or Kenney.nl
3. Clone the full repository from GitHub: https://github.com/asadullah48/space-invaders

For placeholder testing, the game will create simple colored rectangles if assets are not found.
"""

if __name__ == "__main__":
    main()