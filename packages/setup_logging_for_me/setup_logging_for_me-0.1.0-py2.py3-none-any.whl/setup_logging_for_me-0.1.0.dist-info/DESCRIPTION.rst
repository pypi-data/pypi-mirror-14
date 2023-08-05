===============================
setup logging for me
===============================

I never remember how to do python logging basic config. Do you?


* Free software: ISC license

Features
--------

Need to view your logs on the console? Just do:

.. code-block:: python

    import setup_logging_for_me
    ...
    setup_logging_for_me.basicConfig()

Which does nothing more than calling to:

.. code-block:: python

    logging.basicConfig(level=logging.INFO,
                        format="%(name)s %(levelname)s %(asctime)s - %(message)s)


Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage


=======
History
=======

0.1.0 (2016-1-22)
------------------

* First release on PyPI.


