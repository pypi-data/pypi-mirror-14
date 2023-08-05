###############################################################################
#
# The MIT License (MIT)
#
# Copyright (c) Tavendo GmbH
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
###############################################################################

from __future__ import absolute_import

import os
import re
import sys
import platform
from setuptools import setup
from setuptools.command.test import test as test_command

# remember if we already had six _before_ installation
try:
    import six  # noqa
    _HAD_SIX = True
except ImportError:
    _HAD_SIX = False

CPY = platform.python_implementation() == 'CPython'
PY3 = sys.version_info >= (3,)
PY33 = (3, 3) <= sys.version_info < (3, 4)

LONGSDESC = open('README.rst').read()

# get version string from "autobahn/__init__.py"
# See: http://stackoverflow.com/a/7071358/884770
#
VERSIONFILE = "autobahn/__init__.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = u['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))


# Autobahn core packages
#
packages = [
    'autobahn',
    'autobahn.wamp',
    'autobahn.wamp.test',
    'autobahn.websocket',
    'autobahn.websocket.test',
    'autobahn.asyncio',
    'autobahn.twisted',
    'twisted.plugins'
]

# Twisted dependencies (be careful bumping these minimal versions,
# as we make claims to support older Twisted!)
#
extras_require_twisted = [
    "zope.interface>=4.1.3", # Zope Public License
    "Twisted>=15.5"          # MIT license
]

# asyncio dependencies
#
if PY3:
    if PY33:
        # "Tulip"
        extras_require_asyncio = [
            "asyncio>=3.4.3"        # Apache 2.0
        ]
    else:
        # Python 3.4+ has asyncio builtin
        extras_require_asyncio = []
else:
    # backport of asyncio for Python 2
    extras_require_asyncio = [
        "trollius>=2.0",            # Apache 2.0
        "futures>=3.0.4"            # BSD license
    ]

# C-based WebSocket acceleration
#
if CPY and sys.platform != 'win32':
    # wsaccel does not provide wheels: https://github.com/methane/wsaccel/issues/12
    extras_require_accelerate = [
        "wsaccel>=0.6.2"            # Apache 2.0
    ]

    # ujson is broken on Windows (https://github.com/esnme/ultrajson/issues/184)
    if sys.platform != 'win32':
        extras_require_accelerate.append("ujson>=1.33")     # BSD license
else:
    extras_require_accelerate = []

# non-standard WebSocket compression support (FIXME: consider removing altogether)
# Ubuntu: sudo apt-get install libsnappy-dev
# lz4: do we need that anyway?
extras_require_compress = [
    "python-snappy>=0.5",       # BSD license
    "lz4>=0.7.0"                # BSD license
]

# non-JSON WAMP serialization support (namely MsgPack and CBOR)
#
extras_require_serialization = [
    "msgpack-python>=0.4.6",    # Apache 2.0 license
    "cbor>=0.1.24"              # Apache 2.0 license
]

# payload encryption
#
# enforce use of bundled libsodium
os.environ['SODIUM_INSTALL'] = 'bundled'
extras_require_encryption = [
    'pynacl>=1.0',              # Apache license
    'pytrie>=0.2',              # BSD license
    'pyqrcode>=1.1'             # BSD license
]

# everything
#
extras_require_all = extras_require_twisted + extras_require_asyncio + \
    extras_require_accelerate + extras_require_serialization + extras_require_encryption

# extras_require_all += extras_require_compress

# development dependencies
#
extras_require_dev = [
    # flake8 will install the version "it needs"
    # "pep8>=1.6.2",          # MIT license
    "pep8-naming>=0.3.3",   # MIT license
    "flake8>=2.5.1",        # MIT license
    "pyflakes>=1.0.0",      # MIT license
    "mock>=1.3.0",          # BSD license
    "pytest>=2.8.6",        # MIT license
    "unittest2>=1.1.0"      # BSD license
]

# for testing by users with "python setup.py test" (not Tox, which we use)
#
test_requirements = [
    "pytest>=2.8.6",        # MIT license
    "mock>=1.3.0"           # BSD license
]


# pytest integration for setuptools. see:
# http://pytest.org/latest/goodpractises.html#integration-with-setuptools-test-commands
# https://github.com/pyca/cryptography/pull/678/files
class PyTest(test_command):

    def finalize_options(self):
        test_command.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # Import here because in module scope the eggs are not loaded.
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


# Now install Autobahn ..
#
setup(
    name='autobahn',
    version=verstr,
    description='WebSocket client & server library, WAMP real-time framework',
    long_description=LONGSDESC,
    license='MIT License',
    author='Tavendo GmbH',
    author_email='autobahnws@googlegroups.com',
    url='http://autobahn.ws/python',
    platforms='Any',
    install_requires=[
        'six>=1.10.0',      # MIT license
        'txaio>=2.2.2',     # MIT license
    ],
    extras_require={
        'all': extras_require_all,
        'asyncio': extras_require_asyncio,
        'twisted': extras_require_twisted,
        'accelerate': extras_require_accelerate,
        'compress': extras_require_compress,
        'serialization': extras_require_serialization,
        'encryption': extras_require_encryption,
        'dev': extras_require_dev,
    },
    tests_require=test_requirements,
    cmdclass={'test': PyTest},
    packages=packages,
    zip_safe=False,
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    #
    classifiers=["License :: OSI Approved :: MIT License",
                 "Development Status :: 5 - Production/Stable",
                 "Environment :: No Input/Output (Daemon)",
                 "Framework :: Twisted",
                 "Intended Audience :: Developers",
                 "Operating System :: OS Independent",
                 "Programming Language :: Python",
                 "Programming Language :: Python :: 2",
                 "Programming Language :: Python :: 2.7",
                 "Programming Language :: Python :: 3",
                 "Programming Language :: Python :: 3.3",
                 "Programming Language :: Python :: 3.4",
                 "Programming Language :: Python :: 3.5",
                 "Programming Language :: Python :: Implementation :: CPython",
                 "Programming Language :: Python :: Implementation :: PyPy",
                 "Programming Language :: Python :: Implementation :: Jython",
                 "Topic :: Internet",
                 "Topic :: Internet :: WWW/HTTP",
                 "Topic :: Communications",
                 "Topic :: System :: Distributed Computing",
                 "Topic :: Software Development :: Libraries",
                 "Topic :: Software Development :: Libraries :: Python Modules",
                 "Topic :: Software Development :: Object Brokering"],
    keywords='autobahn autobahn.ws websocket realtime rfc6455 wamp rpc pubsub twisted asyncio'
)


try:
    from twisted.internet import reactor
    print("Twisted found (default reactor is {0})".format(reactor.__class__))
except ImportError:
    # the user doesn't have Twisted, so skip
    pass
else:
    # Make Twisted regenerate the dropin.cache, if possible. This is necessary
    # because in a site-wide install, dropin.cache cannot be rewritten by
    # normal users.
    if _HAD_SIX:
        # only proceed if we had had six already _before_ installing AutobahnPython,
        # since it produces errs/warns otherwise
        try:
            from twisted.plugin import IPlugin, getPlugins
            list(getPlugins(IPlugin))
        except Exception as e:
            print("Failed to update Twisted plugin cache: {0}".format(e))
        else:
            print("Twisted dropin.cache regenerated.")
    else:
        print("Warning: regenerate of Twisted dropin.cache skipped (can't run when six wasn't there before)")
