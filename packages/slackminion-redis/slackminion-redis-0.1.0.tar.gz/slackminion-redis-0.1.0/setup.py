from setuptools import setup, find_packages

from slackminion.plugins.state_redis import version

setup(
        name='slackminion-redis',
        version=version,
        packages=find_packages(exclude=['test_plugins']),
        url='https://github.com/arcticfoxnv/slackminion-redis',
        license='MIT',
        author='Nick King',
        author_email='',
        description='Provides a redis state handler for slackminion',
        install_requires=[
            'redis',
            'slackminion',
        ],
        classifiers=[
            "Programming Language :: Python",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Development Status :: 2 - Pre-Alpha",
            "Topic :: Communications :: Chat",
        ]
)
