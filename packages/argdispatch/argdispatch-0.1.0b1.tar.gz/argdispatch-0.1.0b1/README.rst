argdispatch — Drop-in replacement for `argparse` dispatching subcommand calls to functions, modules or binaries
===============================================================================================================

|sources| |pypi| |build| |documentation| |license|

If your parser has less than five subcommands, you can parse them with ``argparse``. If you have more, you still can, but you will get a huge, unreadable code. This module makes this easier by dispatching subcommand calls to functions, modules or binaries.

Examples
--------

Example 1 : Manual definition of subcommands
""""""""""""""""""""""""""""""""""""""""""""

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
        subparser.add_binary("baz")

        subparser.parse_args()

With this simple code:

* ``mycommand.py foo -v --arg=2`` is equivalent to the python code ``foo(['-v', '--arg=2'])``;
* ``mycommand.py bar -v --arg=2`` is equivalent to ``python -m bar -v --arg=2``;
* ``mycommand.py baz -v --arg=2`` is equivalent to ``baz -v --arg=2``.

Then, each function, module or binary does whatever it wants with the arguments.

Example 2 : Automatic definition of subcommands
"""""""""""""""""""""""""""""""""""""""""""""""

With programs like `git <http://git-scm.com/>`_, if a ``git-foo`` binary exists, then calling ``git foo --some=arguments`` is equivalent to ``git-foo --some=arguments``. The following code, in ``myprogram.py`` copies this behaviour::

    import sys
    from argdispatch import ArgumentParser

    if __name__ == "__main__":
        parser = ArgumentParser()
        subparser = parser.add_subparsers()

        subparser.add_iter_modules("myprogram")
        subparser.add_prefix_binaries("myprogram-")

        subparser.parse_args()

With this program, given that binary ``myprogram-foo`` and python module ``myprogram.bar.__main__.py`` exist:

* ``myprogram foo -v --arg=2`` is equivalent to ``myprogram-foo -v --arg=2``;
* ``myprogram bar -v --arg=2`` is equivalent to ``python -m myprogram.bar -v --arg=2``.

Documentation
"""""""""""""

The complete documentation is available on `readthedocs <http://argdispatch.readthedocs.org>`_.

To compile it from source, download and run::

      cd doc && make html

What's new?
-----------

See `changelog
<https://git.framasoft.org/spalax/argdispatch/blob/master/CHANGELOG.md>`_.

Download and install
--------------------

* From sources:

  * Download: https://pypi.python.org/pypi/argdispatch
  * Install (in a `virtualenv`, if you do not want to mess with your distribution installation system)::

        python3 setup.py install

* From pip::

    pip install argdispatch

* Quick and dirty Debian (and Ubuntu?) package

  This requires `stdeb <https://github.com/astraw/stdeb>`_ to be installed::

      python3 setup.py --command-packages=stdeb.command bdist_deb
      sudo dpkg -i deb_dist/argdispatch-<VERSION>_all.deb


.. |documentation| image:: http://readthedocs.org/projects/argdispatch/badge
  :target: http://argdispatch.readthedocs.org
.. |pypi| image:: https://img.shields.io/pypi/v/argdispatch.svg
  :target: http://pypi.python.org/pypi/argdispatch
.. |license| image:: https://img.shields.io/pypi/l/argdispatch.svg
  :target: http://www.gnu.org/licenses/gpl-3.0.html
.. |sources| image:: https://img.shields.io/badge/sources-argdispatch-brightgreen.svg
  :target: http://git.framasoft.org/spalax/argdispatch
.. |build| image:: https://git.framasoft.org/spalax/argdispatch/badges/master/build.svg
  :target: https://git.framasoft.org/spalax/argdispatch/builds

