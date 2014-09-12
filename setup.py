from setuptools import setup, find_packages

setup(
    name='obachan',
    version='0.0.1',
    description='Server user management automation tool',
    # long_description=long_description,
    url='https://github.com/n10o/obachan',
    author='n10o',
    author_email='0x0082@gmail.com',
    license='MIT',
    packages=find_packages('.'),
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: System Administrators',
        'Topic :: System :: Systems Administration',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    entry_points={
        'console_scripts': [
            'obachan=obachan.main:main',
        ],
    },
)
