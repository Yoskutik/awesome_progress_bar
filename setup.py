import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="awesome-progress-bar",
    version="0.0.1",
    author="Yoskutik",
    author_email="yoskutik@gmail.com",
    description="Progress bar for terminal",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yoskutik/awesome_progress_bar",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)