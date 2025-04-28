import numpy as np
from PIL import Image, ImageDraw
import os

def create_food_images(size=40, save_dir='assets'):
    # Create regular food (apple)
    apple = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(apple)
    
    # Draw apple body
    draw.ellipse([(5, 5), (size-5, size-5)], fill=(220, 30, 30, 255))
    
    # Add highlight
    draw.ellipse([(size//3, size//3), (size//2, size//2)], fill=(255, 255, 255, 100))
    
    # Add stem
    draw.rectangle([(size//2-2, 0), (size//2+2, 7)], fill=(101, 67, 33, 255))
    
    # Add leaf
    leaf_points = [(size//2+2, 5), (size//2+10, 0), (size//2+5, 10)]
    draw.polygon(leaf_points, fill=(50, 180, 50, 255))
    
    # Save apple
    apple.save(os.path.join(save_dir, 'food_regular.png'))
    
    # Create special food (golden apple)
    golden_apple = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(golden_apple)
    
    # Draw golden apple body
    draw.ellipse([(5, 5), (size-5, size-5)], fill=(255, 215, 0, 255))
    
    # Add highlight
    draw.ellipse([(size//3, size//3), (size//2, size//2)], fill=(255, 255, 255, 150))
    
    # Add stem
    draw.rectangle([(size//2-2, 0), (size//2+2, 7)], fill=(101, 67, 33, 255))
    
    # Add leaf
    draw.polygon(leaf_points, fill=(50, 180, 50, 255))
    
    # Add sparkle effect
    sparkle_points = [
        (size//4, size//4), (3*size//4, size//4), 
        (size//4, 3*size//4), (3*size//4, 3*size//4),
        (size//2, size//8), (size//2, 7*size//8),
        (size//8, size//2), (7*size//8, size//2)
    ]
    
    for point in sparkle_points:
        draw.ellipse([(point[0]-1, point[1]-1), (point[0]+1, point[1]+1)], fill=(255, 255, 255, 200))
    
    # Save golden apple
    golden_apple.save(os.path.join(save_dir, 'food_special.png'))
    
    print(f"Food images saved to {save_dir}")

if __name__ == "__main__":
    # Ensure the assets directory exists
    os.makedirs('assets', exist_ok=True)
    create_food_images()
