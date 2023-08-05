from setuptools import setup, find_packages
import os

version = '1.1.3'


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

long_description = (
    read('README.txt')
    + '\n' +
    read('js', 'bootstrapdatepicker', 'test_bootstrapdatepicker.txt')
    + '\n' +
    read('CHANGES.txt'))

setup(
    name='js.bootstrapdatepicker',
    version=version,
    description="Fanstatic packaging of bootstrap-datepicker.js.",
    long_description=long_description,
    classifiers=[],
    keywords='fanstatic bootstrap date widget',
    author='Nathan Van Gheem',
    author_email='vangheem@gmail.com',
    url='https://github.com/vangheem/js.bootstrapdatepicker',
    download_url='https://pypi.python.org/pypi/js.bootstrapdatepicker',
    license='GPL',
    packages=find_packages(),
    namespace_packages=['js'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'fanstatic',
        'js.bootstrap',
        'setuptools'
    ],
    entry_points="""
    # -*- Entry points: -*-
    [fanstatic.libraries]
    bootstrap = js.bootstrapdatepicker:library
    """,
)
