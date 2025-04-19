# 🔍 QR Code Generator & Scanner

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://qr-code-app.streamlit.app/)
[![GitHub](https://img.shields.io/github/license/asadullah48/qr-code-app)](https://github.com/asadullah48/qr-code-app/blob/main/LICENSE)
[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

A powerful and user-friendly web application for generating and scanning QR codes with customization options.

![App Screenshot](https://raw.githubusercontent.com/asadullah48/qr-code-app/main/app_screenshot.png)

## ✨ Features

- **Generate QR Codes**: Create QR codes from any text or URL
- **Customize QR Codes**: Change colors, size, and border thickness
- **Download QR Codes**: Save generated QR codes as image files
- **Scan QR Codes**: Upload and decode existing QR code images
- **Responsive Design**: Works on desktop and mobile devices

## 🚀 Demo

View the live demo: [QR Code Generator & Scanner App](https://qr-code-app.streamlit.app/)

## 🛠️ Installation

### Prerequisites
- Python 3.7 or higher

### Setup Instructions

1. Clone this repository:
   ```bash
   git clone https://github.com/asadullah48/qr-code-app.git
   cd qr-code-app
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   streamlit run app.py
   ```

5. Open your browser and navigate to:
   ```
   http://localhost:8501
   ```

## 📱 Usage

### Generating QR Codes

1. Select "Generate QR Code" from the sidebar
2. Enter text or URL in the input field
3. Customize the QR code appearance (optional)
4. Click "Generate QR Code"
5. Download the generated QR code

### Scanning QR Codes

1. Select "Scan QR Code" from the sidebar
2. Upload an image containing a QR code
3. Click "Scan QR Code"
4. View and copy the decoded data

## 📋 Implementation Details

This application is built using:

- **Streamlit**: For the web interface
- **qrcode**: For generating QR codes
- **OpenCV**: For QR code detection and decoding
- **Pillow**: For image processing
- **NumPy**: For array operations

## 🔄 Commits & Development History

### Initial Commit: Application Setup
- 📁 Project structure setup
- 🔧 Basic QR code generation functionality
- 📝 README creation

### Feature Update: QR Code Scanner
- 🔍 Added QR code scanning capability
- 🖼️ Image upload functionality
- 🔄 Decoder implementation with OpenCV

### UI Enhancements
- 💄 Improved user interface
- 🎨 Added QR code customization options
- 📱 Responsive design for all devices

### Final Improvements
- ⚡ Performance optimizations
- 🛠️ Bug fixes and code refactoring
- 📊 Added download and sharing options

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Asadullah**
- GitHub: [@asadullah48](https://github.com/asadullah48)

## 🙏 Acknowledgements

- [Streamlit](https://streamlit.io/) for the amazing web app framework
- [qrcode](https://github.com/lincolnloop/python-qrcode) library contributors
- [OpenCV](https://opencv.org/) for image processing capabilities

---

Built with ❤️ by [Asadullah](https://github.com/asadullah48)"# qr-code-app" 
