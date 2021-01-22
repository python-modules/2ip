
#!/usr/bin/env python
import os
import sys
from codecs import open
from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))

# 'setup.py publish' shortcut.
if sys.argv[-1] == 'publish':
    os.system('python3 setup.py sdist bdist_wheel')
    os.system('python3 -m twine upload dist/*')
    sys.exit()

about = {}
with open(os.path.join(here, 'twoip', '__version__.py'), 'r', 'utf-8') as f:
    exec(f.read(), about)

with open('README.md', 'r', 'utf-8') as f:
    readme = f.read()

with open('requirements.txt', 'r', 'utf-8') as f:
    requires = f.read().splitlines()

test_requirements = [
    'pytest'
]

# If username is in the version file, append it to the package name
if '__username__' in about:
    name = f'{about["__title__"]}-{about["__username__"]}'
else:
    name = about['__title__']

setup(
    name=name,
    version=about['__version__'],
    description=about['__description__'],
    long_description=readme,
    long_description_content_type='text/markdown',
    author=about['__author__'],
    author_email=about['__author_email__'],
    url=about['__url__'],
    packages=find_packages(exclude=('tests',)),
    include_package_data=True,
    python_requires='>= 3.6',
    install_requires=requires,
    tests_require=test_requirements,
    license=about['__license__'],
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)