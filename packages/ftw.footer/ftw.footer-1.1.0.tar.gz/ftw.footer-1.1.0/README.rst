Introduction
============

``ftw.footer`` provides a viewlet, which shows 1 - 4 contextual portlet columns.


Installation
============


- Add ``ftw.footer`` to your buildout configuration:

::

    [instance]
    eggs +=
        ftw.footer

- Run `bin/buildout`

- Install the generic import profile.


Configuration
=============

The amount of portlet columns in the footer can be configured in the
`portal_registry` option `IFooterSettings.columns_count`.

Up to four columns are currently supported.


Screenshot
===========

.. image:: https://raw.github.com/4teamwork/ftw.footer/master/docs/screenshot.png

The screenshot is created with
`plonetheme.onegov <https://github.com/OneGov/plonetheme.onegov>`_.



Links
=====

- Github: https://github.com/4teamwork/ftw.footer
- Issues: https://github.com/4teamwork/ftw.footer/issues
- Pypi: http://pypi.python.org/pypi/ftw.footer
- Continuous integration: https://jenkins.4teamwork.ch/search?q=ftw.footer


Copyright
=========

This package is copyright by `4teamwork <http://www.4teamwork.ch/>`_.

``ftw.footer`` is licensed under GNU General Public License, version 2.
