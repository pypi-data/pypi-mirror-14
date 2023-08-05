packagecloud-poll
=================

Overview
--------
``packagecloud-poll`` repeatedly polls the `packagecloud.io <https://packagecloud.io>`_ API, looking for a specific package 
filename to appear. It is intended to be used in continuous integration/continuous deployment pipelines, where we want 
to block something until we are sure a package has been uploaded and is available before continuing onwards.

Installation
------------
.. code:: bash

  pip install packagecloud-poll

Setup
-----
You must set a ``PACKAGECLOUD_TOKEN`` environment variable before you can run packagecloud-poll. See the `packagecloud API
documentation <https://packagecloud.io/docs/api>`_ for instructions on how to generate a token.

.. code:: bash

  export PACKAGECLOUD_TOKEN=deadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef

Running
-------
Sample invocation:

.. code:: bash

  packagecloud-poll --user my_user --repo my_repo_name --type deb --distro ubuntu --distro_version precise --arch amd64 --pkg_name myorg-stuff --filename myorg-stuff_v5.3_precise_amd64.deb

Run ``packagecloud-poll --help`` for detailed help.

Developing
----------
Setup.py creates the packagecloud-poll command. When running from source, execute ``run.py`` instead.

.. code::

  ./run.py --help
