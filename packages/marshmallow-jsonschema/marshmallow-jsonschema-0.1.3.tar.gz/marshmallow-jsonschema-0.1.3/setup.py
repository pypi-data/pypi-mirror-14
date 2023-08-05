import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='marshmallow-jsonschema',
    version='0.1.3',
    description='JSON Schema Draft v4 (http://json-schema.org/) formatting with marshmallow',
    long_description=read('README.md'),
    author='Stephen Fuhry',
    author_email='fuhrysteve@gmail.com',
    url='https://github.com/fuhrysteve/marshmallow-jsonschema',
    packages=find_packages(exclude=("test*", )),
    package_dir={'marshmallow-jsonschema': 'marshmallow-jsonschema'},
    include_package_data=True,
    install_requires=['marshmallow>=2.3.0'],
    tests_require=['pytest>=2.1', 'jsonschema', 'strict-rfc3339'],
    license=read('LICENSE'),
    zip_safe=False,
    keywords=('marshmallow-jsonschema marshmallow schema serialization '
              'jsonschema validation'),
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests'
)
