=============================
django-pj-portfolio
=============================

.. image:: https://badge.fury.io/py/django-pj-portfolio.png
    :target: https://badge.fury.io/py/django-pj-portfolio

.. image:: https://travis-ci.org/jokimies/django-pj-portfolio.png?branch=master
    :target: https://travis-ci.org/jokimies/django-pj-portfolio

.. image:: https://codecov.io/github/jokimies/django-pj-portfolio/coverage.svg?branch=master
    :target: https://codecov.io/github/jokimies/django-pj-portfolio?branch=master


Portfolio tracking

Documentation
-------------

The full documentation is at
https://django-pj-portfolio.readthedocs.org. (at some point) 

Quickstart
----------

Install django-pj-portfolio::

    pip install django-pj-portfolio

Then to use it in a project, add `portfolio` into ``INTALLED_APPS``::

  INSTALLED_APPS = (
  ....
  'portfolio',
  )

And apply the migrations::

  python manage.py migrate


Configure `urls`, add to main `urls.py`::

  ...
  url(r'^portfolio/', include('portfolio.urls')),
  ...


Update price trackers (for updating the prices)::

  python manage update_price_trackers

For daily price tracking, `update_share_prices` can be used::

  python manage update_price_values

Updates prices once per day (even if run multiple times a day, the first
price only is taken in to account)


Features
--------

* TODO

Cookiecutter Tools Used in Making This Package
----------------------------------------------

*  cookiecutter
*  cookiecutter-djangopackage




v1.1.1 (2016-03-06)
-------------------

New features
~~~~~~~~~~~~

- *summary detail*: Flash changed prices. [Petri Jokimies]




Other
~~~~~

- *account summary*: Use latest date from Google Finance. [Petri
  Jokimies]




- *account summary*: Sort table using Angular's orderBy. [Petri
  Jokimies]








- *securities service*: Use smaller number of mocked results. [Petri
  Jokimies]




- *gulp*: Output results in separate directory. [Petri Jokimies]




- *account summary*: $timeout parameters changed in 1.4.x. [Petri
  Jokimies]






- *account summary*: More tests. [Petri Jokimies]

- *position service*: Test for google_quote. [Petri Jokimies]

- *karma conf*: Run coverage. [Petri Jokimies]

v1.1.0 (2016-02-16)
-------------------

New features
~~~~~~~~~~~~

- *account summary*: Use correct currency in calculations, use spinner.
  [Petri Jokimies]
















- *account summary*: Added market value calculation. [Petri Jokimies]

- *account summary*: Display live values. [Petri Jokimies]

- *account summary*: Count total market value. [Petri Jokimies]

- *account summary*: Initial price live updates. [Petri Jokimies]




- Added API to get list of holdings. [Petri Jokimies]

Other
~~~~~

- More files to watch in karma.conf. [Petri Jokimies]

- Added test for Angular currency service. [Petri Jokimies]

- *karma*: Using jasmine-query for fixtures. [Petri Jokimies]

- *gulp*: First gulp tasks. [Petri Jokimies]

- *account summary*: Removed unnecessary DB queries. [Petri Jokimies]




- *account*: Make AccountBase more usable. [Petri Jokimies]




v1.0.1 (2016-01-15)
-------------------

Fix
~~~

- *requirements*: Specific about Django version. [Petri Jokimies]







Other
~~~~~

- *update prices*: Adapt to KL's new web page. [Petri Jokimies]

v1.0.0 (2015-11-30)
-------------------

New features
~~~~~~~~~~~~

- Add management commands to update prices. [Petri Jokimies]




Refactor
~~~~~~~~

- *test*: Security test and factories separeted. [Petri Jokimies]

- *test*: Price tests and factories sepateted. [Petri Jokimies]

Documentation
~~~~~~~~~~~~~

- Added comments for management commads. [Petri Jokimies]

v0.1.0 (2015-09-25)
-------------------

- Initial commit. [Petri Jokimies]


