from setuptools import setup

setup(
    name = 'mylibrary',
    version = '0.0.3',
    keywords = ('simple', 'test'),
    description = 'just a simple test',
    license = 'Apache License 2.0',
    author = 'breeze',
    author_email = 'whitney_0323@163.com', 
    url          = 'https://github.com/rainmanwy/robotframework-SikuliLibrary', 
    package_dir  = {'' : 'src'},
    packages     = ['java','python'],
    include_package_data = True,
)