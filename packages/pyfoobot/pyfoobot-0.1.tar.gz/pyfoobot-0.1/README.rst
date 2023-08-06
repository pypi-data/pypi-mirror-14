pyfoobot
========

.. image:: https://travis-ci.org/philipbl/pyfoobot.svg?branch=master
    :target: https://travis-ci.org/philipbl/pyfoobot

A Python wrapper for the `FooBot API <http://api.foobot.io/apidoc/index.html>`__. It allows you to pull data from your `Foobot device <http://foobot.io>`__.

Installation
------------
::

    pip install pyfootbot

Example
-------
::

    fb = Foobot("username", "password")
    devices = fb.devices()

    # Devices is a list, in case you have more than one foobot
    device = devices[0]

    # Get the most recent sample
    latest_data = device.latest()

    # Get data from the last hour
    last_hour_data = device.data_period(3600, 0)

    # Get data for a data range
    range_data = device.data_range(start='2016-04-12T11:00:00',
                                   end='2016-04-12T12:00:00')
