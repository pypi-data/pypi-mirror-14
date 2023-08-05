click-didyoumean
================
|pypi| |build| |license|

Enable git-like *did-you-mean* feature in click.

|demo|

Example
-------

This example is based on the official naval example from click:

.. code::

    $ naval shi move
    Usage: naval [OPTIONS] COMMAND [ARGS]...

    Error: No such command "shi".

    Did you mean one of these?
        ship


Usage
-----

Install this extension with pip:

.. code::

    pip install click-didyoumean


Use specific *did-you-mean* `group` class for your cli:


.. code:: python

    import click
    from click_didyoumean import DYMGroup

    @click.group(cls=DYMGroup)
    def cli():
        pass

    @cli.command()
    def foo():
        pass

    @cli.command()
    def bar():
        pass

    @cli.command()
    def barrr():
        pass

    if __name__ == "__main__":
        cli()


Or you it in a `CommandCollection`:

.. code:: python

    import click
    from click_didyoumean import DYMCommandCollection

    @click.group()
    def cli1():
        pass

    @cli1.command()
    def foo():
        pass

    @cli1.command()
    def bar():
        pass

    @click.group()
    def cli2():
        pass

    @cli2.command()
    def barrr():
        pass

    cli = DYMCommandCollection(sources=[cli1, cli2])

    if __name__ == "__main__":
        cli()


Change configuration
--------------------

There are two configuration for the ``DYMGroup`` and ``DYMCommandCollection``:

+-----------------+-------+---------+---------------------------------------------------------------------------+
| Parameter       | Type  | Default | Description                                                               |
+=================+=======+=========+===========================================================================+
| max_suggestions | int   | 3       | Maximal number of *did-you-mean* suggestions                              |
+-----------------+-------+---------+---------------------------------------------------------------------------+
| cutoff          | float | 0.5     | Possibilities that don’t score at least that similar to word are ignored. |
+-----------------+-------+---------+---------------------------------------------------------------------------+

Examples
~~~~~~~~

.. code:: python

    @cli.group(cls=DYMGroup, max_suggestions=2, cutoff=0.7)
    def cli():
        pass

    ... or ...

    cli = DYMCommandCollection(sources=[cli1, cli2], max_suggestions=2, cutoff=0.7)


.. |pypi| image:: https://img.shields.io/pypi/v/click-didyoumean.svg?style=flat&label=version
    :target: https://pypi.python.org/pypi/click-didyoumean
    :alt: Latest version released on PyPi

.. |build| image:: https://img.shields.io/travis/timofurrer/click-didyoumean/master.svg?style=flat
    :target: http://travis-ci.org/timofurrer/click-didyoumean
    :alt: Build status of the master branch

.. |demo| image:: https://asciinema.org/a/duyr2j5d7w7fhpe7xf71rafgr.png
    :target: https://asciinema.org/a/duyr2j5d7w7fhpe7xf71rafgr
    :alt: Demo

.. |license| image:: https://img.shields.io/badge/license-MIT-blue.svg?style=flat
    :target: https://raw.githubusercontent.com/timofurrer/click-didyoumean/master/LICENSE
    :alt: Package license
