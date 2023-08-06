try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

with open("README.rst", 'r') as readme:
    README_txt = readme.read()

with open("CHANGELOG.rst", 'r') as changelog:
    README_txt += changelog.read()

dependencies = [
    'pyexcel>=0.2.0',
    'tabulate>=0.7.4',
]

extras = {}


setup(
    name='pyexcel-text',
    author='C.W.',
    version='0.2.0',
    author_email='wangc_2011 (at) hotmail.com',
    url='https://github.com/pyexcel/pyexcel-text',
    description='A plugin to pyexcel and provides the capbility to present and write data in text fromats',
    install_requires=dependencies,
    extras_require=extras,
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    long_description=README_txt,
    zip_safe=False,
    tests_require=['nose'],
    keywords=[
        'excel',
        'python',
        'pyexcel',
        "plain",
        "simple",
        "grid",
        "pipe",
        "orgtbl",
        "rst",
        "mediawiki",
        "latex",
        "latex_booktabs",
        "json"
    ],
    license='New BSD',
    classifiers=[
        'Topic :: Office/Business',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Developers',
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: PyPy'
    ]
)