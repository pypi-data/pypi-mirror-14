import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

ns = {}
with open(os.path.join(here, 'kyper-data', '_version.py')) as f:
   exec(f.read(), {}, ns)

setup(
    name='kyper.data',
    version=ns['__version__'],
    author='Kyper Developers',
    author_email='developers@kyperdata.com',
    packages=find_packages(),
    url='https://git.kyper.co/kyper/kyper-data',
    description='Kyper Data',
    install_requires=[
        "python-dateutil",
        "future",
        "requests",
        "pandas",
        "pyyaml",
        "tzlocal",
        "kyper.util>=0.2.1"
    ],
    tests_require=[
        "mock"
    ],
    extras_require={'test': ["mock"]}
)
