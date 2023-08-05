try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Path Less Traveled',
    'author': 'Matt Olsen',
    'url': 'https://github.com/digwanderlust/pathlt',
    'author_email': 'digwanderlust@gmail.com',
    'version': '0.0.1',
    'install_requires': [
        'nose',
        'coverage',
        'python-coveralls',
        'mock',
        'toolz'
    ],
    'packages': ['pathlt'],
    'entry_points': {
        'console_scripts': [
            'pathlt = pathlt.__main__:main'
        ]
    },
    'name': 'pathlt'
}

setup(**config)
