collective.pygelf
=================

Provides ZConfig_-compatible logger handler factories for
`Graylog Extended Log Format`__.

__ http://docs.graylog.org/en/latest/pages/gelf.html

.. code:: python

Usage with `plone.recipe.zope2instance`_:

.. _ZConfig: https://pypi.python.org/pypi/ZConfig
.. _plone.recipe.zope2instance: https://pypi.python.org/pypi/plone.app.zope2instance

.. code:: ini

   [instance]
   ...
   event-log-custom =
       %import collective.gelf
       <gelfudp>
           host 127.0.0.1
           port 9401
           custom app_name=Zope buildout=example.com
       </gelfudp>

Available GELF hander types are ``gelfudp``, ``gelftcp`` and ``gelftls``.  See
pygelf_-documentation for available configuration options.

.. _pygelf: https://pypi.python.org/pypi/pygelf

Custom fields with static values can be defined with ``custom`` option,
which accepts space separated list of ``fieldname=staticvalue`` pairs.
