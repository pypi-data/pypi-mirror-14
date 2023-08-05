from setuptools import setup, find_packages
import safeurl

setup(
    name='safeurl',
    version=safeurl.__version__,
    packages=find_packages(),
    long_description=open('README.rst').read(),
    install_requires=[
        'requests==2.7.0'
    ],
    test_suite='tests',
    author='Fedor Isakov',
    author_email='mydearfrodo@yandex.ru',
    url='https://github.com/FrodoTheTrue/safeurl',
    keywords=['python', 'analizer', 'urls'],
    description=(
    "Simple and clever analyzer, decoder, encoder ... urls on python, using requests"),
    license = "MIT",

)
