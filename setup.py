from setuptools import setup, find_packages

with open("readme.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["pandas>=0.24", "xlrd>=1", "requests>=2"]

setup(
    name="aam_api",
    version="0.0.59",
    author="Trevor McCormick",
    author_email="trevor.ryan.mccormick@gmail.com",
    description="Adobe Audience Manager API Python Wrapper",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/tmcormick92/aam_api/",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
