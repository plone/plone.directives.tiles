from setuptools import setup, find_packages
import os

version = '1.0a1'

setup(name='plone.directives.tiles',
      version=version,
      description="Grokkers for plone.tiles",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='plone tiles deco blocks grok directives',
      author='Martin Aspeli',
      author_email='optilude@gmail.com',
      url='http://pypi.python.org/pypi/plone.app.tiles',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['plone', 'plone.directives'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'five.grok',
          'zope.deferredimport',
          'grokcore.component',
          'grokcore.view',
          'grokcore.security',
          'plone.tiles',
      ],
      entry_points="""
      """,
      )
