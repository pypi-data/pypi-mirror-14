Kaching
=======

Pass, fail and trigger sounds for test driven development.

Intended for use when refactoring with tests to give you auditory feedback about passes, failures and triggered test runs.

To install::

    $ apt-get install mplayer (or equivalent)
    $ pip install kaching

Command line use::

    $ kaching start
    [ starting sound ]
    
    $ kaching fail
    [ failure sound ]

    $ kaching win
    [ passing test sound ]
    
Python API use::

    >>> import kaching
    >>> kaching.start()
    [ starting sound ]
    
    >>> kaching.fail()
    [ failure sound ]
    
    >>> kaching.win()
    [ passing test sound ]

Kaching requires mplayer to be installed to make a sound although it won't raise an exception / exit with status code > 0 if it isn't.

Sounds taken from : http://soundfxnow.com/