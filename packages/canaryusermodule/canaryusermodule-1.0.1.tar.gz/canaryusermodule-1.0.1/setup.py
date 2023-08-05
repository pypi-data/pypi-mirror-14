from setuptools import setup, find_packages

setup(
    name='canaryusermodule',
    version='1.0.1',
    url='http://www.thinkst.com/',
    author='Thinkst Applied Research',
    author_email='info@thinkst.com',
    description='Generate Thinkst Canary user modules',
    install_requires=[
        'Jinja>=1.2',
        'pip>=8.0.0',
        'opencanary>=0.3.1'
    ],
    setup_requires=[
        'setuptools_git'
    ],
    packages = find_packages(exclude="test"),
    entry_points = {
        'console_scripts': [
            'usermodgen = canaryusermodule.usermodgen:main'
        ]
    },
    platforms='any',
    include_package_data=True,
)
