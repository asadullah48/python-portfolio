from PIL import Image, ImageEnhance, ImageFilter

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