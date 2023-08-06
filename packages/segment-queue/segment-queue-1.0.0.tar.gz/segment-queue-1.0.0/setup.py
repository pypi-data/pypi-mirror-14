"""
Wrap Segment's python library to use Redis as the queue.
"""
from setuptools import find_packages, setup

dependencies = [
    'analytics-python',
    'click',
    'python-dateutil',
    'redis',
]

setup(
    name='segment-queue',
    version='1.0.0',
    url='https://github.com/gitprime/segment-queue',
    author='George Hickman',
    author_email='george@ghickman.co.uk',
    description='Wrap Segment\'s python library to use Redis as the queue',
    license='MIT',
    long_description=__doc__,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=dependencies,
    entry_points={
        'console_scripts': [
            'send-segment-events = segment.cli:main',
        ],
    },
)
