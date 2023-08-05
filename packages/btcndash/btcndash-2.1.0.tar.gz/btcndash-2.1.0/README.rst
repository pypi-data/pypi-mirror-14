========
BTCnDash
========

BTCnDash is a web-based dashboard displaying information about the status of a bitcoin node such
as currently connected peers, recent transactions forwarded, bandwidth usage, and network stats
like hash rate. Most items are generated automatically or retrieved from the bitcoind server
itself via RPC calls.

BTCnDash is meant to be lightweight, and with the assumption that there will be very low traffic
to the dashboard. As such, it does not use a full webserver like Nginx or apache. It uses the
Bottle_ microframework and generates static status pages on a schedule. Python's WSGI reference
server is used as the actual webserver, but Bottle (and therefore BTCnDash) can be served by lots
of different servers. Python 2.7 is required. 3.5 works, but is not as well tested!.

.. _Bottle: http://bottlepy.org

.. image:: https://bitbucket.org/mattdoiron/btcndash/raw/default/doc/btcndash_screenshot.png

Author and Acknowledgements
===========================

BTCnDash is written and maintained by Matt Doiron <mattdoiron@gmail.com> and is released under
the GPL v3 license. The source can be found on the Bitbucket_ page. Hope you find it useful!
If so, please consider donating Bitcoin to 1AHT2Zq7JneADw94M8uCdKRrqVZfhrTBYM

.. _Bitbucket: https://bitbucket.org/mattdoiron/btcndash

Thanks to those who make great tools like these that make BTCnDash possible:

* Bottle: python web framework (http://bottlepy.org)
* bitcoinlib: rpc library (https://github.com/petertodd/python-bitcoinlib/)
* Blocks: bootstrap theme (http://alvarez.is/)

Other Resources
===============

* See the `BTCnDash PyPi page`_ for other info.
* Also see the `BTCnDash documentation`_.

.. _`BTCnDash PyPi page`: https://pypi.python.org/pypi/btcndash/
.. _`BTCnDash documentation`: https://pythonhosted.org/btcndash/
