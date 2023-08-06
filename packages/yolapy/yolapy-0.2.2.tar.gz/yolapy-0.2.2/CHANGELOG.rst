0.2.2 (2016-04-06)
------------------

* Add ``Site.is_published``

0.2.1 (2016-03-31)
------------------

* Add ``Site.list``

0.2.0 (2016-03-29)
------------------

* ``Yola.create_subscription`` now returns the created subscription.
* **Breaking change:** Remove ``Yola.suspend_user`` and ``Yola.resume_user``.
* Add a ``Site`` model.

0.1.7 (2015-12-02)
------------------

* Update Subscription model to include all attributes returned from the API.

0.1.6 (2015-12-01)
------------------

* Update installation requirements (demands)
* Support Python 3


0.1.5 (2015-11-23)
------------------

* Return values from ``change_subscription_type`` and ``activate_trial_subscription``
  methods.
* Fixed failing integration tests.


0.1.4 (2015-11-19)
------------------

* Add Subscription model

0.1.3 (2015-10-19)
------------------

* Add a Partner model


0.1.2 (2015-10-15)
------------------

* Add a configuration module
* Add a User model
* Add Sphinx Docs - http://yolapy.readthedocs.org/


0.1.1 (2015-09-11)
------------------

* Update installation requirements


0.1.0 (2015-09-02)
------------------

* Initial version with ``Yola`` wrapper for the Yola API
