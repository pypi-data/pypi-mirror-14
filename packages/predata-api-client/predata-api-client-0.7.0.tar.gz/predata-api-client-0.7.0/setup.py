from setuptools import setup

setup(
    name='predata-api-client',
    version='0.7.0',
    description='Predata Python API Client',
    author='predata',
    author_email='dev@predata.com',
    url='http://www.predata.com',
    packages=['predata', 'predata/clients', 'predata/config'],
    install_requires=[
        'requests==2.5.1',
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    test_suite='nose.collector',
    test_requires=['nose==1.3.7'],
)
