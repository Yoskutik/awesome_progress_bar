import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="awesome-progress-bar",
    version="1.7.2",
    author="Yoskutik",
    author_email="yoskutik@gmail.com",
    description="Progress bar for terminal",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yoskutik/awesome_progress_bar",
    packages=setuptools.find_packages(exclude=['test', 'test.*', '*.gif', 'examples.py']),
    classifiers=[
        "Programming Language :: Python :: 3.4",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.4',
    include_package_data=True,
    exclude_package_data={
        '': ['preview.gif'],
    }
)