from distutils.core import setup
from setuptools import find_packages


setup(
    name = "correly",
    version = "0.0.1",
    description = "mqtt timescale bridge",
    author = "Alex Swhehla",
    author_email = "alex.swehla@gmail.com",
    url = "https://www.github.com/lordspacehog/correly",
    packages = find_packages(),
    entry_points = {
        'console_scripts': ['correly=correly.__main__:main'],
    },
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
