===============================
Server Density Python Wrapper
===============================

.. image:: https://img.shields.io/pypi/v/sd-python-wrapper.svg
        :target: https://pypi.python.org/pypi/sd-python-wrapper

.. image:: https://img.shields.io/travis/serverdensity/sd-python-wrapper.svg
        :target: https://travis-ci.org/serverdensity/sd-python-wrapper


A python wrapper for the Server Density Api
It runs on both python 2.7 and up to python 3.5

* Free software: MIT license
* Documentation: https://apidocs.serverdensity.com/

Up and running
--------------

There are two ways of using the api wrapper. Either calling the endpoints from an instance of :code:`ApiClient` or from an instance of the class of an endpoint such as :code:`Device`.

.. code-block:: python

    from serverdensity.wrapper import ApiClient
    from serverdensity.wrapper import Device

    token = '2dfae5bf81f65492a40569d39b29ffa3'

    client = ApiClient(token)
    device = client.devices.create(data={'name': 'testdevice'})


    # instead of keyword arguments, it can also take a dictionary.
    device2 = Device(token, name='name2')
    device2.create()

    # This will create an AttributeError, since name is required to create a
    # device at some point.
    device3 = Device(token, group='testgroup')



Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
