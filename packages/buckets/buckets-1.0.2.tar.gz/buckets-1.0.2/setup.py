from setuptools import setup, find_packages

with open('README.md') as fhandle:
    long_description = fhandle.read()


setup(
    name='buckets',
    version='1.0.2',
    description='managing data by relevancy.',
    long_description=long_description,
    url="https://github.com/bdastur/spam",
    author="Behzad Dastur",
    author_email="bdastur@gmail.com",
    license='Apache Software License',
    classifier=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Intended Audience :: Developers',
        'License :: Apache Software License',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
    ],

    keywords='buckets utility ',
    py_modules=['buckets']
)

