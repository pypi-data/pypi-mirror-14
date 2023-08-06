Fauxmo README
=============

|Build Status|

Python 3 module that emulates Belkin WeMo devices for use with the
Amazon Echo.

-  Documentation:
   `fauxmo.readthedocs.org <https://fauxmo.readthedocs.org>`__

Introduction
------------

The Amazon Echo is able to control certain types of home automation
devices by voice. Fauxmo provides emulated Belkin Wemo devices that the
Echo can turn on and off by voice, locally, and with minimal lag time.
Currently these Fauxmo devices can be configured to make requests to an
HTTP server or to a `Home Assistant <https://home-assistant.io>`__
instance via `its Python
API <https://home-assistant.io/developers/python_api/>`__ and only
require a JSON config file for setup.

As of version 0.3.0, Fauxmo uses the new `asyncio
module <https://docs.python.org/3/library/asyncio.html#module-asyncio>`__
and requires Python >= 3.4.4 due to
`#6 <https://github.com/n8henrie/fauxmo/issues/6>`__. Python >= 3.5 is
encouraged, in case I decide to use the new ``async`` and ``await``
keywords in the future.

Usage
-----

Simple install: From PyPI
~~~~~~~~~~~~~~~~~~~~~~~~~

1. ``python3 -m pip install fauxmo``
2. Make a ``config.json`` based on
   ```config-sample.json`` <https://github.com/n8henrie/fauxmo/blob/master/config-sample.json>`__
3. ``fauxmo -c config.json [-v]``

Simple install of dev branch (from GitHub)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. ``pip install [-e] git+https://github.com/n8henrie/fauxmo.git@dev``

Install for development (from GitHub)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. ``git clone https://github.com/n8henrie/fauxmo.git``
2. ``cd fauxmo``
3. ``python3 -m venv venv``
4. ``source venv/bin/activate``
5. ``pip install -e .``
6. ``cp config-sample.json config.json``
7. Edit ``config.json``
8. ``fauxmo [-v]``

Set up the Echo
~~~~~~~~~~~~~~~

1. Open the Amazon Alexa webapp to the `Smart
   Home <http://alexa.amazon.com/#smart-home>`__ page
2. **With Fauxmo running**, click "Discover devices" (or tell Alexa to
   "find connected devices")
3. Ensure that your Fauxmo devices were discovered and appear with their
   names in the web interface
4. Test: "Alexa, turn on [the kitchen light]"

Set fauxmo to run automatically in the background
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

systemd (e.g. Raspbian Jessie)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Recommended: add an unprivileged user to run Fauxmo:
   ``sudo useradd -r    -s /bin/false fauxmo``

   -  NB: Fauxmo may require root privileges if you're using ports below
      1024

2. ``sudo cp extras/fauxmo.service /etc/systemd/system/fauxmo.service``
3. Edit the paths in ``/etc/systemd/system/fauxmo.service``
4. ``sudo systemctl enable fauxmo.service``
5. ``sudo systemctl start fauxmo.service``

launchd (OS X)
^^^^^^^^^^^^^^

1. ``cp extras/com.n8henrie.fauxmo.plist ~/Library/LaunchAgents/com.n8henrie.fauxmo.plist``
2. Edit the paths in
   ``~/Library/LaunchAgents/com.n8henrie.fauxmo.plist``

   -  You can remove the ``StandardOutPath`` and ``StandardErrorPath``
      sections if desired

3. ``launchctl load ~/Library/LaunchAgents/com.n8henrie.fauxmo.plist``
4. ``launchctl start com.n8henrie.fauxmo``

Handlers
--------

Fauxmo has an example REST handler class that reacts to on and off
commands using the
`python-requests <http://docs.python-requests.org/en/latest/>`__ library
as well as a handler for the `Home Assistant Python
API <https://home-assistant.io/developers/python_api>`__; these are
examples of a multitude of ways that you could have the Echo trigger an
action. In ``config-sample.json``, you'll see examples of:

-  A ``GET`` request to a local server
-  A ``POST`` request to the `Home Assistant REST
   API <https://home-assistant.io/developers/rest_api/>`__
-  A ``PUT`` request to an `Indigo <https://www.indigodomo.com/>`__
   server
-  Requests to `Home Asssistant's Python
   API <https://home-assistant.io/developers/python_api/>`__

Configuration
-------------

I recommend that you copy and modify ``config-sample.json``.

-  ``FAUXMO``: General Fauxmo settings

   -  ``ip_address``: Manually set the server's IP address. Optional.
      Recommended value: ``auto``

-  ``DEVICES``: List of devices that will employ ``RESTAPIHandler``

   -  ``port``: Port that Echo will use connect to device, should be
      different for each device
   -  ``handler``: Dictionary for ``RESTAPIHandler`` configuration

      -  ``on_cmd``: URL that should be requested to turn device on
      -  ``on_cmd``: URL that should be requested to turn device off
      -  ``method``: GET, POST, PUT, etc.
      -  ``headers``: Optional dict for extra headers
      -  ``on_json`` / ``off_json``: Optional dict of JSON data
      -  ``on_data`` / ``off_data``: Optional POST data
      -  ``auth_type``: ``basic`` or ``digest`` authentication, optional
      -  ``user`` / ``password``: for use with ``auth_type``, also
         optional

   -  ``description``: What you want to call the device (how to activate
      by Echo)

-  ``HOMEASSISTANT``: Section for `Home Assistant Python
   API <https://home-assistant.io/developers/python_api>`__

   -  ``enable``: Disable this section by omitting or setting to
      ``false``
   -  ``host``: IP of host running Hass
   -  ``port``: Port for Hass access (default: 8123)
   -  ``password``: Hass API password
   -  ``DEVICES``: List of devices that will employ ``HassApiHandler``

      -  ``description``: What you want to call the device (how to
         activate by Echo)
      -  ``port``: Port that Echo will use connect to device, should be
         different for each device
      -  ``entity_id``: Hass identifier used in API, one easy way to
         find is to curl and grep the REST API, eg
         ``curl http://IP_ADDRESS/api/bootstrap   | grep entity_id``

Troubleshooting / FAQ
---------------------

-  Increase logging verbosity with ``-v[vv]``
-  Ways to ensure your config is valid JSON:

   -  ``python -m json.tool < config.json``
   -  Use ``jsonlint`` or one of numerous online tools

-  But I don't *wanna* upgrade to 3.4.4... how can I install an older
   version of Fauxmo that worked with Python 3.4.2?

   -  Install from a tag:

      -  ``pip install git+git://github.com/n8henrie/fauxmo.git@v0.1.11``

   -  Install from a specific commit:

      -  ``pip install   git+git://github.com/n8henrie/fauxmo.git@d877c513ad45cbbbd77b1b83e7a2f03bf0004856``

Installing Python 3.5 with pyenv
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

    sudo install -o $(whoami) -g $(whoami) -d /opt/pyenv
    git clone https://github.com/yyuu/pyenv /opt/pyenv
    echo 'export PYENV_ROOT="/opt/pyenv"' >> ~/.bashrc
    echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
    echo 'eval "$(pyenv init -)"' >> ~/.bashrc
    source ~/.bashrc
    pyenv install 3.5.1

You can then install Fauxmo into Python 3.5 in a few ways, including:

.. code:: bash

    # Install with pip
    "$(pyenv root)"/versions/3.5.1/bin/python3.5 -m pip install fauxmo

    # Run with included console script
    fauxmo -c /path/to/config.json -vvv

    # Show full path to fauxmo console script
    pyenv which fauxmo

    # I recommend using the full path for use in start scripts (e.g. systemd, cron)
    "$(pyenv root)"/versions/3.5.1/bin/fauxmo -c /path/to/config.json -vvv

    # Alternatively, this also works (after `pip install`)
    "$(pyenv root)"/versions/3.5.1/bin/python3.5 -m fauxmo.cli -c config.json -vvv

Acknowledgements / Reading List
-------------------------------

-  Tremendous thanks to @makermusings for `the original version of
   Fauxmo <https://github.com/makermusings/fauxmo>`__!

   -  Also thanks to @DoWhileGeek for commits towards Python 3
      compatibility

-  http://www.makermusings.com/2015/07/13/amazon-echo-and-home-automation
-  http://www.makermusings.com/2015/07/18/virtual-wemo-code-for-amazon-echo
-  http://hackaday.com/2015/07/16/how-to-make-amazon-echo-control-fake-wemo-devices
-  https://developer.amazon.com/appsandservices/solutions/alexa/alexa-skills-kit
-  https://en.wikipedia.org/wiki/Universal_Plug_and_Play
-  http://www.makermusings.com/2015/07/19/home-automation-with-amazon-echo-apps-part-1
-  http://www.makermusings.com/2015/08/22/home-automation-with-amazon-echo-apps-part-2

.. |Build Status| image:: https://travis-ci.org/n8henrie/fauxmo.svg?branch=master
   :target: https://travis-ci.org/n8henrie/fauxmo


Changelog
=========

Will not contain minor changes -- feel free to look through ``git log``
for more detail.

0.3.0 :: 20160409
-----------------

-  Fauxmo now uses asyncio and requires Python >= 3.4.4
-  *Extensive* changes to codebase
-  Handler classes renamed for PEP8 (capitalization)
-  Moved some general purpose functions to ``fauxmo.utils`` module
-  Both the UDP and TCP servers are now in ``fauxmo.protocols``
-  Added some rudimentary `pytest <http://pytest.org/latest>`__ tests
   including `tox <http://tox.readthedocs.org/en/latest>`__ and
   `Travis <https://travis-ci.org/>`__ support
-  Updated documentation on several classes

0.2.0 :: 20160324
-----------------

-  Add additional HTTP verbs and options to ``RestApiHandler`` and
   Indigo sample to config

   -  **NB:** Breaking change: ``json`` config variable now needs to be
      either ``on_json`` or ``off_json``

-  Make ``RestApiHandler`` DRYer with ``functools.partialmethod``
-  Add ``SO_REUSEPORT`` to ``upnp.py`` to make life easier on OS X

0.1.11 :: 20160129
------------------

-  Consolidate logger to ``__init__.py`` and import from there in other
   modules

0.1.8 :: 20160129
-----------------

-  Add the ability to manually specify the host IP address for cases
   when the auto detection isn't working
   (https://github.com/n8henrie/fauxmo/issues/1)
-  Deprecated the ``DEBUG`` setting in ``config.json``. Just use
   ``-vvv`` from now on.

0.1.6 :: 20160105
-----------------

-  Fix for Linux not returning local IP

   -  restored method I had removed from Maker Musings original /
      pre-fork version not knowing it would introduce a bug where Linux
      returned 127.0.1.1 as local IP address

0.1.4 :: 20150104
-----------------

-  Fix default verbosity bug introduced in 1.1.3

0.1.0 :: 20151231
-----------------

-  Continue to convert to python3 code
-  Pulled in a few PRs by [@DoWhileGeek](https://github.com/DoWhileGeek)
   working towards python3 compatibility and improved devices naming
   with dictionary
-  Renamed a fair number of classes
-  Added kwargs to several class and function calls for clarity
-  Renamed several variables for clarity
-  Got rid of a few empty methods
-  Import devices from ``config.json`` and include a sample
-  Support ``POST``, headers, and json data in the RestApiHandler
-  Change old debug function to use logging module
-  Got rid of some unused dependencies
-  Moved license (MIT) info to LICENSE
-  Added argparse for future console scripts entry point
-  Added Home Assistant API handler class
-  Use "string".format() instead of percent
-  Lots of other minor refactoring


