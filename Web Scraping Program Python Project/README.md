# 🔍 GitHub Profile Explorer

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://github-profile-explorer.streamlit.app)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.13%2B-blue)](https://www.python.org/downloads/)
[![GitHub Stars](https://img.shields.io/github/stars/yourusername/github-profile-explorer?style=social)](https://github.com/yourusername/github-profile-explorer)

A modern, feature-rich web application that allows you to explore GitHub user profiles, repositories, and activity statistics using the GitHub API.

![App Screenshot](./screenshots/app_screenshot.png)

## ✨ Features

- 👤 **Comprehensive Profile Information**: View detailed user information including bio, location, email, and website
- 📊 **Interactive Statistics**: Visualize followers, following, repositories, and gists
- 📚 **Repository Explorer**: Browse, filter, and sort repositories with advanced filtering options
- 📈 **Data Visualization**: Interactive charts for language distribution, activity patterns, and repository metrics
- 🏢 **Organization Information**: View organizations the user belongs to
- 📱 **Responsive Design**: Modern UI that works on desktop and mobile devices
- 🌓 **Theme Options**: Choose between light and dark themes
- 📥 **Data Export**: Download repository data in CSV or JSON formats
- ⚡ **Performance Optimized**: Caching for faster load times and reduced API calls

## 🚀 Getting Started

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/github-profile-explorer.git
cd github-profile-explorer

# Create and activate a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the App

```bash
streamlit run app.py
```

The app will be available at http://localhost:8501

## 🔧 Configuration

To increase the GitHub API rate limit, you can add your GitHub personal access token to a `.streamlit/secrets.toml` file:

```toml
# .streamlit/secrets.toml
github_token = "your-github-personal-access-token"
```

## 📖 Usage

1. Enter a GitHub username or profile URL in the search box
2. Click the "Explore Profile" button
3. Browse through the user's profile information, repositories, and statistics
4. Use the filtering and sorting options to customize the view
5. Export data as needed

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

- [Streamlit](https://streamlit.io/) for the amazing web app framework
- [GitHub API](https://docs.github.com/en/rest) for providing the data
- [Plotly](https://plotly.com/) for interactive visualizations
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) for web scraping capabilities