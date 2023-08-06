from setuptools import find_packages, setup
exec(open("aster/version.py").read())


setup_args = {
    'name': 'aster',
    'version': __version__,
    'url': 'https://github.com/seiyanuta/aster',
    'author': 'Seiya Nuta',
    'author_email': 'nuta@seiya.me',
    'description': 'A pythonic serverless web application framework for minimalist',
    'license': 'Public Domain',
    'packages': ['aster'],
    'scripts': ['bin/aster'],
    'install_requires': open('requirements.txt').read().strip().splitlines(),
    'classifiers': [
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: Public Domain',
        'Programming Language :: Python :: 3'
    ],
}


if __name__ == '__main__':
    setup(**setup_args)
