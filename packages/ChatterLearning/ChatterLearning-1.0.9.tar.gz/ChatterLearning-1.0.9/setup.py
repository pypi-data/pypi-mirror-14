from setuptools import setup, find_packages

setup(
    name = 'ChatterLearning',
    packages = find_packages(),
    install_requires=['pymongo', 'jieba', 'fuzzywuzzy'],
    package_data={'chatter_learning.brains':['*.big']},
    scripts = [],
    version = '1.0.9',
    description = 'Automatic Chat',
    author = 'GCA',
    author_email = 'gcaaa31928@gmail.com',
    url = 'https://github.com/gcaaa31928/ChatterLearningt',
    download_url = 'https://github.com/gcaaa31928/ChatterLearning/releases/tag/v1.0',
    keywords = ['ai', 'chat', 'bot'],
    classifiers = [],
)