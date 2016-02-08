from setuptools import setup, find_packages


setup(
    name='weld',
    version='0.1',
    packages=find_packages(),
    zip_safe=False,
    license="MIT",
    install_requires=['sqlalchemy', 'click', 'pipe'],
    entry_points={
        'console_scripts': ['weld=source.weld:weld'],
    }
)
