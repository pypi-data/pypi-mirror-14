Status build shields for Sloth CI powered by http://shields.io.

Enable the extension in the server config and go to http://host:port/app?action=shield to get the shield for ``app``.

Use ``colors``, ``style``, and ``format`` params to customize the badge. You can set these params for all apps in the config and override them with query params when requesting a badge.


Installation
------------

.. code-block:: bash

    $ pip install sloth-ci.ext.shields_io


Usage
-----

.. code-block:: yaml
    :caption: sloth.yml

    extensions:
        shields:
            # Use the module sloth_ci.ext.shields_io.
            module: shields_io

            # Default color map for build statuses
            colors:
                INFO: green
                WARNING: yellowgreen
                ERROR: orange

            # See available styles on http://shields.io/
            style: social

            # See available formats on http://shields.io/
            format: png
            ...


