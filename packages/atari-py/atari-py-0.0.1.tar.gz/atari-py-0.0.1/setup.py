import os
from setuptools import setup
import subprocess
from distutils.command.build import build as DistutilsBuild

with open(os.path.join(os.path.dirname(__file__), 'package_data.txt')) as f:
    package_data = [line.rstrip() for line in f.readlines()]

class Build(DistutilsBuild):
    def run(self):
        subprocess.check_call(['make', 'build', '-C', 'atari_py/ale_interface'])
        DistutilsBuild.run(self)

setup(name='atari-py',
      version='0.0.1',
      description='Python bindings to Atari games',
      url='https://github.com/rl-gym/atari-py',
      author='OpenAI',
      author_email='info@openai.com',
      license='',
      packages=['atari_py'],
      package_data={'atari_py': package_data},
      cmdclass={'build': Build},
      tests_require=['nose2']
)
