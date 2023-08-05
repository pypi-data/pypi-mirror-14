"""Install Caenbrew."""
from setuptools import find_packages, setup


setup(
    name="caenbrew",
    version="0.0.5",
    author="Waleed Khan",
    author_email="wkhan@umich.edu",
    description="Install packages on CAEN.",
    url="https://github.com/arxanas/caenbrew",

    packages=find_packages(),
    entry_points="""
    [console_scripts]
    caenbrew=caenbrew.__main__:cli
    """,
    install_requires=["click==6.3",
                      "sh==1.11"],
)
