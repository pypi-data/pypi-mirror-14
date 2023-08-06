from setuptools import setup, find_packages

setup(
    name = 'mylibrary',
    version = '0.0.2',
    keywords = ('simple', 'test'),
    description = 'just a simple test',
    license = 'Apache License 2.0',
    author = 'breeze',
    author_email = 'whitney_0323@163.com',  
    packages = find_packages(),
    include_package_data = True,
)