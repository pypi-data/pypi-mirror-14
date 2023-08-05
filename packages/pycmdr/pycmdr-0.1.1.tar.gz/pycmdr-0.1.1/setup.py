from os.path import dirname, join
from setuptools import setup

author_email = 'acsherrock@gmail.com'
base_path = dirname(__file__)
readme_path = join(base_path, 'README.md')
requirements_path = join(base_path, 'requirements.txt')

description = 'A simple python library for easily creating command line applications, use Python\'s decorators to manage subcommands and positional and optional arguments.'
long_description = description
requirements = []

try:
    with open(readme_path) as f:
        readme = f.read()
except IOError:
    print('Could not find readme, long description will be set to the short description.')
else:
    long_description = readme

try:
    with open(requirements_path) as f:
        for line in f.readline():
            requirements.append(line)
except IOError:
    print('requirements.txt not found in', base_path, 'please email me at', author_email, 'to resolve issues.')


setup(
    name='pycmdr',
    version='0.1.1',
    packages=['cmdr'],
    include_package_data=True,
    url='https://bitbucket.org/aquilleph/cmdr',
    license='GPL',
    author='Aquilleph',
    author_email=author_email,
    description=description,
    long_description=long_description,
    keywords='console cli program app manager subcommands cmd',
    install_requires=requirements,
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4'
    ]

    # entry_points={
    #     'console_scripts': [
    #         'cmdr = cmdr:main',
    #     ]
    # }
)