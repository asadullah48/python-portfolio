# 🔒 Secure Password Generator

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org/downloads/)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://docs.streamlit.io)

A secure, feature-rich password generator with an intuitive Streamlit interface. Generate strong passwords with various complexity levels, check password strength, and more!

![./ssword Generator Screenshot](./Password%20Generator%20Screenshot/Screenshot%20.png)
## ✨ Features

- **Multiple Complexity Levels**: Choose from low, medium, high, PIN, or memorable passwords
- **Password Strength Analysis**: Visual representation of password strength with entropy calculation
- **Memorable Password Option**: Word-based passwords that are easier to remember but still secure
- **Copy to Clipboard**: One-click copy functionality for convenient use
- **Password Checker**: Assess the strength of your existing passwords
- **Streamlit Interface**: User-friendly web interface
- **Security Best Practices**: Uses Python's `secrets` module for cryptographically strong generation

## 🚀 Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/asadullah48/secure-password-generator.git
   cd secure-password-generator
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## 💻 Usage

### Streamlit Web Interface

Run the Streamlit app:
```bash
streamlit run app.py
```

This will launch the web interface in your default browser.

### Command Line Interface

You can also use the password generator from the command line:

```bash
python cli.py --length 16 --complexity high
```

Command line options:
- `-l, --length`: Password length (default: 12)
- `-c, --complexity`: Complexity level (low, medium, high, pin, memorable) (default: high)
- `-n, --number`: Number of passwords to generate (default: 1)
- `-e, --exclude`: Characters to exclude
- `-i, --interactive`: Run in interactive mode

## 🔐 Password Complexity Levels

- **Low**: Letters and numbers
- **Medium**: Letters, numbers, and some symbols
- **High**: Letters, numbers, and all symbols
- **PIN**: Numbers only
- **Memorable**: Word-based passwords with separators and numbers

## 🛠️ Development

### Requirements

- Python 3.7+
- Dependencies listed in `requirements.txt`

### Project Structure

```
secure-password-generator/
├── app.py              # Streamlit web application
├── cli.py              # Command-line interface
├── password_gen.py     # Core password generator library
├── requirements.txt    # Python dependencies
├── LICENSE             # MIT License
└── README.md           # This file
```

## 📋 Requirements

```
streamlit>=1.22.0
matplotlib>=3.5.0
numpy>=1.20.0
pyperclip>=1.8.2
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Asadullah**

- GitHub: [@asadullah48](https://github.com/asadullah48)"# secure-password-generator" 
