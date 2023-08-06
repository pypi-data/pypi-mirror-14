from setuptools import setup, find_packages

setup(
    name='tomb_cli_testapps',
    packages=find_packages(),
    entry_points={
        'paste.app_factory': [
            'main=tomb_cli_testapps:simple',
        ],
    }
)
