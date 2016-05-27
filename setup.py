from setuptools import setup, find_packages
setup(
    name="cinder-data",
    version="0.0.1",
    packages=find_packages(),
    author="Alastair McClelland",
    author_email="alastair.mcclelland@gmail.com",
    description="A library inspired by ember-data for python projects.",
    license="MIT License",
    keywords="ember cinder data rest json api client",
    url="https://github.com/almcc/cinder-data",
    install_requires=[
        "inflection>=0.3.1",
        "requests>=2.10.0",
        "schematics>=1.1.1"
    ]
)
