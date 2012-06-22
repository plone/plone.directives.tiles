from setuptools import setup
from setuptools import find_packages


version = '1.0'

setup(
    name='plone.directives.tiles',
    version=version,
    description="Grokkers for plone.tiles",
    long_description=open("README.rst").read(),
    classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
    keywords='plone tiles deco blocks grok directives',
    author='Martin Aspeli',
    author_email='optilude@gmail.com',
    url='https://github.com/plone/plone.directives.tiles',
    license='GPL',
    packages=find_packages(),
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
    )
