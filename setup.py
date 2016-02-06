from setuptools import setup, find_packages


setup(
    name='brew',
    version='0.0.1',
    packages=find_packages(),
    zip_safe=False,
    entry_points={
        'console_scripts': ['brew=source.brew:brew'],
    }
)
