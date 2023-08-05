from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import sys
import re
import codecs


def read(*parts):
    # intentionally *not* adding an encoding option to open
    # see here: https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    return codecs.open(os.path.join(os.path.abspath(os.path.dirname(__file__)), *parts), 'r').read()

setup(name="kaching",
      version=read('VERSION').replace('\n', ''),
      description="Notification sounds for test pass and failure.",
      long_description=read('README.rst'),
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.1',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.3',
      ],
      keywords='tests sound effects notifications',
      author='Colm O\'Connor',
      author_email='colm.oconnor.github@gmail.com',
      url='https://github.com/crdoconnor/kaching',
      packages=find_packages(exclude=[]),
      entry_points=dict(console_scripts=['kaching=kaching:commandline',]),
      license='MIT',
      package=['kaching'],
      package_data={'kaching': ['pass/*.mp3', 'fail/*.mp3', 'start/*.mp3', ]},
      zip_safe=False,
)
