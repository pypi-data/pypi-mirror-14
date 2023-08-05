from setuptools import setup

setup(
    name='sanelogging',
    version='1.0.0',
    author='Jeffrey Paul',
    author_email='sneak@sneak.berlin',
    packages=['sanelogging'],
    url='https://github.com/sneak/sanelogging/',
    license='LICENSE.txt',
    description='Python logging for humans',
    long_description=open('README.md').read(),
    install_requires=[
        "colorlog",
    ],
)
