from setuptools import setup


setup(
    name='pytest-start-from',
    description='Start pytest run from a given point',
    url='https://bitbucket.org/dtao/pytest-start-from',
    author='Dan Tao',
    author_email='daniel.tao@gmail.com',
    packages=['pytest_start_from'],
    version='0.1.0',
    install_requires=['pytest>=2.5'],
    entry_points={
        'pytest11': ['start-from = pytest_start_from']
    },
)
