from setuptools import find_packages
from setuptools import setup
import json

package_json = json.load(open('package.json'))
version = package_json['version']

setup(
    name='mockup-highlightjs',
    version=version,
    description="Extension to Mockup's patterns.",
    long_description='{0}\n{1}'.format(
        open("README.rst").read(),
        open("CHANGES.rst").read(),
    ),
    classifiers=[
	"Environment :: Web Environment",
        "Framework :: Plone",
	"Framework :: Plone :: 5.0",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='plone mockup',
    author='Rene´ Jochum',
    author_email='rene@jochums.at',
    url='https://github.com/collective/mockup-highlightjs',
    license='BSD',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'plone.resource',
    ],
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
