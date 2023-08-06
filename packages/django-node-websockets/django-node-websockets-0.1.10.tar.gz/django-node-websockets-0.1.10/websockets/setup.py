from setuptools import setup, find_packages

setup(
    name='django-node-websockets',
    version='0.1.1',
    author='John Leith',
    author_email='leith.john@gmail.com',
    packages=find_packages(),
    description='Tool to quick async/websocket integration',
    install_requires=[
        'six'
    ]
)
