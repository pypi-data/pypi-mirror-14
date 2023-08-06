from setuptools import setup

setup(name='dpassgen',
      version='1.2',
      description='Generate passwords based on system dict, https://xkcd.com/936/',
      url='https://xkcd.com/936/',
      author='John Dulaney',
      author_email='jdulaney@fedoraproject.org',
      license='GPLv3',
      packages=['dpassgen'],
      entry_points={
          'console_scripts': [
              'dpassgen=dpassgen:dpassgen_cli'
          ]
      }
)
