import os

import setuptools


setuptools.setup(
    name='packagedemo',
    version='2015.09.1',
    keywords='demo',
    description='A demo for python packaging.',
    long_description=open(
        os.path.join(
            os.path.dirname(__file__),
            'README.rst'
        )
    ).read(),
    author='vanderliang',
    author_email='vanderliang@gmail.com',
    url='https://github.com/DeliangFan/packagedemo',
    packages=setuptools.find_packages(),
    license='MIT'
)
