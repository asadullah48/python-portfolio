import numpy as np
from PIL import Image, ImageDraw
import os

def create_snake_images(size=40, save_dir='assets'):
    # Create snake head
    head = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(head)
    
    # Draw head body
    draw.rectangle([(0, 0), (size, size)], fill=(0, 180, 0, 255), outline=(0, 100, 0, 255), width=2)
    
    # Add eyes
    eye_size = size // 5
    # Left eye
    draw.ellipse([(size//4-eye_size//2, size//3-eye_size//2), 
                  (size//4+eye_size//2, size//3+eye_size//2)], 
                 fill=(255, 255, 255, 255))
    draw.ellipse([(size//4-eye_size//4, size//3-eye_size//4), 
                  (size//4+eye_size//4, size//3+eye_size//4)], 
                 fill=(0, 0, 0, 255))
    
    # Right eye
    draw.ellipse([(3*size//4-eye_size//2, size//3-eye_size//2), 
                  (3*size//4+eye_size//2, size//3+eye_size//2)], 
                 fill=(255, 255, 255, 255))
    draw.ellipse([(3*size//4-eye_size//4, size//3-eye_size//4), 
                  (3*size//4+eye_size//4, size//3+eye_size//4)], 
                 fill=(0, 0, 0, 255))
    
    # Add tongue
    tongue_points = [
        (size//2, 2*size//3), 
        (size//2, size), 
        (size//2+size//8, size-size//8)
    ]
    draw.polygon(tongue_points, fill=(255, 50, 50, 255))
    
    # Save head
    head.save(os.path.join(save_dir, 'snake_head.png'))
    
    # Create snake body segment
    body = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(body)
    
    # Draw body
    draw.rectangle([(0, 0), (size, size)], fill=(0, 200, 0, 255), outline=(0, 120, 0, 255), width=2)
    
    # Add pattern
    pattern_size = size // 5
    for i in range(2):
        for j in range(2):
            draw.rectangle([
                (i*size//2 + size//8, j*size//2 + size//8),
                (i*size//2 + size//8 + pattern_size, j*size//2 + size//8 + pattern_size)
            ], fill=(0, 150, 0, 255))
    
    # Save body
    body.save(os.path.join(save_dir, 'snake_body.png'))
    
    print(f"Snake images saved to {save_dir}")

if __name__ == "__main__":
    # Ensure the assets directory exists
    os.makedirs('assets', exist_ok=True)
    create_snake_images()
