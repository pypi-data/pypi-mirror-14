from setuptools import setup
import natgeo

setup(
    name="natgeo_photo",
    version="0.0.1",
    author=natgeo.__author__,
    author_email="medazizknani@gmail.com",

    keywords="natgeo photo day grabber",
    install_requires=[
        "requests",
        "beautifulsoup4"
    ],
    packages=['natgeo']

)
