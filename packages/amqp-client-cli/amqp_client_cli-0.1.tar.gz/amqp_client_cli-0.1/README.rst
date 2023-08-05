amqp-client-cli
===============

A simple CLI tool for sending amqp messages to exchanges.

What is the purpose of ``amqp-client-cli``?
-------------------------------------------

The purpose of this command line tool is to make sending messages to
exchanges as simple as possible. Uses include:

-  In ``cron`` scripts that periodically send simple messages to an
   ``ampq`` server for workers to pick up.
-  Unit testing during implementation of an ``amqp`` system into a
   workflow.
-  Simple one-off queue messages where anything more than a simple
   command line tool is a hassle to use.

What does ``amqp-client-cli`` **not** do?
-----------------------------------------

This tool is **not** intended for configuration. It assumes your entire
infrastructure is already in place. It can **only** send to existing
exchanges and vhosts and provide a routing key.

It is up to you to configure your infrastructure elsewhere before using
this tool (i.e. through your queue workers, through something like
``rabbitmqadmin``, through a web management console. etc).

How do I get it?
----------------

Install via pip:

::

    pip install amqp-client-cli

How do I use it?
----------------

``amqp-client-cli`` is run via the ``amqpcli`` command. Run the ``help``
subcommand to see the list of options:

::

    $ amqpcli help
    amqpcli: A command line interface for interacting with amqp exchanges

    Usage: amqpcli {{options}} {{subcommand}}

    Options:
      -h, --help     Show this help message and exit
      -n, --nocolor  Do not colorize output

    Subcommands:
      config  Configure the amqpcli client
      send    Send a message to an exchange

Let's send a message!
~~~~~~~~~~~~~~~~~~~~~

Sending messages can be done using the ``amqpcli send`` command.

::

    amqpcli send: Send a message to an exchange

    Usage: send {{arguments}} {{options}}

    Arguments:
      host [text]         Address of the amqp server
      port [int]          Port of the amqp server
      exchange [text]     Name of the exchange being sent to
      routing_key [text]  The routing key for the message

    Options:
      -h, --help              Show this help message and exit
      -m, --message [text]    String to use as the message body
      -f, --file-path [text]  Path of a file to use as the message body
      -p, --persistent        Make the message persistent if routed to a durable queue
      -u, --user [text]       User to connect to the queue as
      -v, --vhost [text]      The vhost to connect to
      -n, --nocolor           Do not colorize output

Let's assume we have a `RabbitMQ <https://www.rabbitmq.com>`__ server
listening at ``localhost:5671`` with an exchange we would like to send a
message to named ``exchange_a`` on a vhost ``my_vhost`` with a routing
key of ``simple_message``. We are going to send via the ``guest`` user.

Let's define our message on the command line!
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    $ amqpcli send localhost 5671 exchange_a simple_message -m "Hello there" -v my_vhost
    User: guest
    Password:
    Connecting to queue @ localhost:5671... SUCCESS!
    Message successfully published to exchange [exchange_a]!

Let's define our message as a file!
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The message body can also be a file. It will be interpreted as binary.

**Warning:** Although *any* binary content can be sent, it is **not**
recommended to insert large payloads into the queue for performance
reasons.

.. code:: bash

    $ echo "I'm a message in a file" > my_message.txt

::

    $ amqpcli send localhost 5671 exchange_a simple_message -f my_message.txt -v my_vhost
    User: guest
    Password:
    Connecting to queue @ localhost:5671... SUCCESS!
    Message successfully published to exchange [exchange_a]!

How can I specify credentials/configurations for a script?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can optionally add user credentials to a config file for use with
the tool (``~/.amqpclirc``). There is no limit to the number of users
that can be added.

Configuration options can be seen from the command line.

::

    amqpcli config: Configure the amqpcli client

    Usage: config {{options}} {{subcommand}}

    Options:
      -h, --help     Show this help message and exit
      -n, --nocolor  Do not colorize output

    Subcommands:
      add_user     Add a new queue user
      delete_user  Remove an existing queue user

With ``add_user``, you will be prompted for a username, password, and
vhost (default is ``/``).

A user can also be specified in the environment variables by defining
``AMQP_USER``, ``AMQP_PASSWORD``, and ``AMQP_VHOST``.

::

    $ amqpcli config add_user
    User: guest
    Password:
    vhost? [/]: my_vhost
    $ amqpcli send localhost 5671 exchange_a simple_message -m "Hello there" -u guest
    Connecting to queue @ localhost:5671... SUCCESS!
    Message successfully published to exchange [exchange_a]!
