from distutils.core import setup

version = __import__('chatter_learning').__version__
author = __import__('chatter_learning').__author__
author_email = __import__('chatter_learning').__email__
setup(
    name = 'ChatterLearning',
    packages = [
        'chatter_learning',
        'chatter_learning.brains',
        'chatter_learning.store_adapters',

    ],
    install_requires = ['pymongo', 'jieba'],
    package_data={'chatter_learning.brains':['*.big']},
    scripts = [],
    version = version,
    description = 'Automatic Chat',
    author = author,
    author_email = author_email,
    url = 'https://github.com/gcaaa31928/ChatterLearningt',
    download_url = 'https://github.com/gcaaa31928/ChatterLearning/releases/tag/v1.0',
    keywords = ['ai', 'chat', 'bot'],
    classifiers = [],
)