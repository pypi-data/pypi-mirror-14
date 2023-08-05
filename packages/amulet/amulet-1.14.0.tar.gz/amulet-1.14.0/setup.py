from setuptools import setup

install_requires = [
    'requests',
    'libcharmstore',
    'PyYAML',
    'path.py'
]

tests_require = [
    'coverage',
    'nose',
    'pep8',
]


setup(
    name='amulet',
    version='1.14.0',
    description='Tools to help with writing Juju Charm Functional tests',
    install_requires=install_requires,
    package_data={'amulet': ['unit-scripts/amulet/*']},
    author='Marco Ceppi',
    author_email='marco@ceppi.net',
    url="https://github.com/juju/amulet",
    packages=['amulet'],
)
