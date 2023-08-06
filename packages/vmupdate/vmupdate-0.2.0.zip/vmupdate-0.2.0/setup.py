from io import open
from os.path import abspath, dirname, join
from setuptools import setup, find_packages

from vmupdate import __version__

cur_dir = abspath(dirname(__file__))

with open(join(cur_dir, 'README.rst'), encoding='utf-8') as readme_file:
    long_description = readme_file.read()

with open(join(cur_dir, 'LICENSE'), encoding='utf-8') as license_file:
    license = license_file.read()

setup(
    name='vmupdate',
    version=__version__,
    description='Command line utility used to keep your virtual machines up to date.',
    long_description=long_description,
    license=license,
    author='Corwin Tanner',
    author_email='corwintanner@gmail.com',
    url='https://github.com/corwintanner/vmupdate',
    packages=find_packages(),
    data_files=[
        ('data', ['vmupdate/data/vmupdate.yaml']),
        ('logging', ['vmupdate/data/logging.yaml'])],
    include_package_data=True,
    zip_safe=False,
    install_requires=['PyYAML>=3', 'keyring>=8', 'paramiko>=1'],
    entry_points={
        'console_scripts': [
            'vmupdate=vmupdate.cli:main',
        ],
    },
    test_suite='tests',
    tests_require=['mock>=1.3'],
    keywords=['vm', 'update', 'virtual', 'machine'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
    ],
)
