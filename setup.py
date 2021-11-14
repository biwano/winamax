"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
"""
 
import setuptools
 
with open("README.md", "r") as fh:
    long_description = fh.read()
 
setuptools.setup(
    name="winamax",
    version="0.0.1",
    author="Bruno Ilponse",
    author_email="bruno.ilponse@gmail.com",
    description="Winamax",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/biwano/ftxbot.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "sqlalchemy",
        "requests",
        "flask",
        "flask_cors",
        "webdriver-manager",
        "selenium-wire"
    ]
)