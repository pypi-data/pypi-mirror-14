from codecs import open as codecs_open
from setuptools import setup

import tornado_async_odm


setup(
    name='tornado_async_odm',
    version=tornado_async_odm.__version__,
    url='https://github.com/shicky/tornado_async_odm',
    download_url='https://github.com/shicky/tornado_async_odm/tarball/v1.0.0',
    license='MIT',
    author='Sick Yoon',
    author_email='shicky@gmail.com',
    description='Asynchronous Object Document Mapper designed for Tornado Web Server',
    packages=['tornado_async_odm'],
    install_requires=['tornado', 'motor'],
    zip_safe=False,
    keywords=['webserver', 'tornado', 'flask', 'orm', 'odm', 'database'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ]
)


