import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sanic-dantic",
    version="1.1.4",
    author="Connor Zhang",
    author_email="chzhangyue@outlook.com",
    description="A request parameter checking and parsing library based on pydantic under the sanic framework",
    install_requires=['pydantic>=1.7.2', 'nest-asyncio>=1.4.2'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/misss85246/sanic-dantic",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Utilities",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.6.5',
)
