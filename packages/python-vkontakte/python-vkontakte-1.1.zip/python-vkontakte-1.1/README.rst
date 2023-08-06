python-vkontakte
****************

.. image:: https://badge.fury.io/py/python-vkontakte.svg
    :target: https://badge.fury.io/py/python-vkontakte

Python library to access vkontakte social network api.

Installation
============

Via pip:

.. code-block:: shell

    pip install python-vkontakte

Api
===

.. code-block:: python

    import pyvkontakte
    api = pyvkontakte.VkontakteApi()
    api.call('users.get', user_ids=1) # [{'last_name': 'Дуров', 'id': 1, 'first_name': 'Павел'}]

or calling method via class attribute:

.. code-block:: python

    api.users_get(user_ids=1) # [{'last_name': 'Дуров', 'id': 1, 'first_name': 'Павел'}]

Are both the same. In a second form, it is a method name where dots replaced with underscores - ``wall.getById`` will be ``wall_getById`` and so on.

If you want to call some private api, which require access token, just create a api class with it:

.. code-block:: python

    pyvkontakte.VkontakteApi('access token')

Using different api version:

.. code-block:: python

    pyvkontakte.VkontakteApi(v='5.50')

If some error occures after api request (response json contains ``error`` insead of ``response`` key), ``pyvkontakte.VkontakteApiError`` will be raised.
Special attribute ``json`` will be avaible on exception object, additionally exception str representation will contain error description and error code.

Authorization
=============

For obtaining access token, you can use ``pyvkontakte.auth`` method.

.. code-block:: python

    pyvkontakte.auth(login, password, client_id, scope)

which will return dict with keys access_token, expires_in, user_id. If login or password is invalid, ``pyvkontakte.InvalidCredentials`` will be raised.
If some parsing error occurs, ``pyvkontakte.ParsingError`` will be raised.
Both ``pyvkontakte.InvalidCredentials`` and ``pyvkontakte.ParsingError`` are subclasses of ``pyvkontakte.VkontakteAuthError``.

There is also a logger ``pyvkontakte`` (``pyvkontakte.auth`` and ``pyvkontakte.api``) enabled.
``pyvkontakte.api`` logs an INFO every request made with request params, and DEBUG with json of response
