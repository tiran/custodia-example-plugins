import os

from setuptools import setup

requirements = [
    'custodia',
]

# test requirements
test_requires = ['coverage', 'pytest', 'mock'] + requirements

extras_require = {
    'test': test_requires,
    'test_docs': ['docutils', 'markdown'],
    'test_pep8': [
        'flake8', 'flake8-import-order', 'pep8-naming',
    ] + requirements,
    'test_pylint': ['pylint'] + test_requires,
}


with open('README') as f:
    long_description = f.read()


about = {}
with open(os.path.join('src', 'custodiaexample', '__about__.py')) as f:
    exec(f.read(), about)


setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__summary__'],
    long_description=long_description,
    license=about['__license__'],
    url=about['__uri__'],
    author=about['__author__'],
    author_email=about['__email__'],
    maintainer=about['__author__'],
    maintainer_email=about['__email__'],
    package_dir={'': 'src'},
    packages=[
        'custodiaexample',
    ],
    entry_points={
        'custodia.authenticators': [
            'ExampleAuth = custodiaexample.auth:ExampleAuth',
        ],
        'custodia.authorizers': [
            'ExampleAuthz = custodiaexample.authz:ExampleAuthz',
        ],
        'custodia.stores': [
            'ExampleStore = custodiaexample.store:ExampleStore',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Intended Audience :: Developers',
        'Topic :: Security',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    install_requires=requirements,
    tests_require=test_requires,
    extras_require=extras_require,
)
