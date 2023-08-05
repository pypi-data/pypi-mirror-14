from distutils.core import setup

from jsonschema_serialize_fork import __version__


with open("README.rst") as readme:
    long_description = readme.read()


classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.6",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.1",
    "Programming Language :: Python :: 3.2",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: Implementation :: CPython",
    "Programming Language :: Python :: Implementation :: PyPy",
]


setup(
    name="jsonschema_serialize_fork",
    version=__version__,
    packages=["jsonschema_serialize_fork", "jsonschema_serialize_fork.tests"],
    package_data={'jsonschema_serialize_fork': ['schemas/*.json']},
    author="Laurence Rowe, Julian Berman",
    author_email="laurence@lrowe.co.uk",
    classifiers=classifiers,
    description="Fork of Julian Berman's jsonschema to include support for serializing defaults",
    license="MIT",
    long_description=long_description,
    url="http://github.com/lrowe/jsonschema_serialize_fork",
)
