.. image:: docs/fingerpointing.png
    :align: left
    :alt: Finger Pointing
    :height: 100px
    :width: 100px

***************
Finger Pointing
***************

.. contents:: Table of Contents

Life, the Universe, and Everything
==================================

Keep track of different events and write them down to an audit log.

Mostly Harmless
===============

.. image:: http://img.shields.io/pypi/v/collective.fingerpointing.svg
   :target: https://pypi.python.org/pypi/collective.fingerpointing

.. image:: https://img.shields.io/travis/collective/collective.fingerpointing/master.svg
    :target: http://travis-ci.org/collective/collective.fingerpointing

.. image:: https://img.shields.io/coveralls/collective/collective.fingerpointing/master.svg
    :target: https://coveralls.io/r/collective/collective.fingerpointing

Got an idea? Found a bug? Let us know by `opening a support ticket`_.

.. _`opening a support ticket`: https://github.com/collective/collective.fingerpointing/issues

Don't Panic
===========

Installation
------------

To enable this package in a buildout-based installation:

#. Edit your buildout.cfg and add add the following to it::

    [buildout]
    ...
    eggs =
        collective.fingerpointing

After updating the configuration you need to run ''bin/buildout'', which will take care of updating your system.

Go to the 'Site Setup' page in a Plone site and click on the 'Add-ons' link.

Check the box next to ``collective.fingerpointing`` and click the 'Activate' button.

Usage
-----

Go to 'Site Setup' and select 'Finger Pointing' and enable the events you want to keep an eye on.

.. figure:: docs/controlpanel.png
    :align: center
    :height: 600px
    :width: 768px

    The Finger Pointing control panel configlet.

Finger Pointing will start logging the selected events::

    # bin/instance fg
    2016-03-01 17:29:29 INFO ZServer HTTP server started at Tue Mar  1 17:29:29 2016
            Hostname: 0.0.0.0
            Port: 8080
    2016-03-01 17:29:31 INFO collective.fingerpointing Start logging audit information to audit.log
    2016-03-01 17:29:34 INFO Plone OpenID system packages not installed, OpenID support not available
    2016-03-01 17:29:37 INFO Zope Ready to handle requests
    2016-03-01 17:31:40 INFO collective.fingerpointing user=admin ip=127.0.0.1 action=logged out
    2016-03-01 17:31:49 INFO collective.fingerpointing user=admin ip=127.0.0.1 action=logged in

These events are also logged in `var/log/audit.log`::

    2016-03-01 17:31:40,813 - collective.fingerpointing - INFO - user=admin ip=127.0.0.1 action=logged out
    2016-03-01 17:31:49,678 - collective.fingerpointing - INFO - user=admin ip=127.0.0.1 action=logged in

The audit log is available through the `@@fingerpointing-log` view,
available in portal_actions for users with the `collective.fingerpointing: Show the Log` permission.
