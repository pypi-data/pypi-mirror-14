==========================================
Welcome to argdispatch's documentation!
==========================================

This module is a drop-in replacement for :mod:`argparse`, dispatching `subcommand <https://docs.python.org/3/library/argparse.html#sub-commands>`_ calls to functions, modules or executables.

.. contents::
  :local:
  :backlinks: none

Rationale
=========

If your parser has less than five subcommands, you can parse them with :mod:`argparse`. If you have more, you still can, but you will get a huge, unreadable code. This module makes this easier by dispatching subcommand calls to functions, modules or executables.

Example 1 : Manually define subcommands
---------------------------------------

For instance, consider the following code for ``mycommand.py``::

    import sys
    from argdispatch import ArgumentParser

    def foo(args):
        """A function associated to subcommand `foo`."""
        print("Doing interesting stuff")
        sys.exit(1)

    if __name__ == "__main__":
        parser = ArgumentParser()
        subparser = parser.add_subparsers()

        subparser.add_function(foo)
        subparser.add_package("bar")
        subparser.add_executable("baz")

        subparser.parse_args()

With this simple code:

* ``mycommand.py foo -v --arg=2`` is equivalent to the python code ``foo(['-v', '--arg=2'])``;
* ``mycommand.py bar -v --arg=2`` is equivalent to ``python -m bar -v --arg=2``;
* ``mycommand.py baz -v --arg=2`` is equivalent to ``baz -v --arg=2``.

Then, each function, module or executable does whatever it wants with the arguments.

Example 2 : Automatic subcommand definition
-------------------------------------------

With programs like `git <http://git-scm.com/>`_, if a ``git-foo`` executable exists, then calling ``git foo --some=arguments`` is equivalent to ``git-foo --some=arguments``. The following code, in ``myprogram.py`` copies this behaviour::

    import sys
    from argdispatch import ArgumentParser

    if __name__ == "__main__":
        parser = ArgumentParser()
        subparser = parser.add_subparsers()

        subparser.add_iter_modules("myprogram")
        subparser.add_prefix_executables("myprogram-")

        subparser.parse_args()

With this program, given that executable ``myprogram-foo`` and python module ``myprogram.bar.__main__.py`` exist:

* ``myprogram foo -v --arg=2`` is equivalent to ``myprogram-foo -v --arg=2``;
* ``myprogram bar -v --arg=2`` is equivalent to ``python -m myprogram.bar -v --arg=2``.

Module documentation
====================

.. automodule:: argdispatch

.. _advanced:

Advanced usage
==============

This module works by subclassing two :mod:`argparse` classes:

* :class:`_SubCommandsDispatch` is a subclass of :class:`argparse._SubParsersAction`;
* :class:`ArgumentParser` is a subclass of :class:`argparse.ArgumentParser`.

The class doing all the job is :class:`_SubCommandsDispatch`.

.. autoclass:: _SubCommandsDispatch
  :no-members:

The only thing changed in :class:`ArgumentParser` is :meth:`ArgumentParser.add_subparsers`, which enforces argument ``action=_SubCommandsDispatch`` for parent method :meth:`argparse.ArgumentParser.add_subparsers`. Thus, it is also possible to use this module as following::

    import argparse
    import argdispatch

    parser = argparse.ArgumentParser(...)
    subparsers = parser.add_subparsers(action=argdispatch._SubCommandsDispatch)
    ...

Download and install
====================

See the `main project page <http://git.framasoft.org/spalax/argdispatch>`_ for
instructions, and `changelog
<https://git.framasoft.org/spalax/argdispatch/blob/master/CHANGELOG.md>`_.
