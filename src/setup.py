import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="settlingInSpace", # Replace with your own username
    version="0.0.1",
    author="calisto",
    author_email="calisto mail",
    description="game of settling in space",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="???",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
