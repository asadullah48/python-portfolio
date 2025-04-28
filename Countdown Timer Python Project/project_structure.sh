countdown-timer/
├── src/
│   ├── __init__.py
│   ├── cli/
│   │   ├── __init__.py
│   │   ├── countdown_timer.py
│   │   └── cli_utils.py
│   ├── web/
│   │   ├── __init__.py
│   │   ├── streamlit_timer.py
│   │   └── web_utils.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── timer.py
│   │   └── presets.py
│   └── utils/
│       ├── __init__.py
│       ├── theme_manager.py
│       └── sound_manager.py
├── static/
│   ├── sounds/
│   │   ├── alert.mp3
│   │   └── tick.mp3
│   ├── images/
│   │   ├── favicon.ico
│   │   └── logo.png
│   └── css/
│       └── custom.css
├── presets/
│   └── timer_presets.json
├── tests/
│   ├── __init__.py
│   ├── test_timer.py
│   ├── test_presets.py
│   └── test_utils.py
├── docs/
│   ├── installation.md
│   ├── usage.md
│   ├── api.md
│   └── contributing.md
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   └── workflows/
│       └── python-app.yml
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
├── requirements-dev.txt
└── pyproject.toml