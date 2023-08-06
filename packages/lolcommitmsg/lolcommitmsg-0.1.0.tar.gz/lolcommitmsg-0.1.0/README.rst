lolcommitmsg
============

Demo
----

.. image:: https://github.com/petedmarsh/lolcommitmsg/raw/master/lolcommitmsg.gif

Installation
------------

.. code:: bash


  $ pip install lolcommitmsg
  $ cd lovely-repository
  $ echo -e '#!/bin/sh\nsed -i "/^#/d" $1\nlolcommitmsg $1' > .git/hooks/commit-msg && chmod +x .git/hooks/commit-msg

Acknowledgements
----------------

* Moe: https://github.com/busyloop/lolcat

* Wijnand Modderman-Lenstra: https://github.com/tehmaze/lolcat
