from setuptools import setup

setup(name = "cephalopod",
    version = "0.11a0",
    description = "package to manage SIMS data remotely",
    url = "https://github.com/copperwire/cephalopod.git",
    author = "Robert Solli",
    author_email = "octopus.prey@gmail.com",
    license  ="MIT",
    packages = ["cephalopod"],
    install_requires = [
           "numpy",
           "bokeh"],
    zip_safe = False )
