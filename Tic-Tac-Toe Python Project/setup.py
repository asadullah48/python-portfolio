import setuptools

setuptools.setup(
    name="TicTacToe",
    version="0.1.0",
    author="Asadullah48",
    author_email="your.email@example.com",
    description="A Tic Tac Toe game with Pygame and Streamlit implementations",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "pygame>=2.1.0",
        "streamlit>=1.20.0",
    ],
)