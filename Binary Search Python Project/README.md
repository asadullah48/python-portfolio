# 🔍 Binary Search Visualizer

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=for-the-badge&logo=Matplotlib&logoColor=black)

An interactive web application that visualizes the binary search algorithm with real-time step-by-step animation.

![Binary Search Visualization Demo](demo.gif) *(Replace with your actual demo gif)*

## 🌟 Features

- **Interactive visualization** of binary search algorithm
- **Two visualization modes**:
  - Graphical (using Matplotlib)
  - Text-based (fallback when Matplotlib not available)
- **Adjustable animation speed**
- **Detailed step-by-step explanation**
- **Input validation** for sorted arrays
- **Responsive design** works on all devices
- **Educational tool** for understanding algorithms

## 🚀 Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/asadullah48/-Binary-Search.git
   cd binary-search-python-project
Project Structure
binary-search-python-project/
├── main.py                # Main application code
├── requirements.txt      # Dependencies
├── README.md             # This file
└── assets/               # Optional: Store demo gifs/images
    └── demo.gif
    📝 How to Use
Enter a sorted comma-separated list of numbers (e.g., 1, 3, 5, 7, 9)

Enter the target value you want to search for

Adjust the animation speed slider

Click "Run Search" to visualize the algorithm

Explore the detailed steps in the expandable section

📚 Algorithm Explanation
Binary search is an efficient algorithm for finding an item from a sorted list of items. It works by repeatedly dividing in half the portion of the list that could contain the item.

Time Complexity: O(log n)
Space Complexity: O(1)

Project Link: https://github.com/asadullah48/binary-search-python-project

Copy

### Additional Recommendations:

1. **Create a requirements.txt** file:
   ```text
   streamlit>=1.13.0
   matplotlib>=3.6.0
   numpy>=1.23.0
