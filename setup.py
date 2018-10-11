from setuptools import find_packages, setup

setup(
    name="DataPlatform",
    version="1.0.0",
    packages=find_packages(),
    maintainer='michael',
    description="big data platform",
    install_requires=[
        'flask',
        'numpy',
        'pandas',
    ]
)
