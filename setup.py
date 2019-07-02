from setuptools import setup

setup(
    name='dinero',
    version='0.1',
    description='API wrapper for Dinero (Danish accoutning service)',
    url='http://github.com/geanix/dinero',
    author='Geanix ApS',
    author_email='info@geanix.com',
    license='LGPL-2.1',
    packages=[
        'libdinero',
        'dinerocli',
    ],
    python_requires='>=3.7.0',
    install_requires=[
        'attrs',
        'requests',
        'requests-oauthlib',
        ],
    entry_points={
        'console_scripts': [
            'dinero = dinerocli.dinero:main',
        ],
    },
)
