# pyinfra
# File: setup.py
# Desc: needed

from setuptools import setup

from pyinfra import __version__


if __name__ == '__main__':
    setup(
        version=__version__,
        name='pyinfra',
        description='Deploy stuff by diff-ing the state you want against the remote server.',
        author='Nick / Fizzadar',
        author_email='pointlessrambler@gmail.com',
        license='MIT',
        url='http://github.com/Fizzadar/pyinfra',
        packages=(
            'pyinfra',
            'pyinfra.api',
            'pyinfra.facts',
            'pyinfra.facts.util',
            'pyinfra.modules',
            'pyinfra.modules.util'
        ),
        package_dir={
            'pyinfra': 'pyinfra'
        },
        scripts=(
            'bin/pyinfra',
        ),
        install_requires=(
            'gevent',
            'paramiko',
            'docopt',
            'colorama',
            'termcolor',
            'jinja2',
            'python-dateutil',
            'six'
        ),
        extras_require={
            'dev': (
                # Dev debugging
                'ipdb',

                # Dev testing requirements
                'nose==1.3.7',
                'jsontest==1.2',
                'coverage==4.0.3',
                'mock==1.3.0',

                # Dev docs requirements
                'sphinx==1.3.1',
                'sphinx-autobuild==0.5.2'
            )
        }
    )
