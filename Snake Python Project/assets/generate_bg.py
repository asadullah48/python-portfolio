import numpy as np
from PIL import Image, ImageDraw
import os

def create_snake_pattern_background(width=800, height=600, save_path='assets/snake_bg.png'):
    # Create a dark background
    background = np.zeros((height, width, 3), dtype=np.uint8)
    background.fill(30)  # Dark gray background
    
    # Convert to PIL Image
    img = Image.fromarray(background)
    draw = ImageDraw.Draw(img)
    
    # Draw snake pattern (S shapes) in the background
    for x in range(0, width, 100):
        for y in range(0, height, 100):
            # Draw subtle S shapes
            points = [
                (x + 20, y + 20),
                (x + 40, y + 30),
                (x + 60, y + 70),
                (x + 80, y + 80)
            ]
            draw.line(points, fill=(50, 80, 50), width=3)
    
    # Add a vignette effect
    for i in range(20):
        alpha = int(100 * (1 - i / 20))
        draw.rectangle(
            [(i, i), (width - i, height - i)],
            outline=(0, 0, 0, alpha),
            width=1
        )
    
    # Save the image
    img.save(save_path)
    print(f"Background saved to {save_path}")

if __name__ == "__main__":
    # Ensure the assets directory exists
    os.makedirs('assets', exist_ok=True)
    create_snake_pattern_background()
