from distutils.core import setup

setup(
    name = 'ChatterLearning',
    packages = ['chatter_learning'],
    install_requires=[
        'pymongo',
        'jieba'
    ],
    scripts = [],
    version = '1.0',
    description = 'Automatic Chat',
    author = 'GCA',
    author_email = 'gcaaa31928gmail.com',
    url = 'https://github.com/gcaaa31928/ChatterLearningt',
    download_url = 'https://github.com/gcaaa31928/ChatterLearning/releases/tag/v1.0',
    keywords = ['ai', 'chat', 'bot'],
    classifiers = [],
)