from setuptools import setup, find_packages

setup(
    name='boussole',
    version=__import__('boussole').__version__,
    description=__import__('boussole').__doc__,
    long_description=open('README.rst').read(),
    author='David Thenon',
    author_email='sveetch@gmail.com',
    url='https://github.com/sveetch/boussole',
    license='MIT',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python',
        "Programming Language :: Python :: 2.7",
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[
        'click==5.1',
        'argh==0.24.1',
        'pathtools==0.1.2',
        'watchdog==0.8.3',
        'libsass==0.11.0',
    ],
    tests_require=[
        'pytest',
        'colorama',
        'sphinx>=1.6',
    ],
    entry_points={
        'console_scripts': [
            'boussole = boussole.cli.console_script:cli_frontend',
        ]
    },
    include_package_data=True,
    zip_safe=False
)