=====================
pytest_exact_fixtures
=====================

Proactively tear-down session and module fixtures so that only those fixtures requested by the current test are active.
This is useful when multiple fixtures modify the same module global.
The behaviour is similar to that of zope.testrunner layers_.

.. _layers: https://pypi.python.org/pypi/zope.testrunner#layers
