Yola API Python Client
======================

.. image:: https://travis-ci.org/yola/yolapy.svg?branch=master
    :target: https://travis-ci.org/yola/yolapy

Usage
-----

.. code:: python

    # settings file

    from yolapy.configuration import configure

    configure(
        auth=('username', 'password'),
        url='https://wl.qa.yola.net/',
    )

    # application code

    from yolapy.models import User as YolaUser

    yola_user = YolaUser(
        email='test@example.com',
        name='Jane',
        surname='Doe',
        partner_id='WL_YOLA',
        preferences={'name': 'value'})
    yola_user.save()

See http://yolapy.readthedocs.org/ for available methods with
documentation.

Development
-----------

To run the tests::

    $ nosetests

Integration tests are not run by default. To run them, you must set up an
integration environment and edit the test settings::

    $ cp tests/test_integration/test_settings.py.sample \
         tests/test_integration/test_settings.py

**Note:** Try not to run the tests agains the Yola QA environment. It gets
used for manual testing and we don't want to clutter it up with users created
in automated test runs.

Then you can run the integration tests explicitly::

    $ nosetests tests/test_integration

To test and lint your code automatically when you make changes::

    $ cp tube.py.sample tube.py
    $ stir

To open a REPL with a `Yola` client initialized with your `test_settings`::

    $ python -i shell.py

Documentation
-------------

Changes to the public interface should be documented. See the `docs` directory.

Pushes to the `master` branch build at http://yolapy.readthedocs.org/en/latest/
automatically.

You can test your doc changes locally with::

    $ cd docs
    $ make html
    $ open _build/html/index.html
