import sys

from setup_helpers import require_python, get_version, long_description
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


require_python(50659568)
__version__ = get_version('blackhole/__init__.py')

desc = """Blackhole is an MTA (message transfer agent) that (figuratively)
pipes all mail to /dev/null."""


class PyTest(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = [
            '--doctest-modules', '--verbose',
            './blackhole', './tests'
        ]
        self.test_suite = True

    def run_tests(self):
        import pytest
        sys.exit(pytest.main(self.test_args))


entry_points = {
    'console_scripts': [
        'blackhole = blackhole.application:run',
    ]
}

tests_require = [
    'pytest',
    'pytest-asyncio'
]


setup(name='blackhole',
      version=__version__,
      url='https://blackhole.io/',
      author='Kura',
      author_email='kura@kura.io',
      maintainer='Kura',
      maintainer_email='kura@kura.io',
      description=desc,
      long_description=long_description('README.rst'),
      license=long_description('LICENSE'),
      platforms=['linux'],
      packages=find_packages(exclude=["*.tests"]),
      install_requires=[],
      tests_require=tests_require,
      cmdclass={'test': PyTest},
      entry_points=entry_points,
      classifiers=[
         'Programming Language :: Python :: 3.5',
         'Environment :: Console',
         'Topic :: Internet',
         'Topic :: Utilities',
         'Topic :: Communications :: Email',
         'Topic :: Communications :: Email :: Mail Transport Agents',
         'Topic :: Software Development :: Testing',
         'Topic :: Software Development :: Testing :: Traffic Generation',
         'Topic :: Software Development',
         'Topic :: System :: Networking',
         'Intended Audience :: Developers',
         'License :: OSI Approved :: MIT License',
      ],
      )
