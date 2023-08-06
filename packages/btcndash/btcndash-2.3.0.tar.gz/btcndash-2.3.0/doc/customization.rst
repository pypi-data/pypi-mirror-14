===================
Customization Guide
===================

BTCnDash is customizable, allowing users to choose which tiles are displayed on the index page
and also in which order they are displayed. Advanced users can also create custom tiles.

.. contents:: Table of contents

Tiles and Their Order
=====================

To modify how tiles are displayed, change the ``pages`` variable in the ``config.json`` file.
The default index page is shown below::

    "pages": {
        "index": {
          "template": "index.tpl",
          "static": "index.html",
          "title": "Bitcoin Node Status",
          "tiles": [ ["general2", "nodedetails", "mempool"],
                     ["bandwidth_summary", "network", "bandwidth"],
                     ["bitnodes", "donate2", "21co_fees"] ]
        },
        ...
    }

In the above snippet, the ``tiles`` variable is a list of lists, with each list being a row on
the index page. The names in each row are the names of a tile to display. If, for example,
we wanted to remove the donate tile, leaving a blank in its place, and swap the ``bitnodes`` and
``mempool`` tiles, we would change the ``tiles`` variable to look like the following::

    "tiles": [ ["general2", "nodedetails", "bitnodes"],
               ["bandwidth_summary", "network", "bandwidth"],
               ["mempool", "blank", "21co_fees"] ]

Currently, there can be no more than three tiles in each row, but advanced users could modify the
tiles to allow other arrangements. Also, new pages cannot currently be added - users can modify
the current four pages only: ``index``, ``peers``, ``tx`` and ``404``.

Creating New Tiles
==================

Advanced users may be able to create their own tiles by copying one of the various tiles
currently available and modifying as they see fit. BTCnDash uses `Bottle's Simple Template Engine`_
so users can reference its documentation for details on how to modify the temples.

Various data is available to templates in the form of a dictionary called ``data``. The keys of
this dictionary include all config variables, and any variables returned by the RPC commands
specified in the ``tiles`` section of the ``config.json`` file. A sample is
see below::

    "tiles": {
        ...
        "general2": {
          "template": "general2.tpl",
          "rpc_commands": [ "getnetworkinfo", "getblockchaininfo" ]
        },
        ...
    }

In the above snippet, the ``getnetworkinfo`` and ``getblockchaininfo`` RPC commands will be run
and their results available to *all* templates if the ``general2`` tile is specified in the
``pages`` variable of the ``config.json`` file. Each RPC command will be called only once,
regardless of how many times it may be listed in various tiles.

.. _Bottle's Simple Template Engine: http://bottlepy.org/docs/dev/stpl.html

