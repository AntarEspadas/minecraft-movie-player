from setuptools import setup, find_packages
import os

HERE = os.path.abspath(".")

try:
    with open("readme.md", "r") as readme:
        long_description = readme.read()
except OSError:
    long_description = "For more information, see [https://github.com/Naratna/minecraft-movie-player](https://github.com/Naratna/minecraft-movie-player#readme)"
    
install_requires ='''kdtree>=0.16
nbtlib>=1.8.1
opencv-python>=4.4.0.42
pydub>=0.24.1'''.split("\n")

setup(
    name="minecraft-movie-player",
    version = "0.3.0",
    author = "Naratna",
    author_email = "antar.espadas@hotmail.com",
    description = "A command line program that generates a datapack that plays videos in vanilla Minecraft",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/Naratna/minecraft-movie-player",
    packages = find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires = ">=3.8",
    install_requires = install_requires,
    entry_points='''[console_scripts]
            mc-movie = minecraft_movie_player.__main__:main''',
    license = "MIT",
    includa_package_data=True,
    package_data = {"": ["palette.txt", "index.txt"]}
)