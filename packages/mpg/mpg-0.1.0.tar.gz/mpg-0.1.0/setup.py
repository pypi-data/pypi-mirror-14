# Copyright  2016  Kevin Murray <spam@kdmurray.id.au>
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from setuptools import setup
from setuptools.command.test import test as TestCommand
from Cython.Build import cythonize
import versioneer


# Inspired by the example at https://pytest.org/latest/goodpractises.html
class NoseCommand(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # Run nose ensuring that argv simulates running nosetests directly
        import nose
        nose.run_exit(argv=['nosetests'])


desc = """
MPG: Markov Process Generator of DNA sequences
"""

setup_requires = [
    'nose',
    'cython',
]

install_requires = [
    'docopt>=0.6',
    'screed>=0.9',
    'numpy',
    'scipy',
    'pyyaml',
]

test_requires = [
    'coverage>=3.7',
]

command_classes=versioneer.get_cmdclass()
command_classes['test'] =  NoseCommand

setup(
    name="mpg",
    packages=['mpg', ],
    version=versioneer.get_version(),
    entry_points={
        'console_scripts': [
            'mpg = mpg.main:mpg_main',
        ],
    },
    ext_modules=cythonize('mpg/_util.pyx'),
    cmdclass=command_classes,
    install_requires=install_requires,
    tests_require=test_requires,
    setup_requires=setup_requires,
    description=desc,
    author="Kevin Murray",
    author_email="spam@kdmurray.id.au",
    url="https://github.com/kdmurray91/mpg",
    keywords=[
        "bioinformatics",
        "Next-gen Sequencing",
    ],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        #TODO: add license
    ],
)
