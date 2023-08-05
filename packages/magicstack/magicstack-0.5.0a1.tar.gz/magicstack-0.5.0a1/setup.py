from setuptools import setup


setup(**{
    'name': 'magicstack',
    'version': '0.5.0a1',
    'description': 'MagicStack Application Development Framework',
    'maintainer': 'MagicStack Inc.',
    'maintainer_email': 'devteam@magic.io',
    'url': 'http://magic.io',
    'platforms': ['any'],

    'packages': ['magicstack'],
    'include_package_data': True,
    'exclude_package_data': {
        '': ['.gitignore']
    },

    'classifiers': [
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5'
    ]
})
