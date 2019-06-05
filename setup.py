from setuptools import find_packages, setup
setup(
    name='dock',
    version='0.0.45',
    packages=find_packages(),
    install_requires=['fire>=0.1.3', 'sh>=1.12.14'],
    package_data={'': ['LICENSE.txt', 'README.md']},
    include_package_data=True,
    entry_points={
        'console_scripts': ['dock=dock.app:main'],
    }
)
