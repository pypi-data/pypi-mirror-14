import os

from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='TwitterToReddit',
    packages=['TwitterToReddit'],  # this must be the same as the name above
    version='v0.1',
    description='Simple python bot that crossposts Tweets to reddit',
    long_description=read('README.md'),
    author='Thomas Lue',
    author_email='thomasvanhalen01@gmail.com',
    url='https://github.com/l3d00m/TwitterToReddit/',  # use the URL to the github repo
    download_url='https://github.com/l3d00m/TwitterToReddit/tarball/v0.1',  # I'll explain this in a second
    keywords=['reddit', 'twitter', 'bot'],  # arbitrary keywords
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Topic :: Utilities",
        "Programming Language :: Python :: 3.4"
    ],
    install_requires=[
        'praw',
        'tweepy'
    ],
)
