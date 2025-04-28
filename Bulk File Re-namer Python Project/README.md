# 📁 Bulk File Renamer 🔄

![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

A simple Python script to batch rename files in a directory with customizable prefixes and counters.

## 🌐 Web App Version

We now have a Streamlit web interface! Try it:

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://renamebulkfile.streamlit.app/)

Or run locally:
```bash
uv add streamlit
streamlit run app.py

## ✨ Features

- 🔄 Batch rename files with sequential numbering
- 🏷️ Add custom prefixes to filenames
- 🔍 Filter by specific file extensions
- 📊 Provides detailed renaming summary
- ✅ Case-insensitive extension matching
- 🛠️ Robust error handling

## 🚀 Installation

1. Ensure you have Python 3.6+ installed
2. Clone this repository or download the script:
   ```bash
   git clone https://github.com/asadullah48/Bulk-File-Renamer.git

   🏁 Usage
Run the script from the command line:
python bulk_renamer.py

Example:
📁 Enter the folder path: /Users/me/Pictures
🔤 Enter a prefix for the new filenames: Vacation_
📝 Enter the file extension to rename: .jpg
🔄 Renamed: IMG_001.jpg → Vacation_1.jpg
🔄 Renamed: IMG_002.jpg → Vacation_2.jpg
...
✅ Bulk renaming complete!

📊 Output Example
📊 Renaming Summary:
• Total files processed: 15
• Files renamed: 15
• Files skipped: 0"# Bulk-File-Renamer" 
