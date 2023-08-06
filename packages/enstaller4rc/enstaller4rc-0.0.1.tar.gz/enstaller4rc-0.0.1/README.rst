.. image:: https://travis-ci.org/enthought/enstaller4rc.png
  :target: https://travis-ci.org/enthought/enstaller4rc

This is a small library to read an existing `.enstaller4rc` file without
importing enstaller.

This supports `.enstaller4rc` from the 4.6.X series until 4.8.X. It only
supports parsing configuration, and purposedly does not support modifying it.

Example::

        from enstaller4rc import Configuration

        config = Configuration.from_file(".enstaller4rc")
        print(config.auth)
        print(config.use_pypi)
        print(config.indexed_repositories)
