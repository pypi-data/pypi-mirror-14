.. contents:: Table of Contents


Installation
============

Add the package as dependency to your setup.py:

.. code:: python

  setup(...
        install_requires=[
          ...
          'ftw.servicenavigation',
        ])

or to your buildout configuration:

.. code:: ini

  [instance]
  eggs += ftw.servicenavigation

and rerun buildout.


Icons
=====

By default this package implements a list of font awesome (Version 4.3.0) icons (only .yaml).
You're self responsible how the icon resources are loaded.

If you don not use the Icon feature, no problem the only effect it has is a CSS Class applied on
a service navigation item.

Further this packages ships with select2 (Version 4.0.0) for the Icons list.
If you have already select2 installed, that's fine it will not be loaded again.


Links
=====

- Github: https://github.com/4teamwork/ftw.servicenavigation
- Issues: https://github.com/4teamwork/ftw.servicenavigation/issues
- Pypi: http://pypi.python.org/pypi/ftw.servicenavigation
- Continuous integration: https://jenkins.4teamwork.ch/search?q=ftw.servicenavigation


Copyright
=========

This package is copyright by `4teamwork <http://www.4teamwork.ch/>`_.

``ftw.servicenavigation`` is licensed under GNU General Public License, version 2.
