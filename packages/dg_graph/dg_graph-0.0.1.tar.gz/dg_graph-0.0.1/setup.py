from __future__ import print_function
from setuptools import setup
import os
import dg_graph

here = os.path.abspath(os.path.dirname(__file__))

long_description = '''Diggi graph traversal tool.'''

setup(
    name='dg_graph',
    version=dg_graph.__version__,
    url='https://bitbucket.org/serviciosveca/dg_graph',
    license='Apache Software License',
    author='Servicios VECA',
    install_requires=[
		'graph_db >= 0.*'
	],
    author_email='1josegomezr@gmail.com',
    description='dgGraph.',
    long_description=long_description,
    packages=['dg_graph'],
    include_package_data=True,
    platforms='any',
    keywords='graph database grafos',
    # test_suite='dg_graph.test.all',
    classifiers = []
)
