from setuptools import setup, find_packages

setup(
    name="pong-game",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "streamlit>=1.18.0",
        "Pillow>=9.0.0",
    ],
    author="Asadullah",
    author_email="your.email@example.com",
    description="A classic Pong game with Turtle graphics and Streamlit interface",
    keywords="game, pong, turtle, python, streamlit",
    url="https://github.com/asadullah48/pong-game",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)