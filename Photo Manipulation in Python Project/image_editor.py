from PIL import Image
import os
import filters

class ImageEditor:
    """
    📸 Image Editor class for applying various filters to images.
    """
    def __init__(self, path):
        """
        Initialize the image editor with an image file.
        
        Args:
            path (str): Path to the image file
        
        Raises:
            FileNotFoundError: If the image path does not exist
            Exception: If the image cannot be opened
        """
        if not os.path.exists(path):
            raise FileNotFoundError("Image path not found. Please check the path and try again.")
        try:
            self.original = Image.open(path)
            self.edited = self.original.copy()
            self.history = [self.original.copy()]  # 🔄 Track editing history
            self.current_step = 0
        except Exception as e:
            raise Exception(f"Unable to open the image. Error: {e}")
    
    def apply(self, filter_name, *args):
        """
        Apply a filter to the current image.
        
        Args:
            filter_name (str): Name of the filter function to apply
            *args: Arguments to pass to the filter function
        
        Returns:
            bool: True if filter was applied successfully, False otherwise
        """
        if hasattr(filters, filter_name):
            func = getattr(filters, filter_name)
            try:
                self.edited = func(self.edited, *args)
                # 🔄 Add to history and trim if we've gone back in history and then made a change
                self.current_step += 1
                self.history = self.history[:self.current_step]
                self.history.append(self.edited.copy())
                return True
            except Exception as e:
                print(f"Error applying filter: {e}")
                return False
        else:
            print(f"Filter '{filter_name}' not found.")
            return False
    
    def save(self, path):
        """
        Save the edited image to a file.
        
        Args:
            path (str): Path to save the image to
        """
        try:
            self.edited.save(path)
            return True
        except Exception as e:
            print(f"Error saving image: {e}")
            return False
    
    def show(self):
        """
        Display the current edited image.
        """
        self.edited.show()
    
    def reset(self):
        """
        ↩️ Reset to the original image.
        """
        self.edited = self.original.copy()
        self.history = [self.original.copy()]
        self.current_step = 0
        return True
    
    def undo(self):
        """
        ↩️ Undo the last filter application.
        
        Returns:
            bool: True if undo was successful, False otherwise
        """
        if self.current_step > 0:
            self.current_step -= 1
            self.edited = self.history[self.current_step].copy()
            return True
        return False
    
    def redo(self):
        """
        ↪️ Redo the last undone filter application.
        
        Returns:
            bool: True if redo was successful, False otherwise
        """
        if self.current_step < len(self.history) - 1:
            self.current_step += 1
            self.edited = self.history[self.current_step].copy()
            return True
        return False
    
    def get_image_info(self):
        """
        📊 Get information about the current image.
        
        Returns:
            dict: Image information including size, format, and mode
        """
        return {
            "size": self.edited.size,
            "format": self.original.format,
            "mode": self.edited.mode
        }