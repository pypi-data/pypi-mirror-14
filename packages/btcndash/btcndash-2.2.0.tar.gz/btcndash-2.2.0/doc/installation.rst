==================
Installation Guide
==================

BTCnDash is developed on and intended for use on Debian/Ubuntu linux flavours. It should work
anywhere Python 2.7 or 3.5 work, but it hasn't been tested very much. BTCnDash is not currently
compatible with Python 2.6. This guide assumes you have bitcoind installed already. There are
various tutorials on the web on how to do this.

.. contents:: Table of contents

Create a new User
~~~~~~~~~~~~~~~~~

It's a bad idea to run most anything as root so let's create a user just for BTCnDash::

    sudo adduser --system --group btcndash

Create a virtualenv
~~~~~~~~~~~~~~~~~~~

Technically, this step is optional, but it's highly recommended to ensure updates to other Python
files/libraries later don't break BTCnDash. Many users will already have pip and virtualenv
installed, but if not install them now. The exact location of the home directory is not important
as long as the permissions are set properly (see later steps)::

    sudo apt-get install python-pip python-virtualenv
    cd /home/btcndash
    virtualenv venv
    source venv/bin/activate

Install BTCnDash
~~~~~~~~~~~~~~~~

The recommended way to install BTCnDash is via pip::

    pip install btcndash

It can also be installed manually by downloading the latest release of BTCnDash::

    wget https://bitbucket.org/mattdoiron/btcndash/get/v2.1.0.tar.gz
    
If you have mercurial installed you can also do::

    hg clone https://bitbucket.org/mattdoiron/btcndash
    
In either of the manual cases, you will need to manually install the dependencies::

    pip install -r requirements.txt
    
Configure bitcoind and BTCnDash
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Take a look at the sample ``bitcoin.conf`` supplied in the ``docs`` folder, to see how to
configure bitcoind to accept RPC requests. The important steps would be to ensure that the RPC
server is enabled by setting ``server=1`` and that a username and password are defined with
``rpcuser`` and ``rpcpassword``.

If there is a firewall involved, it must be configured to ensure that the RPC port is accessible
from the machine on which BTCnDash in installed. Make sure you open the port for the BTCnDash
webserver so that you can access it over your network and/or the internet. Note this is NOT the
same as the RPC port. The RPC port should NOT be exposed unless you intend to run the BTCnDash
program on a computer other than the one running bitcoind. It is a significant security risk to
expose the RPC port to the Internet! You may need to open the webserver port on your router as
well (similarly to how you would have opened a port for bitcoind to get it working).

See the :doc:`configuration` for details on configuring BTCnDash itself.

Create startup scripts
~~~~~~~~~~~~~~~~~~~~~~

Use the provided startup scripts in the ``scripts`` folder and change any values near the top of
the file to match your system and the location of various files. Specific instructions for
locations and use of these scripts is beyond the scope fo this help, so please see the web for
additional details if needed.

Permissions
~~~~~~~~~~~

Use the following command to make sure the files that will be used by BTCnDash are owned by the
user created in step one::

    sudo chown -R btcndash:btcndash /path/to/virtualenv
    sudo chown -R btcndash:btcndash /path/to/btcndash_homedir

Start it and test it
~~~~~~~~~~~~~~~~~~~~

If installed via pip, BTCnDash can be started like this::

    btcndash

Or, if using a startup script, then::

    sudo start btcndash
    
or::

    sudo service btcndash start

or for systemd::

    sudo systemctl enable btcndash
    sudo systemctl start btcndash

