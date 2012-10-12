from setuptools import setup
from setuptools import find_packages


version = '1.0'
tests_require = [
    'zope.configuration',
    'zope.publisher',
    'zope.traversing',
    'zope.interface',
    'zope.schema',
    ]

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
        'martian',
        'grokcore.component',
        'grokcore.security',
        'zope.component',
        'plone.tiles>=1.1',
        'five.grok',
        'zope.deferredimport',
        ],
    tests_require=tests_require,
    extras_require=dict(test=tests_require),
    )
