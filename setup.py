import os
from setuptools import setup, find_packages

HERE = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(HERE, 'README.md')) as f:
    README = f.read()

URL = "https://github.com/vincentzhchen/redquill"

setup(
    name="redquill",
    version="0.0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["pandas>=0.18.0"],
    setup_requires=["pytest-runner"],
    tests_require=["pytest-cov"],
    python_requires=">=3.6",

    # metadata to display on PyPI
    license="Apache 2.0",
    description="Logging for pandas and more.",
    long_description=README,
    long_description_content_type="text/markdown",

    author="Vincent Chen",
    author_email="vincent.zh.chen@gmail.com",
    url=URL,
    project_urls={
        "Source": URL
    },
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: System :: Logging",
    ],
)
