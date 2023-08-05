import os
from distutils.core import setup

version = '0.1'
README = os.path.join(os.path.dirname(__file__), 'README.md')
long_description = open(README).read()
setup(name='yt_interaction',
      version=version,
      description=("Interaction in yt via HoloViews"),
      long_description=long_description,
      classifiers=[
          "Programming Language :: Python",
          ("Topic :: Software Development :: Libraries :: Python Modules"),
      ],
      keywords='data',
      author='Matthew Turk <matthewturk@gmail.com>',
      license='BSD',
      package_dir={'yt_interaction':'yt_interaction'},
      packages=["yt_interaction"],
      install_requires=["holoviews"],
      url="http://bitbucket.org/data-exp-lab/yt_interaction/",
      author_email="matthewturk@gmail.com",
)
