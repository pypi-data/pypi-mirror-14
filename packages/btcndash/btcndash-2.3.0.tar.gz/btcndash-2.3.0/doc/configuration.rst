===================
Configuration Guide
===================

BTCnDash is generates and displays a status dashboard for a Bitcoin node. It uses a JSON-based
configuration file which defaults to config.json in the root folder of the script, but can also
be specified on the command line.

.. contents:: Table of contents

Command-line Options
====================

Several command-line options are available

:mod:`config`
    The default config file location can be overridden using the config option::

        btcndash --config=/my/absolute/path/here/myconfig.json

:mod:`clearcache`
    Clears any cached static html files before continuing to load BTCnDash::

        btcndash --clearcache

RPC and Bitcoin Node Settings
=============================

:mod:`rpc_urn`
    This is the complete URN used to contact the bitcoin RPC server. It must start with
    ``http://`` or ``https://``. Note that v0.12 of Bitcoin Core no longer supports https
    connections! The URN must take the form of::

        http://username:password@ip.add.re.ss:port

    :mod:`username`
        RPC username. Used to log into the bitcoind RPC server. The RPC functionality must be
        enabled in the ``bitcoin.conf`` file by setting ``server=1`` along with ``rpcuser`` and
        ``rpcpassword``.
    :mod:`password`
        RPC password. Used to log into the bitcoind RPC server. Because RPC is done over http,
        this password should contain only characters that can be included in a URL. This means some
        special characters like ``#`` should not be used.
    :mod:`ip address`
        IP address of server to which RPC calls will be made (the computer on which bitcoind is
        running). This is typically the same machine this script is running on, but doesn't have to
        be. If it is not the same machine, be sure that your firewall allows the ``rpc_port`` through.
    :mod:`port`
        The port on which bitcoind listens for RPC requests.
:mod:`node_port`
    The port on which the bitcoind daemon is listening for bitcoin protocol requests. This is used
    for informational purposes only.

General settings
================

:mod:`header_title`
    This text will appear in the header of all pages to the right of the bitcoin logo.
:mod:`node_name`
    This is the text that appears in the Node Information tile as the name of the Node.
:mod:`donate_address`
    Bitcoin address to which donations can be sent for this bitcoin node server. This will be
    displayed on the dashboard and used to automatically generate a qr code.
:mod:`cache_time`
    How often, in seconds, the status pages will be refreshed. The pages are refreshed by a
    background task.
:mod:`cache_time_loc`
    How often, in seconds, the IP address and location will be refreshed. This is done by a
    background task. Location is refreshed independently because it should rarely change so will
    typically have a much longer refresh time.

Local Server Settings
=====================

:mod:`server_ip_local`
    The local, internal IP address of the server running BTCnDash. Used by the Bottle framework
    to decide which IP to listen on.
:mod:`server_ip_public`
    The public, external IP address of the server running BTCnDash. Used to find the location of
    the server and for informational purposes. This will be auto-detected if set to ``detect``.
:mod:`server_port`
    The port on which BTCnDash will listen for requests. Can't be the standard port 80 unless you
    run BTCnDash as root, which is not recommended.
:mod:`server_type`
    The type of server that the Bottle framework will use to serve pages. More information on the
    choices is available in the `Bottle documentation`_. The default is Python's built-in wsgi
    server ``wsgiref``.

    .. _Bottle documentation: http://bottlepy.org/docs/dev/deployment.html#switching-the-server-backend

:mod:`server_location`
    Physical location of the BTCnDash server. This will be auto-detected if set to ``detect``.
:mod:`server_latitude`
    The latitude of the BTCnDash server. This will be auto-detected if set to ``detect`` as long
    as either ``server_ip_public`` or ``server_location`` is also set to ``detect``.
:mod:`server_longitude`
    The longitude of the BTCnDash server. This will be auto-detected if set to ``detect`` as long
    as either ``server_ip_public`` or ``server_location`` is also set to ``detect``.
:mod:`debug`
    Sets whether or not the Bottle framework server will run in debug mode. Disable this on
    production servers!
:mod:`log_level`
    Level of detail for logging. Use typical Python logger values such as ``INFO``, ``WARN``,
    ``ERROR``, ``DEBUG`` and ``CRITICAL``.
:mod:`alternate_views`
    Defines a location which will be added as an additional search path for template files.
    Defaults to ``""``.
:mod:`alternate_static`
    Defines a location where user-defined static files may be placed for use in custom tiles.
    Custom tiles can access resources located here by directing tiles to the ``static_alt``
    directory at the BTCnDash web root - for example ``http://mysite.com/static_alt/mypng.png``.
    Defaults to ``""``.

External API settings
=====================

:mod:`qr_url`
    Address to use for generating qr codes.
:mod:`qr_param`
    Parameters to pass to the qr code generating service.
:mod:`block_height_url`
    Address to use when displaying information about the current block height.
:mod:`ip_info_url`
    Address to use when displaying information about a peer connected to the node.
:mod:`tx_info_url`
    Address to use when displaying information about a Bitcoin transaction.
:mod:`hash_diff_url`
    Address to use when displaying information about the Bitcoin network hash rate and difficulty.
:mod:`loc_url`
    Service to use to get current IP address and location.
:mod:`map_url`
    Address to use to create link to map of current location. Must use ``{}`` within the URL to
    define where the latitude and longitude will be substituted.
:mod:`donate_url`
    Address to use when directing a visitor to the donate address.
:mod:`bitnodes_url`
    Address used when querying the Bitnodes API.
:mod:`fee_url`
    Address used for retrieving fee information.

Page and Tile Settings
======================

:mod:`tx_summary_limit`
    Limits the number of recent transactions displayed in the data table found on the transactions
    page. Defaults to ``500``.
:mod:`pages`
    Stores various information about the pages that make up BTCnDash.

    :mod:`template`
        The name of the ``.tpl`` file that contains the template for this page.
    :mod:`static`
        The name of the static file to be generated as an output of the template for this page.
    :mod:`title`
        The text to appear at the top of the page.
    :mod:`tiles`
        the individual tiles (components that make up the dashboard) to be displayed on the given
        page and in which order. This is a list of lists with each sub-list being a row on the
        page.
:mod:`tiles`
    Stores information about the tiles that can be assembled on pages.

    :mod:`template`
        The name of the ``.tpl`` file that contains the template for this page.
    :mod:`rpc_commands`
        A list of RPC commands which must be called in order for this tile to have access to the
        required data while populating its template. A mostly up-to-date list of RPC commands is
        available at the `Bitcoin Wiki`_.

    .. _Bitcoin Wiki: https://en.bitcoin.it/wiki/Original_Bitcoin_client/API_calls_list
