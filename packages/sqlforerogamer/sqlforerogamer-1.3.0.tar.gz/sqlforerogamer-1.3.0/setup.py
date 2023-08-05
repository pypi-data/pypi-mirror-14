from setuptools import setup, find_packages
from os import path
import subprocess

here = path.abspath(path.dirname(__file__))
subprocess.call('pandoc {0}/README.md -s -o {0}/README.rst'
                .format(here), shell=True)
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='sqlforerogamer',
    version='1.3.0',
    description='A library for http://erogamescape.dyndns.org/~ap2/ero/toukei_kaiseki/sql_for_erogamer_index.php',
    long_description=long_description,
    url='http://github.com/roronya/sqlforerogamer',
    author='roronya',
    author_email='roronya628@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    keywords='erogame sql',
    packages=find_packages(exclude=['tests*']),
    install_requires=['requests', 'beautifulsoup4'],
)
