pag
===

``pag`` helps you win at `pagure.io <https://pagure.io>`_.

Intended to mimic the `hub <https://github.com/github/hub>`_ cli tool for `github.com <https://github.com>`_.

Usage
-----

::

    $ pag --help
    Usage: pag [OPTIONS] COMMAND [ARGS]...

    Options:
      --help  Show this message and exit.

    Commands:
      clone
      create
      remote

----

The clone command can be used to clone a repo by name without having to find or type out the URL::

    ❯ pag clone koji
    Cloning into 'koji'...

Or you can clone a fork::

    ❯ pag clone ralph/koji
    Cloning into 'koji'...

----

After you clone a repo, you can fork it on pagure.io and adjust your local `remote` settings::

    ❯ pag fork

----

If you want to add the remotes of other forks, that's easy too.  Just do it by username::

    ❯ cd koji/
    ❯ pag remote add ausil
    ❯ git remote -v
    ausil   ssh://git@pagure.io/forks/ausil/koji.git (fetch)
    origin  ssh://git@pagure.io/koji.git (fetch)
    ❯ git pull ausil master

----


``pag`` provides a convenience command for creating new projects::

    ❯ pag create factory2 "Ostensibly better than factory version 1"
