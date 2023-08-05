from setuptools import setup

setup(
    name='TwitterToReddit',
    packages=['TwitterToReddit'],
    version='v0.1.4',
    description='Simple python bot that crossposts Tweets to reddit',
    author='Thomas Lue',
    author_email='thomasvanhalen01@gmail.com',
    url='https://github.com/l3d00m/TwitterToReddit/',
    download_url='https://github.com/l3d00m/TwitterToReddit/tarball/v0.1.4',
    keywords=['reddit', 'twitter', 'bot'],
    license='MIT',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "Programming Language :: Python :: 3.4"
    ],
    install_requires=[
        'praw',
        'tweepy',
    ],
    entry_points={
        'console_scripts': [
            'TwitterToRedditBot = TwitterToReddit.__main__:main'
        ]
    },
)
