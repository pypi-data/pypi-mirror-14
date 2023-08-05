Python Bindings for CloudCIX API
================================

Python bindings and utils to make the work with CloudCIX API fun and
easy.

`API Docs <https://docs.cloudcix.com>`__

CloudCIX is developed by `CIX <http://www.cix.ie>`__

Requirements
------------

-  `CloudCIX Account <https://auth.cloudcix.com/register/>`__
-  `CloudCIX Account's Member
   ID <https://saas.cloudcix.com/membership/setup/account/member/>`__
   under Member ID
-  `Python
   2.7.x <http://docs.python-guide.org/en/latest/starting/installation/>`__
-  `pip <https://pip.pypa.io/en/stable/installing/>`__ or download
   `zip <https://github.com/CloudCIX/cloudcix-python/releases/download/v0.1.4/cloudcix.zip>`__

*It is crucial that you install Python 2.7, this library was not
designed for use with Python 3+.*

Pre Installation with pip
-------------------------

Download
`get-pip.py <https://raw.githubusercontent.com/pypa/pip/master/contrib/get-pip.py>`__
and run

::

    python get-pip.py

Installation
------------

With pip:

::

    pip install -U cloudcix

Without pip \* download
`this <https://github.com/CloudCIX/cloudcix-python/releases/download/v0.1.4/cloudcix.zip>`__
\* extract to your project folder \* open a new python file and add the
settings described below:

Required settings
-----------------

When you run your project you should set the settings variable
``CLOUDCIX_SETTINGS_MODULE`` to point to the module that contains the
settings object.

ENV Based Settings (Basic)
~~~~~~~~~~~~~~~~~~~~~~~~~~

As an alternative when used from ``console`` the settings can be set as
environment variables.

.. code:: python

    os.environ['CLOUDCIX_SERVER_URL'] = 'https://api.cloudcix.com/'
    # utils method get_admin_token and get_admin_session, will require you to set
    # following environment variables as well
    os.environ['CLOUDCIX_API_USERNAME'] = 'EMAIL'     # CloudCIX login
    os.environ['CLOUDCIX_API_PASSWORD'] = 'PASSWORD'  # CloudCIX password
    os.environ['CLOUDCIX_API_ID_MEMBER'] = 'NUMBER'   # CloudCIX Member ID (see Requirements)
    os.environ['OPENSTACK_KEYSTONE_URL'] = 'https://keystone.cloudcix.com:5000/v3'

Module Based Settings (Advanced)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    # In main python script
    import os
    os.environ.setdefault("CLOUDCIX_SETTINGS_MODULE", "my_project.my_settings")

.. code:: python

    # In my_project/my_settings.py
    CLOUDCIX_SERVER_URL = 'https://api.cloudcix.com'
    CLOUDCIX_API_USERNAME = 'EMAIL'     # CloudCIX login
    CLOUDCIX_API_PASSWORD = 'PASSWORD'  # CloudCIX password
    CLOUDCIX_API_ID_MEMBER = 'NUMBER'   # CloudCIX Member ID (see Requirements)
    OPENSTACK_KEYSTONE_URL = 'https://keystone.cloudcix.com:5000/v3'

Django Settings (Advanced)
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    # In settings.py
    INSTALLED_APPS = (
      ...
      'django_cloudcix'
    )

    CLOUDCIX_SERVER_URL = 'https://api.cloudcix.com'
    CLOUDCIX_API_USERNAME = 'EMAIL'     # CloudCIX login
    CLOUDCIX_API_PASSWORD = 'PASSWORD'  # CloudCIX password
    CLOUDCIX_API_ID_MEMBER = 'NUMBER'   # CloudCIX Member ID (see Requirements)
    OPENSTACK_KEYSTONE_URL = 'https://keystone.cloudcix.com:5000/v3'

Sample usage
------------

Use the language service
~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    import os

    os.environ['CLOUDCIX_SERVER_URL'] = 'https://api.cloudcix.com'
    os.environ['CLOUDCIX_API_USERNAME'] = 'EMAIL'
    os.environ['CLOUDCIX_API_PASSWORD'] = 'PASSWORD'
    os.environ['CLOUDCIX_API_ID_MEMBER'] = 'NUMBER'
    os.environ['OPENSTACK_KEYSTONE_URL'] = 'https://keystone.cloudcix.com:5000/v3'

    # NOTE: environ variables must be set before importing cloudcix

    from cloudcix import api
    from cloudcix.utils import get_admin_session

    token = get_admin_session().get_token()
    response = api.membership.language.list(token=token)

    print response.json()

More Examples
-------------

see ``examples`` folder for more.
