from setuptools import find_packages
from setuptools import setup


with open('README.rst', 'r') as f:
  readme = f.read()


with open('LICENSE', 'r') as f:
  license = f.read()


setup(
    name = 'python-pyparts',
    version = '1.0.0', 
    description = 'A cross platform library for embedded hardware development using single board computers.',
    long_description = readme,
    author = 'Sean Watson',
    author_email = 'sean@seanwatson.io',
    url = 'https://gitlab.com/seanwatson/pyparts',
    keywords = 'raspberrypi beagleboard pine64 mbed embedded hardware gpio spi pwm electronics',
    packages = find_packages('src'),
    package_dir = {
        '': 'src',
    },
    package_data = {
        '': ['README.rst', 'LICENSE'],
    },
    test_suite = 'tests',
    install_requires = ['spidev', 'RPi.GPIO'],
    license = 'MIT',
    classifiers = (
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    )
)
