Status build badges for Sloth CI apps, powered by http://shields.io.


Installation
------------

.. code-block:: bash

    $ pip install sloth-ci.ext.shields_io


Usage
-----

#.  Enable the extension in the server config:

        .. code-block:: yaml
            :caption: sloth.yml for Shields.io

            extensions:
                shields:
                    # Use the module sloth_ci.ext.shields_io.
                    module: shields_io

                    # Badge label. You can use the ``{app}`` and ``{timestamp}`` placeholders for app name and build timestamp.
                    # label: "My Sloth CI Status for {app}" # default is ``Sloth CI: {app}``

                    # Badge status. You can use ``{status}``, ``{app}``, and ``{timestamp}`` placeholders build status, app name, and build timestamp
                    # status: "{status}" # default is ``{status}, {timestamp}``

                    # Badge style: ``plastic``, ``flat``, ``flat-square``, or ``social``
                    # style: social # default is ``flat``

                    # Badge format: svg, png, jpg, or gif
                    # format: png # default is svg

                    # Color map for build statuses
                    # colors:
                    #    INFO: green # default is ``brightgreen``
                    #    WARNING: yellowgreen # default is ``yellow``
                    #    ERROR: orange # default is ``red``
                    ...

    All params are optional.

#.  Use the URL http://host:port/app?action=shield to get your badge.

    You can customize the badge on the fly by passing ``label``, ``style``, and ``format`` query params:

    -   http://host:port/app?action=shield&label=Build%20for%20{app}
    -   http://host:port/app?action=shield&style=social
    -   http://host:port/app?action=shield&format=png



