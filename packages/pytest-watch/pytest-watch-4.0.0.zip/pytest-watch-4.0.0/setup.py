import os
from setuptools import setup, find_packages


def read(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as f:
        return f.read()


setup(
    name='pytest-watch',
    version='4.0.0',
    description='Local continuous test runner with pytest and watchdog.',
    long_description=read('README.md'),
    author='Joe Esposito',
    author_email='joe@joeyespo.com',
    url='http://github.com/joeyespo/pytest-watch',
    license='MIT',
    platforms='any',
    packages=find_packages(),
    install_requires=read('requirements.txt').splitlines(),
    entry_points={
        'console_scripts': [
            'pytest-watch = pytest_watch:main',
            'ptw = pytest_watch:main',
        ]
    },
)
