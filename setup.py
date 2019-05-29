import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()

setup(
    name="redquill",
    version="0.0.0",
    description="Logging for pandas and more.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/vincentzhchen/redquill",
    author="Vincent Chen",
    author_email="vincent.zh.chen@gmail.com",
    license="Apache 2.0",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: System :: Logging",
    ],
    packages=["redquill"],
    include_package_data=True,
    install_requires=["requill", "redquill.*"],
)
