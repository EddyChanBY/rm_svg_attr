import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rm_svg_attr",  # Replace with your own username
    version="0.0.1",
    author="EddyChanBY",
    author_email="",
    description="A short script to remove svg tag's attributes from svg files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/EddyChanBY/rm_svg_attr",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
