from sys import version_info
import os
# Prevent spurious errors during `python setup.py test` in 2.6, a la
# http://www.eby-sarna.com/pipermail/peak/2010-May/003357.html:
try:
    import multiprocessing
except ImportError:
    pass

from setuptools import setup, find_packages

def read(fname):
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
setup(
    name='mzbench_api_client',
    version='0.1.12',
    description='MZBench client lib',
    long_description='A wrapper-library for MZBench',
    author='Machine Zone',
    author_email='info@machinezone.com',
    license='BSD',
    packages=find_packages(exclude=['ez_setup']),
    install_requires=['requests>=2.6.0', 'docopt', 'erl_terms'],
    tests_require=['nose'],
    test_suite='nose.collector',
    url='https://github.com/machinezone/mzbench',
    include_package_data=True,
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Development Status :: 2 - Pre-Alpha',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Topic :: Software Development :: Libraries',
        'Topic :: Text Processing :: General'],
    keywords=['testing', 'mzbench', 'api', 'http'],
    entry_points={
        'console_scripts': [
            'mzbench = mzbench_api_client.mzbench:main'
        ],
    },
    use_2to3=version_info >= (3,)
)
