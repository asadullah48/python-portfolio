from PIL import Image, ImageEnhance, ImageFilter, ImageOps, ImageDraw, ImageFont
import numpy as np
from io import BytesIO

def apply_brightness(image, factor):
    """
    ☀️ Adjust the brightness of an image.

    Args:
        image (PIL.Image): The image to modify
        factor (float): Brightness factor (0.0-2.0, 1.0 is original)

    Returns:
        PIL.Image: The modified image
    """
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(factor)

def apply_contrast(image, factor):
    """
    📊 Adjust the contrast of an image.

    Args:
        image (PIL.Image): The image to modify
        factor (float): Contrast factor (0.0-2.0, 1.0 is original)

    Returns:
        PIL.Image: The modified image
    """
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(factor)

def apply_blur(image, radius=2):
    """
    🌫️ Apply blur effect to an image.

    Args:
        image (PIL.Image): The image to modify
        radius (int, optional): Blur radius. Defaults to 2.

    Returns:
        PIL.Image: The modified image
    """
    return image.filter(ImageFilter.GaussianBlur(radius=radius))

def apply_black_and_white(image):
    """
    🔲 Convert an image to black and white.

    Args:
        image (PIL.Image): The image to modify

    Returns:
        PIL.Image: The modified image
    """
    return image.convert("L")

def apply_sharpen(image, factor=2):
    """
    ✨ Sharpen an image.

    Args:
        image (PIL.Image): The image to modify
        factor (int, optional): Sharpening intensity. Defaults to 2.

    Returns:
        PIL.Image: The modified image
    """
    for _ in range(factor):
        image = image.filter(ImageFilter.SHARPEN)
    return image

def apply_sepia(image):
    """
    🧱 Apply sepia tone to an image.

    Args:
        image (PIL.Image): The image to modify

    Returns:
        PIL.Image: The modified image
    """
    grayscale = image.convert("L")
    sepia = Image.new("RGB", grayscale.size)

    for x in range(grayscale.width):
        for y in range(grayscale.height):
            gray_pixel = grayscale.getpixel((x, y))
            r = min(int(gray_pixel * 1.07), 255)
            g = min(int(gray_pixel * 0.74), 255)
            b = int(gray_pixel * 0.43)
            sepia.putpixel((x, y), (r, g, b))

    return sepia

def apply_invert(image):
    """
    🔄 Invert the colors of an image.

    Args:
        image (PIL.Image): The image to modify

    Returns:
        PIL.Image: The modified image
    """
    if image.mode == "RGBA":
        r, g, b, a = image.split()
        r, g, b = map(lambda x: x.point(lambda i: 255 - i), (r, g, b))
        return Image.merge("RGBA", (r, g, b, a))
    return ImageOps.invert(image)

def apply_crop(image, left, top, right, bottom):
    """
    ✂️ Crop an image.

    Args:
        image (PIL.Image): The image to modify
        left (int): Left coordinate
        top (int): Top coordinate
        right (int): Right coordinate
        bottom (int): Bottom coordinate

    Returns:
        PIL.Image: The modified image
    """
    return image.crop((left, top, right, bottom))

def apply_rotate(image, degrees):
    """
    🔄 Rotate an image.

    Args:
        image (PIL.Image): The image to modify
        degrees (float): Rotation angle in degrees

    Returns:
        PIL.Image: The modified image
    """
    return image.rotate(degrees, expand=True)

def apply_saturation(image, factor):
    """
    🌈 Adjust the color saturation of an image.

    Args:
        image (PIL.Image): The image to modify
        factor (float): Saturation factor (0.0-2.0, 1.0 is original)

    Returns:
        PIL.Image: The modified image
    """
    enhancer = ImageEnhance.Color(image)
    return enhancer.enhance(factor)

def apply_edge_enhance(image):
    """
    🔍 Enhance edges in an image.

    Args:
        image (PIL.Image): The image to modify

    Returns:
        PIL.Image: The modified image
    """
    return image.filter(ImageFilter.EDGE_ENHANCE_MORE)

def apply_emboss(image):
    """
    🏔️ Apply emboss effect to an image.

    Args:
        image (PIL.Image): The image to modify

    Returns:
        PIL.Image: The modified image
    """
    return image.filter(ImageFilter.EMBOSS)

def apply_posterize(image, bits=2):
    """
    🎨 Apply posterize effect (reduce number of colors).

    Args:
        image (PIL.Image): The image to modify
        bits (int): Number of bits to keep (1-8)

    Returns:
        PIL.Image: The modified image
    """
    return ImageOps.posterize(image.convert('RGB'), bits)

def apply_solarize(image, threshold=128):
    """
    ☀️ Apply solarize effect (invert colors above threshold).

    Args:
        image (PIL.Image): The image to modify
        threshold (int): Threshold value (0-255)

    Returns:
        PIL.Image: The modified image
    """
    return ImageOps.solarize(image.convert('RGB'), threshold)

def apply_mirror(image):
    """
    🪞 Mirror the image horizontally.

    Args:
        image (PIL.Image): The image to modify

    Returns:
        PIL.Image: The modified image
    """
    return ImageOps.mirror(image)

def apply_flip(image):
    """
    ↕️ Flip the image vertically.

    Args:
        image (PIL.Image): The image to modify

    Returns:
        PIL.Image: The modified image
    """
    return ImageOps.flip(image)

def apply_resize(image, width, height):
    """
    📐 Resize an image to specified dimensions.

    Args:
        image (PIL.Image): The image to modify
        width (int): New width
        height (int): New height

    Returns:
        PIL.Image: The modified image
    """
    return image.resize((width, height), Image.LANCZOS)

def apply_text_overlay(image, text, position=(10, 10), font_size=20, color=(255, 255, 255)):
    """
    📝 Add text overlay to an image.

    Args:
        image (PIL.Image): The image to modify
        text (str): Text to add
        position (tuple): Position (x, y) to place text
        font_size (int): Font size
        color (tuple): RGB color tuple

    Returns:
        PIL.Image: The modified image
    """
    # Create a copy of the image to avoid modifying the original
    img_copy = image.copy().convert('RGBA')

    # Create a drawing context
    draw = ImageDraw.Draw(img_copy)

    # Try to use a nice font, fall back to default if not available
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()

    # Draw text with a slight shadow for better visibility
    draw.text((position[0]+2, position[1]+2), text, font=font, fill=(0, 0, 0, 128))
    draw.text(position, text, font=font, fill=color)

    return img_copy

def apply_vignette(image, amount=1.0):
    """
    🔍 Apply vignette effect (darkened corners).

    Args:
        image (PIL.Image): The image to modify
        amount (float): Intensity of the effect (0.0-1.0)

    Returns:
        PIL.Image: The modified image
    """
    # Convert to numpy array for easier manipulation
    img_array = np.array(image.convert('RGB'))

    # Get dimensions
    height, width, _ = img_array.shape

    # Create a radial gradient
    x = np.linspace(-1, 1, width)
    y = np.linspace(-1, 1, height)
    x_grid, y_grid = np.meshgrid(x, y)
    radius = np.sqrt(x_grid**2 + y_grid**2)

    # Clip radius to max of 1.0
    radius = np.clip(radius, 0.0, 1.0)

    # Create vignette mask
    mask = 1.0 - (radius * amount)
    mask = np.clip(mask, 0.0, 1.0)

    # Apply mask to each color channel
    for i in range(3):
        img_array[:, :, i] = img_array[:, :, i] * mask

    # Convert back to PIL Image
    return Image.fromarray(img_array.astype('uint8'))