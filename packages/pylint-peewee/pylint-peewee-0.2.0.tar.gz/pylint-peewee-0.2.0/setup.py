from distutils.core import setup

packages = ['pylint_peewee']

setup(
    name='pylint-peewee',
    packages=packages,
    package_dir={'pylint_peewee': 'pylint_peewee'},
    version='0.2.0',
    description='PyLint extensions for PeeWee',
    author='Hayden Chudy',
    author_email='hjc1710@gmail.com',
    url='https://github.com/hjc1710/pylint-peewee',
    download_url='https://github.com/hjc1710/pylint-peewee/archive/v0.2.0.tar.gz',
    keywords=['peewee', 'pylint', 'plugin',],
    classifiers=[
        "Environment :: Console",
        "Programming Language :: Python :: 2.7",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Quality Assurance",
    ],
)
