Ambisafe client
===============

Install
-------

Use pip

::

    pip install ambisafe

Usage
-----

Create client
~~~~~~~~~~~~~

Import Client and create client object

::

    from ambisafe import Client

    client = Client(ambisafe_server_url, secret, api_key, api_secret)

You can set prefix for account id

::

    client = Client(ambisafe_server_url, secret, api_key, api_secret, account_id_prefix='prefix')

You can provide read and connect timeout (in seconds)

::

    client = Client(ambisafe_server_url, secret, api_key, api_secret, connect_timeout=2.5, read_timeout=5)

Create account
~~~~~~~~~~~~~~

Simple security schema
^^^^^^^^^^^^^^^^^^^^^^

::

    account = client.create_simple_account(account_id, currency='BTC')

Wallet4 security schema
^^^^^^^^^^^^^^^^^^^^^^^

Generate operator container using secret and create user container from
public\_key, data (encrypted private key), iv and salt

::

    from ambisafe import Container

    operator_container = Container.generate(client.secret)
    user_container = Container(public_key, data, iv, salt)

Create account for security schema "Wallet4" and "BTC" currency

::

    account = client.create_wallet4_account(account_id, user_container=user_container, 
                                            operator_container=operator_container, 
                                            currency='BTC')

Update Wallet4 account
~~~~~~~~~~~~~~~~~~~~~~

Create new containers and update account

::

    account = client.update_wallet4_account(account_id, user_container=user_container, 
                                            operator_container=operator_container, 
                                            currency='BTC')

Get balance
~~~~~~~~~~~

Get balance in float

::

    balance = client.get_balance(account_id, 'BTC')

Get account
~~~~~~~~~~~

::

    account = client.get_account(account_id, 'BTC')

Make payment
~~~~~~~~~~~~

For Simple account
^^^^^^^^^^^^^^^^^^

Build and submit transaction

::

    transaction = client.build_transaction(account_id, 'BTC', address, amount)
    result = client.submit(account_id, transaction, 'BTC')

For Wallet4 accounts
^^^^^^^^^^^^^^^^^^^^

Build transaction

::

    transaction = client.build_transaction(account_id, 'BTC', address, amount)

Sign this transaction by user, then sing by operator and submit it

::

    transaction = client.sign_wallet4_transaction(transaction, account_id, 'BTC')
    client.submit(account_id, transaction, 'BTC')

    # or

    result = client.cosign_wallet4_and_submit(transaction, account_id, 'BTC')

Build recovery transaction
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    transaction = client.build_recovery_transaction(account_id, currency, old_address)

Disclaimer
----------

The library still in BETA. There can be changes without backward
compatibility.
