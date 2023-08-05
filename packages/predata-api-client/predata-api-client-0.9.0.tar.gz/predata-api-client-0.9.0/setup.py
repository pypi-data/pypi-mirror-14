from setuptools import setup

setup(
    name='predata-api-client',
    version='0.9.0',
    description='Predata Python API Client',
    author='predata',
    author_email='dev@predata.com',
    url='http://www.predata.com',
    packages=['predata', 'predata/clients', 'predata/config'],
    install_requires=[
        'requests==2.5.1',
    ],
    setup_requires=[
        'nose>=1.0',
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
