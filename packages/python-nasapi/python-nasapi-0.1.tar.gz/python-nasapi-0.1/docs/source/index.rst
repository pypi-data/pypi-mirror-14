python-nasapi
=============

Python-nasapi is a client library for interacting with NASA api's.

Example:

.. code-block:: python

    import os
    from datetime import date

    from nasapi import Nasapi


    os.environ['NASA_API_KEY'] = 'yourkeyhere'

    resource = Nasapi.get_apod(date=date(2015, 10, 22), hd=True)


.. note::

    Currently the wrapper only includes the APOD, Imagery and Assets endpoints.


Contents
--------

.. toctree::
   :maxdepth: 3

   setup


Modules
-------

- :class:`.Nasapi`
- :class:`.NasapiError`


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
