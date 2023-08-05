Whyd to go
==========

|Build Status| |Coverage Status| |PyPI|

About
-----

"Take your Whyd playlists away."

This is a very simple comand-line wrapper around youtube-dl for Whyd
using BeautifulSoup4, requests and docopt.

Many thanks to the
`Whyd <https://whyd.com>`__ team for their support.

Usage
-----

Check the built-in help: ``whydtogo --help``

For development usage use ``python whydtogo/__init__.py --help``

Don't want to install anything ? Use this automatically generated
`Docker image <https://registry.hub.docker.com/u/djiit/whydtogo/>`__ :

.. code:: bash

    docker run djiit/whydtogo

Installation (all platforms)
----------------------------

You will need (obviously) Python 3.X and pip. Python 3.4 comes bundled
with pip. For earlier Python version, check how to install pip here :
https://pip.pypa.io/en/latest/installing.html.

Optional : to extract audio from YouTube videos, you will also need
avconv of ffmpeg (check how to download ffmpeg here : https://www.ffmpeg.org/download.html)

WhydToGo is available on PYPI. Open a terminal and type :

.. code:: bash

    pip install WhydToGo


For development purpose, check out the latest version from this repository :

.. code:: bash

    git clone https://github.com/Djiit/whydtogo.git
    cd whydtogo
    pip install -e .

License
-------

See `LICENSE <./LICENSE>`__

.. |Build Status| image:: https://travis-ci.org/Djiit/whydtogo.svg
   :target: https://travis-ci.org/Djiit/whydtogo
.. |Coverage Status| image:: https://coveralls.io/repos/Djiit/whydtogo/badge.svg
   :target: https://coveralls.io/r/Djiit/whydtogo
.. |PyPI| image:: https://img.shields.io/pypi/v/whydtogo.svg
   :target: https://pypi.python.org/pypi/whydtogo