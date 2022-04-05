"""General setup for module."""

from setuptools import setup, find_packages

VERSION = "netplotbrain/__version.py"
VERSION = open(VERSION, "rt").read()
VERSION = VERSION.split('"')[1]

setup(name='netplotbrain',
      version=VERSION,
      python_requires='>3.5',
      setup_requires=['pytest-runner'],
      tests_require=['pytest'],
      license='GNU V3',
      install_requires=[
                        'matplotlib>=3.3.3',
                        'nibabel>=3.1.0',
                        'templateflow>=0.6.3',
                        'numpy>=1.18.1',
                        'scipy>=1.4.1',
        ],
      package_data={'': ['./netplotbrain/profiles']},
      include_package_data=True,
      description='Package to plot networks on brains',
      packages=find_packages(),
      author='wiheto, silviafan',
      author_email='william.thompson@gu.se',
      url='https://www.github.com/wiheto/netplotbrain',

      long_description='netplotbrain. \
            Plotting networks on neuroimaging files, \
            nodes and edges can be plotted onto 3D brains. \
            ')