import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'event_bus'))
from version import VERSION

long_description = '''
event_bus_python provide fluent interface for event emition with python
applications.
'''

install_requires = [
    "requests>=2.18,<3.0",
    "six>=1.11",
    "PyJWT>=2.0.0",
    "python-dateutil>=2.6"
]

setup(
    name='event_bus_python',
    version=VERSION,
    url='https://github.com/intellihr/event_bus_python',
    author='intellihr',
    author_email='admin@intellihr.com.au',
    maintainer='intellihr',
    test_suite='analytics.test.all',
    packages=['event_bus'],
    install_requires=install_requires,
    description='intellihr event bus client for python applications',
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ]
)
