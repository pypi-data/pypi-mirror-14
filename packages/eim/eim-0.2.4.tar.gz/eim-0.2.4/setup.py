from setuptools import setup

setup(
    name='eim',
    version='0.2.4',
    packages=['eim',
              'eim.tools',
              'eim.documents'],
    url='http://www.musicsensorsemotion.com/',
    license='',
    author='Brennon Bortz',
    author_email='brennon@vt.edu',
    description='Library for interacting with Emotion and Motion resources',
    install_requires=['pymongo', 'pandas', 'mongoengine>=0.10.6', 'numpy', 'scipy']
)
