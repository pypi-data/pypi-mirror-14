from setuptools import setup, find_packages

setup(
    name='encrypteddict',
    version='0.0.1',
    description='A python library to decrypt values in dictionaries',
    url='https://github.com/grahamhar/encrypted-dict',
    author='Graham Hargreaves',
    license='Apache Licence 2.0',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='encryption gpg dict',
    packages=find_packages(exclude=['static', 'docs', 'tests']),
    install_requires=['pygpgme'],

    # $ pip install -e .[dev]
    extras_require={
        'dev': ['flake8', 'nose', 'PyYaml'],
    },
)
