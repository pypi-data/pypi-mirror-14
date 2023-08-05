"""
TinyCert
--------

A wrapper library around TinyCert's v1 rest api.

API details (including your API key) can be found at https://www.tinycert.org/docs/api

Preferred method of use is via the provided ContextManager.
```````````````````````````````````````````````````````````

.. code:: python

    from tinycert import auto_session

    with auto_session(api_key, account, passphrase) as session:
        ca_list = session.ca.list()
        cert_list = session.cert.list(ca_list[0]['id'])

Or, connect and disconnect manually.
````````````````````````````````````

.. code:: python

    from tinycert import Session

    session = Session(api_key)
    session.connect(account, passphrase)
    ca_list = session.ca.list()
    cert_list = session.cert.list(ca_list[0]['id'])
    session.disconnect()

Links
`````

* `TinyCert <https://www.tinycert.org>`_
* `Home <https://github.com/chrisleck/tinycert>`_

"""
from setuptools import setup


VERSION = '0.1.1'

INSTALL_DEPS = [
    'enum34>=1.1.2',
    'requests>=2.9.1'
]

TEST_DEPS = [
    'mock>=1.3.0',
    'nose>=1.3.7',
    'pylint>=1.5.5',
    'requests-mock>=0.7.0'
]

setup(
    name='tinycert',
    version=VERSION,
    description='TinyCert v1 API wrapper',
    keywords='tinycert tiny cert x509 pki certificate authority',
    author='Christopher Eck',
    author_email='chrisleck@gmail.com',
    url='https://github.com/chrisleck/tinycert',
    bugtrack_url='https://github.com/chrisleck/tinycert/issues',
    license='MIT',
    long_description=__doc__,
    packages=['tinycert'],
    install_requires=INSTALL_DEPS,
    tests_require=TEST_DEPS,
    test_suite='nose.collector',
    platforms='any',
    zip_safe=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Security',
        'Topic :: Security :: Cryptography',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
