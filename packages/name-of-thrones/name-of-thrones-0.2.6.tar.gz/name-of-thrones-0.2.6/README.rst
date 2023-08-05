===============
Name of Thrones
===============
.. image:: https://img.shields.io/travis/Matt-Deacalion/Name-of-Thrones.svg
    :target: https://travis-ci.org/Matt-Deacalion/Name-of-Thrones
    :alt: Build Status
.. image:: https://img.shields.io/coveralls/Matt-Deacalion/Name-of-Thrones.svg
    :target: https://coveralls.io/r/Matt-Deacalion/Name-of-Thrones?branch=master
    :alt: Test Coverage
.. image:: https://img.shields.io/pypi/dw/name-of-thrones.svg
    :target: https://pypi.python.org/pypi/name-of-thrones/
    :alt: Downloads
.. image:: https://img.shields.io/pypi/v/name-of-thrones.svg
    :target: https://pypi.python.org/pypi/name-of-thrones/
    :alt: Latest Version
.. image:: https://img.shields.io/pypi/wheel/name-of-thrones.svg
    :target: https://pypi.python.org/pypi/name-of-thrones/
    :alt: Wheel Status
.. image:: https://img.shields.io/github/license/name-of-thones/apistatus.svg
    :target: https://pypi.python.org/pypi/name-of-thrones/
    :alt: License

Command line tool to generate words that sound like characters from Game of Thrones. Useful for
unique project names, host names and the occasional stray cat.

.. image:: https://raw.githubusercontent.com/Matt-Deacalion/Name-of-Thrones/screenshots/screenshot.png
    :alt: Name of Thrones screenshot

Installation
------------
You can install the *Name of Thrones* using pip:

.. code-block:: bash

    $ pip install name-of-thrones

Usage
-----
You can use the `name-of-thrones` command from the shell to run Name of Thrones::

    $ name-of-thrones --help

    Generate words that sound like characters from Game of Thrones.

    Usage:
      name-of-thrones [--quantity=<number>] [--min=<length>] [--max=<length>]
                      [--json] [--nocolour] [--alphabetical] [--length] [--reverse]
      name-of-thrones (-h | --help | --version)

    Options:
      --version                show program's version number and exit.
      -h, --help               show this help message and exit.
      -q, --quantity=<number>  the quantity of words to generate [default: 10].
      --min=<length>           the minimum length of each word [default: 4].
      --max=<length>           the maximum length of each word [default: 10].
      -j, --json               output the words in JSON format.
      -n, --nocolour           output the words without colourization.
      -a, --alphabetical       output the words in alphabetical order.
      -l, --length             output the words in order of their length.
      -r, --reverse            reverse the order of the words.

License
-------
Copyright © 2016 `Matt Deacalion Stevens`_, released under The `MIT License`_.

.. _Matt Deacalion Stevens: http://dirtymonkey.co.uk
.. _MIT License: http://deacalion.mit-license.org
