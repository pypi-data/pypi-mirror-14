======================
 Holocron Clear Theme
======================

|pypi-version| |pypi-license|

Holocron Clear Theme is an extension that provides simple and clear theme
for Holocron-powered blogs.


Installation
------------

Holocron uses entry-points based extension discovery mechanism, and that
means it's enough to use ``pip`` to install Clear Theme:

.. code:: bash

    $ [sudo] pip3 install holocron-clear-theme


Usage
-----

In order to use Clear Theme you've got to enable ``clear-theme`` extension.
You can do it through your ``_config.yml`` file by changing ``ext.enabled``
option:

.. code:: yaml

   ext:
      enabled:
         - ...
         - clear-theme      # <-- inserted line

Screenshots
-----------

.. image:: https://raw.githubusercontent.com/ikalnitsky/holocron-clear-theme/master/screenshots/post.png
   :align: center


Links
-----

* Holocron: http://holocron.readthedocs.org
* Source: https://github.com/ikalnitsky/holocron-clear-theme
* Bugs: https://github.com/ikalnitsky/holocron-clear-theme/issues


.. Badges
.. |pypi-version| image:: https://img.shields.io/pypi/v/holocron-clear-theme.svg
   :target: https://pypi.python.org/pypi/holocron-clear-theme
.. |pypi-license| image:: https://img.shields.io/pypi/l/holocron-clear-theme.svg
   :target: https://pypi.python.org/pypi/holocron-clear-theme
