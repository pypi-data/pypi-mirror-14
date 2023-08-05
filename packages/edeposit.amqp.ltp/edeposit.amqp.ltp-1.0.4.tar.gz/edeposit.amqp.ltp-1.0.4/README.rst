Introduction
============

.. image:: https://badge.fury.io/py/edeposit.amqp.ltp.png
    :target: https://pypi.python.org/pypi/edeposit.amqp.ltp

.. image:: https://img.shields.io/pypi/dm/edeposit.amqp.ltp.svg
    :target: https://pypi.python.org/pypi/edeposit.amqp.ltp

.. image:: https://readthedocs.org/projects/edeposit-amqp-ltp/badge/?version=latest
    :target: http://edeposit-amqp-ltp.readthedocs.org/

.. image:: https://img.shields.io/pypi/l/edeposit.amqp.ltp.svg

.. image:: https://img.shields.io/github/issues/edeposit/edeposit.amqp.ltp.svg
    :target: https://github.com/edeposit/edeposit.amqp.ltp/issues


This project provides bindings to LTP (Long Time Preservation) system, which
archives ebooks.

Documentation
-------------

Full module documentation and description can be found at Read the Docs:

- http://edeposit-amqp-ltp.readthedocs.org/

Installation
------------

Prepare system ::

   edeposit-aplikace:~ # groupadd edep
   edeposit-aplikace:~ # useradd ltp

- add user ``ltp`` and ``edeposit`` into group ``edep``

- install package::

   edeposit-aplikace:~ # pip install -U edeposit.amqp                                                              
   
- create necessary directories::

   edeposit-aplikace:~ # mkdir /home/ltp
   edeposit-aplikace:~ # chown ltp:edep /home/ltp/ -R
   
   edeposit-aplikace:~ # sudo su - ltp
   ltp@edeposit-aplikace:~> mkdir edep2ltp
   ltp@edeposit-aplikace:~> mkdir ltp2edep

- add them proper permissions::

   ltp@edeposit-aplikace:~> chgrp edep edep2ltp/
   ltp@edeposit-aplikace:~> chgrp edep ltp2edep/
   ltp@edeposit-aplikace:~> chmod 770 edep2ltp/ ltp2edep/

   ltp@edeposit-aplikace:~> ls -al
   total 16
   drwxr-xr-x 4 ltp  edep 4096 Jul 24 15:48 .
   drwxr-xr-x 6 root root 4096 Jul 24 15:40 ..
   drwxrwx--- 2 ltp  edep 4096 Jul 24 15:48 edep2ltp
   drwxrwx--- 2 ltp  edep 4096 Jul 24 15:48 ltp2edep


- authorize external ssh user by its public key::

   ltp@edeposit-aplikace:~> mkdir .ssh
   ltp@edeposit-aplikace:~> cat public-key.pub >> .ssh/authorized_keys

   ltp@edeposit-aplikace:~> ls -al .ssh/
   total 12
   drwxr-xr-x 2 ltp users 4096 Jul 24 16:13 .
   drwxr-xr-x 5 ltp edep  4096 Jul 24 16:05 ..
   -rw-r--r-- 1 ltp users  603 Jul 24 16:13 authorized_keys

Run application
----------------

Run it as ``ltp`` user::

   ltp@edeposit-aplikace:~> edeposit_amqp_ltpd.py start --foreground
