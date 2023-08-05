from setuptools import setup, find_packages

requirements = [
    'docker-py >= 1.7.0',
    'python-vagrant >= 0.5.11'
]

setup_requirements = [
    'flake8'
]

name = 'presto-docker-devenv'

setup(
    name=name,
    version='0.2',
    description='Presto docker developer environment.',
    author='Grzegorz Kokosinski',
    author_email='grzegorz.kokosinski a) teradata.com',
    keywords='presto docker developer environmnent',
    url='https://github.com/kokosing/git-gifi',
    include_package_data=True,
    packages=find_packages(),
    package_dir={'devenv': 'devenv'},
    install_requires=requirements,
    setup_requires=setup_requirements,
    entry_points={'console_scripts': ['presto-devenv = devenv.devenv:main']}
)
