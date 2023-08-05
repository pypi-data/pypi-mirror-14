#from distutils.core import setup
from setuptools import setup

setup(
    name='dhl_shipping',
    version='1.0.2',
    author='Hasanuzzaman Syed',
    author_email='hasanuzzaman.syed@gmail.com',
    packages=['dhl_shipping'],
    url='http://pypi.python.org/pypi/dhl_shipping/',
    license='LICENSE.txt',
    description='DHL Shipping - Quote, Pick Up, Shipping, Label Creation, Tracking',
    long_description=open('README.txt').read(),
    install_requires=[
        'xmltodict',
    ],
)
