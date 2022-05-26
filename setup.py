import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sanic-dantic",
    version="1.2.0",
    author="Connor Zhang",
    author_email="chzhangyue@outlook.com",
    description="A request parameter checking and parsing library " +
                "based on pydantic under the sanic framework",
    install_requires=['pydantic>=1.9.0'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/misss85246/sanic-dantic",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Utilities",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.8',
)
