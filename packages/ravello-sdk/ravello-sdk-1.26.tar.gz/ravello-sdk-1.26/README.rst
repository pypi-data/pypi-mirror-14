Ravello Python SDK
==================

This is a micro-SDK for accessing the Ravello_ API in Python. It also contains
a few useful utility scripts.

Installation
------------

Installation from the Python Package Index::

 $ pip install ravello-sdk

Installation from source::

 $ python setup.py install

Running the tests
-----------------

Run the unit tests on your current Python version::

 $ python tests/unit.py

Run the integration tests on your current Python version::

 $ cp test.conf.in test.conf
 # edit test.conf and follow the comments
 $ python tests/integration.py

Run all tests on all supported Python versions::

 $ tox

Examples
-------

Various usage examples exist for the SDK (credit goes to the relevant contributers):

* *Ravshello* is an almost complete shell to manage Ravello using the Python SDK -  https://github.com/ryran/ravshello
* The *ravello-create-nodes* utility supports various ways for creating applications from disk images - https://github.com/ravello/python-sdk/blob/master/tools/ravello-create-nodes
* A cool example for implementing a highly available load balancer on top of Ravello using the Python SDK - https://gist.github.com/robertoandrade/29e60d41aee6342c16c7
* A simple script for adding VMs to a published application - https://github.com/ravello/vmware-automation 

The following shows a small example of how to use the SDK::

 from ravello_sdk import *
 client = RavelloClient()
 client.login('username', 'Passw0rd')
 for app in client.get_applications():
     print('Found Application: {0}'.format(app['name']))

Source Code
-----------

The source code for this project is on Github_.

License
-------

The Ravello Python SDK is licensed under the Apache 2.0 license.

.. _Ravello: http://www.ravellosystems.com
.. _Github: https://github.com/ravello/python-sdk
