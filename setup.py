from setuptools import setup, find_packages

setup(
    name='payid_validator',
    version='0.2',
    description='A robust payId syntax and usability validation library for Python 3.x.',
    long_description=open("README.md", encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url='https://github.com/RockHoward/python-payid-validator',

    author=u'Rock Howard',
    author_email=u'rock@rockhoward.com',
    license='Apache License 2.0',

    # See https://pypi.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],

    keywords="payid validator",

    packages=find_packages(),
    # install_requires=[
    #     "idna>=2.0.0",
    #     "dnspython>=1.15.0"
    # ],
    #
    # entry_points={
    #     'console_scripts': [
    #         'payid_validator=payid_validator:main',
    #     ],
    # },
)