# 📸 Python Image Editor

![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-brightgreen)

A powerful yet simple image editing application that allows you to apply various filters and transformations to your images. Available as both a command-line interface and a web-based application powered by Streamlit.

## ✨ Features

- 🖼️ Load and edit images in common formats (JPG, PNG, etc.)
- 🎨 Apply various filters:
  - ☀️ Brightness adjustment
  - 📊 Contrast adjustment
  - 🌫️ Blur effect with customizable radius
  - 🔲 Black & White conversion
  - ✨ Sharpen with adjustable intensity
  - 🧱 Sepia tone effect
  - 🔄 Invert colors
  - ↩️ Undo/Redo functionality
  - 🔄 Rotate images
- 💾 Save edited images
- 📱 User-friendly web interface with Streamlit
- 🚀 Command-line interface for quick edits

## 🚀 Installation

1. Clone this repository:
```bash
git clone https://github.com/asadullah48/python-image-editor.git
cd python-image-editor
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## 📋 Usage

### Command-line Interface

Run the application from the command line:

```bash
python main.py
```

Follow the prompts to:
1. Load an image
2. Apply filters
3. Save the edited image

### Streamlit Web Interface

Launch the Streamlit app:

```bash
streamlit run app.py
```

This will open a web browser with the image editor interface where you can:
1. Upload an image
2. Apply filters and adjustments
3. Download the edited image

## 🧩 Project Structure

```
python-image-editor/
├── image_editor.py     # Core ImageEditor class
├── filters.py          # Image filter functions
├── main.py             # Command-line interface
├── app.py              # Streamlit web interface
├── requirements.txt    # Project dependencies
├── LICENSE             # MIT License
└── README.md           # This file
```

## 📦 Dependencies

- [Pillow (PIL Fork)](https://python-pillow.org/) - For image processing
- [Streamlit](https://streamlit.io/) - For the web interface

## 🧪 Example

```python
from image_editor import ImageEditor

# Initialize editor with an image
editor = ImageEditor("path/to/image.jpg")

# Apply filters
editor.apply("apply_brightness", 1.5)  # Increase brightness
editor.apply("apply_contrast", 1.2)    # Increase contrast
editor.apply("apply_blur", 2)         # Apply blur with radius 2

# Save the result
editor.save("output.jpg")
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

- [Asadullah](https://github.com/asadullah48)

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/asadullah48/python-image-editor/issues).

1. Fork the project
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request"# python-image-editor" 
