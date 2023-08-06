from setuptools import setup, find_packages

packages = find_packages(exclude=['tests'])
requires = [
    'betamax >= 0.3.2',
]

extra_requires = {
    'yaml11':  ["PyYAML"]
}

try:
    from betamax_serializers import __version__
except ImportError:
    __version__ = ''

if not __version__:
    raise RuntimeError('Cannot import version information')


def data_for(filename):
    with open(filename) as fd:
        content = fd.read()
    return content

setup(
    name="betamax-serializers",
    version=__version__,
    description="A set of third-party serializers for Betamax",
    long_description="\n\n".join([data_for("README.rst"),
                                  data_for("HISTORY.rst")]),
    license=data_for('LICENSE'),
    author="Ian Cordasco",
    author_email="graffatcolmingov@gmail.com",
    url="https://gitlab.com/betamax/serializers",
    packages=packages,
    package_data={'': ['LICENSE', 'AUTHORS.rst']},
    include_package_data=True,
    install_requires=requires,
    extras_require=extra_requires,
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
    ]
)
