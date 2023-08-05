Django generate-secret-key application
======================================

.. image:: https://badge.fury.io/py/django_generate_secret_key.svg

Simple Django application that adds a new command:

.. code:: bash

    python manage.py generate_secret_key [--replace] [secretkey.txt]

This will generate a new file ``secretkey.txt`` containing a random Django secret
key. In your production settings file, replace the hardcoded key by:

.. code:: python

    # Use a separate file for the secret key
    with open('/path/to/the/secretkey.txt') as f:
        SECRET_KEY = f.read().strip()

You can avoid hardcoding the path of the key by using:

.. code:: python

    import os
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))

    # Use a separate file for the secret key
    with open(os.path.join(BASE_DIR, 'secretkey.txt')) as f:
        SECRET_KEY = f.read().strip()
