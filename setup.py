import setuptools

content = open("README.md", "r").read()
lines = content.split("\n")

packagename = "sanic-dantic"
author = "Connor Zhang"
author_email = "chzhangyue@outlook.com"
version = "1.2.2"
description = "".join(lines[11:13])
long_description = "\n".join(lines)

setuptools.setup(
    author=author,
    version=version,
    name=packagename,
    python_requires='>=3.7',
    description=description,
    author_email=author_email,
    license_files=('LICENSE',),
    long_description=long_description,
    packages=setuptools.find_packages(),
    install_requires=['pydantic>=1.9.1'],
    long_description_content_type="text/markdown",
    url="https://github.com/misss85246/sanic-dantic",
    classifiers=[
        "Topic :: Utilities",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
    ]
)
