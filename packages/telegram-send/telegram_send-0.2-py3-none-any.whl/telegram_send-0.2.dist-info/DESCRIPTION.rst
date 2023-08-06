telegram-send
=============

|License|

Telegram-send is a command-line tool to send messages and files over
Telegram to your account. It provides a simple interface that can be
easily called from other programs.

Usage
=====

To send a message:

.. code:: shell

    telegram-send "hello, world"

To send a file:

.. code:: shell

    telegram-send --file document.pdf

Install
=======

Install telegram-send system-wide with pip:

.. code:: shell

    sudo pip3 install telegram-send

Or if you want to install it for a single user:

.. code:: shell

    pip3 install telegram-send

If installed for a single user you need to add ``~/.local/bin`` to their
path:

.. code:: shell

    echo 'PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc

And finally configure it with ``telegram-send --configure`` and follow
the instructions.

Uninstall
=========

.. code:: shell

    sudo pip3 uninstall telegram-send
    sudo rm /etc/telegram-send.conf

.. |License| image:: https://img.shields.io/badge/License-GPLv3+-blue.svg
   :target: https://github.com/rahiel/telegram-send/blob/master/LICENSE.txt


