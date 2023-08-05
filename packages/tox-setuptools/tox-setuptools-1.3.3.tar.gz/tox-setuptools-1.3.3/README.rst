tox-setuptools
==============

Intro
-----

Tox integration with setuptools test runner. This is a repackage of a sample code from the Tox_ documentation site to allow cleaner ``setup.py`` files.

.. _Tox: http://tox.readthedocs.org/en/latest/example/basic.html#integration-with-setuptools-distribute-test-commands

Instruction
-----------

Add this package into ``setup_requires`` parameter of your ``setup()`` configuration (of ``setup.py`` script)::

    setup(...,
          setup_requires=['tox-setuptools'])

This will automatically overwrite ``test`` command which will run ``tox`` instead.
