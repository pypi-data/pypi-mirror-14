from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

setup(name='flavio',
      version='0.1.2',
      author='David M. Straub',
      author_email='david.straub@tum.de',
      url='https://flav-io.github.io',
      description='A Python package for flavour physics phenomenology in the Standard Model and beyond',
      long_description="""``flavio`` is a package to compute observables in flavour physics
      both within the Standard Model of particle physics and in the presence of new
      physics encoded in Wilson coefficients of local dimension-6 operators.
      Observables implemented include rare B meson decays and meson-antimeson
      mixing.""",
      license='MIT',
      packages=find_packages(),
      package_data={
      'flavio':['data/*',
                'physics/data/arXiv-1503-05534v1/*','physics/data/arXiv-1501-00367v2/*']
      },
      install_requires=['numpy', 'scipy', 'setuptools>=3.3', 'pyyaml'],
      extras_require={
            'testing': ['nose'],
            'plotting': ['matplotlib'],
            'sampling': ['pypmc', 'emcee']},
    )
