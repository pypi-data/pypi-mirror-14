from setuptools import setup

setup(
    name = 'mylibrary',
    version = '0.0.1',
    keywords = ('simple', 'test'),
    description = 'just a simple test',
    license = 'Apache License 2.0',
    author = 'breeze',
    author_email = 'whitney_0323@163.com',  
    package_dir  = {'' : 'src'},
    packages     = ['java','java.com','python'],
    include_package_data = True,
)