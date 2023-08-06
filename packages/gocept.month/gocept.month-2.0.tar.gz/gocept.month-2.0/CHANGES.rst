CHANGES
=======

2.0 (2016-04-28)
----------------

- Made the package compatible with Python 2.7 and Python 3 at the same time.

- Backwards-incompatible change towards stricter comparison behaviour: While
  arbitrary objects (except month strings) used to be considered less than any
  ``Month`` instance, such a comparison now raises a ``TypeError``.

- Removed deprecated ``Month.isBetween`` method.


1.5 (2016-04-27)
----------------

- Support Python 2.7 and PyPy only.

- Add tox as testrunner.


1.4 (2016-02-07)
----------------

- Add a ``__len__`` method to `MonthInterval`.

- Require `z3c.form >= 2.6` to get rid of some odd test dependencies.


1.3.2 (2015-10-13)
------------------

- Fix `configure.zcml` to include needed `meta.zcml` files.


1.3.1 (2015-08-05)
------------------

- Migrate repository to https://bitbucket.org/gocept/gocept.month


1.3 (2014-07-16)
----------------

- Add placeholder for month widget in z3c forms describing the required month
  format.


1.2 (2013-02-18)
----------------

- Split off widgets into setuptools extra ``form``, and don't include the
  ``browser`` ZCML by ourselves, so clients can use only the domain part of
  this package without the UI parts.

- Added ``firstOfMonth`` method to ``Month``.

- Using `zope.formlib >= 4.0` instead of `zope.app.form`.

- Updated to ZTK 1.1.5.


1.1 (2012-02-09)
----------------

- Add MonthInterval.forYear().
- Declared ``fromString`` method as a class method in interface.


1.0.2 (2011-09-01)
------------------

- Added ``__contains__`` method on ``Month``.


1.0.1 (2011-04-26)
------------------

- Declare dependencies that some upstream packages need but don't declare.

- Use stdlib's doctest module, not zope.testing's which is deprecated.


1.0 (2009-10-05)
----------------

- Initial public release.
