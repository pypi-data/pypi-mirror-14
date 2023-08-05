from setuptools import setup

setup(
    name='sanelogging',
    version='1.0.1',
    author='Jeffrey Paul',
    author_email='sneak@sneak.berlin',
    packages=['sanelogging'],
    url='https://github.com/sneak/sanelogging/',
    license='LICENSE.txt',
    description='Python logging for humans',
    install_requires=[
        "colorlog",
    ],
)
