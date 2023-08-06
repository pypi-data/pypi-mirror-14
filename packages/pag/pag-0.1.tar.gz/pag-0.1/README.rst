pag
===

Command line tool for interacting with https://pagure.io

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

When already in a cloned repo, you can easily add remotes of other forks to collaborate::

    ❯ cd koji/
    ❯ pag remote add ausil
    ❯ git remote -v
    ausil   ssh://git@pagure.io/fork/ausil/koji.git (fetch)
    origin  ssh://git@pagure.io/koji.git (fetch)
    ❯ git pull ausil master

----

``pag`` provides a convenience command for creating new projects::

    ❯ pag create factory2 "Ostensibly better than factory version 1"
