from setuptools import setup, find_packages

from slackminion.plugins.state_mysql import version

setup(
        name='slackminion-mysql',
        version=version,
        packages=find_packages(exclude=['test_plugins']),
        url='https://github.com/arcticfoxnv/slackminion-mysql',
        license='MIT',
        author='Nick King',
        author_email='',
        description='Provides a MySQL state handler for slackminion',
        install_requires=[
            'MySQL-python',
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
