from setuptools import setup, find_packages

setup(
    name='django-node-websockets',
    version='0.1.11',
    author='John Leith',
    author_email='leith.john@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    description='Websockets',
    install_requires=['requests', 'socket.io-emitter'],
    scripts=["node_config"]
)
