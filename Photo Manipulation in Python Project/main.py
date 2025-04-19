from image_editor import ImageEditor
import os

def main():
    """
    🖼️ Main CLI application for image editing
    """
    print("📸 Python Image Editor CLI")
    print("==========================")
    
    path = input("Enter image path: ")
    
    try:
        editor = ImageEditor(path)
        print(f"✅ Image loaded successfully!")
        
        # Display image info
        info = editor.get_image_info()
        print(f"📊 Image size: {info['size'][0]}x{info['size'][1]}")
        print(f"📊 Image format: {info['format']}")
        print(f"📊 Image mode: {info['mode']}")
        
        while True:
            print("\n🛠️ Available filters:")
            print("1. ☀️ Brightness")
            print("2. 📊 Contrast")
            print("3. 🌫️ Blur")
            print("4. 🔲 Black & White")
            print("5. ✨ Sharpen")
            print("6. 🧱 Sepia")
            print("7. 🔄 Invert Colors")
            print("8. ↩️ Undo")
            print("9. ↪️ Redo")
            print("10. 🔄 Reset to Original")
            print("11. 💾 Save Image")
            print("12. 🚪 Exit")
            
            choice = input("Choose an option: ")
            
            if choice == "1":
                factor = float(input("Enter brightness factor (0.5-2.0, 1.0 is original): "))
                if editor.apply("apply_brightness", factor):
                    print("✅ Brightness filter applied")
            elif choice == "2":
                factor = float(input("Enter contrast factor (0.5-2.0, 1.0 is original): "))
                if editor.apply("apply_contrast", factor):
                    print("✅ Contrast filter applied")
            elif choice == "3":
                radius = float(input("Enter blur radius (1-10): "))
                if editor.apply("apply_blur", radius):
                    print("✅ Blur filter applied")
            elif choice == "4":
                if editor.apply("apply_black_and_white"):
                    print("✅ Black & White filter applied")
            elif choice == "5":
                factor = int(input("Enter sharpening factor (1-5): "))
                if editor.apply("apply_sharpen", factor):
                    print("✅ Sharpen filter applied")
            elif choice == "6":
                if editor.apply("apply_sepia"):
                    print("✅ Sepia filter applied")
            elif choice == "7":
                if editor.apply("apply_invert"):
                    print("✅ Colors inverted")
            elif choice == "8":
                if editor.undo():
                    print("↩️ Undo successful")
                else:
                    print("❌ Nothing to undo")
            elif choice == "9":
                if editor.redo():
                    print("↪️ Redo successful")
                else:
                    print("❌ Nothing to redo")
            elif choice == "10":
                editor.reset()
                print("🔄 Reset to original image")
            elif choice == "11":
                save_path = input("Enter path to save image: ")
                if editor.save(save_path):
                    print(f"💾 Image saved to {save_path}")
            elif choice == "12":
                print("👋 Exiting. Thanks for using Python Image Editor!")
                break
            else:
                print("❌ Invalid choice. Try again.")
            
            show = input("Show current image? (y/n): ")
            if show.lower() == 'y':
                editor.show()
    
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()