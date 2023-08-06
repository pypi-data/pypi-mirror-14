from distutils.core import setup
from setuptools import find_packages
from bgcluster import __version__, __author__

setup(
    name='bgcluster',
    version=__version__,
    packages=find_packages(),
    url='http://bg.upf.edu',
    license='UPF Free Source Code',
    author=__author__,
    author_email='jordi.deu@upf.edu',
    description='',
    install_requires=[
        'cherrypy',
        'ws4py', 'requests'
    ],

    entry_points={
        'console_scripts': [
            'bg-tee = bgcluster.utils.tee:cmdline',
            'bg-ping = bgcluster.utils.ping:cmdline'
        ]
    }
)
