===================
``virtualenvutils``
===================

You can manage virtualenv based utilities with this utility.
Its primary (and initial) use is to generate Bash  `alias`es for
utilities that are installed in separate virtualenvs.
In such a setup, you don't want to extend your path with the
``bin`` directory of each of the virtualenvs, as that gives you:

- a long PATH
- multiple python executables in your PATH
- all utilties that are a result of installing some Python package dependency
  and for which you might want to use a different version (or not all).

``virtualenvutils alias dir1 dir2`` scans directories, non-recursive, under ``dir1`,
``dir2`` for virtualenvs. Any directory containing ``bin``, ``lib``, ``include`` subdirectories as well as a file ``bin/activate`` is considered a virtualenv.

For any of those virtualenvs it does one of following (checked in this order):

- if there is a virtualenvutils.conf file it is loaded to determine
  the utilties and possibly their mapping.
- if the name of the directory under ``dir1``, etc., is e.g. ``do_xyx``,
  and ``dir1/do_xyz/bin/do_xyz`` exists and is executable then this is
  the utility
- if there is no matching name, then all of the executable files under
  ``bin`` except those matching ``activate*``, ``easy_install*``,
  ``pip*``, ``python*``, ``wheel*`` are considered utilities, unless
  they have extensions matching ".so", ".py", or ".pyc".

the utility then generates aliases for all utilities found this way,
making sure they are unique if added by the last method, and writes
those alias definitions to stdout. Any error go to stderr.

Other functionalities include:

- updating all packages for all virtualenvs

see ``virtualenvutils --help`` for the full list of subcommands

``virtualenvutils.conf``
------------------------

The ``virtualenvutils.conf`` file, if provided, has to be in
the toplevel directory of the virtualenv (i.e. next to ``bin``,
``include`` and ``lib`` and consist of single line with or without a
colon (:).

If there is no colon, then the line is considered to be the
name of an executable file under that virtualenvs ``bin``.

If there is a colon, the part before the colon is considered the
name for executable under ``bin``, for which the executable name is
the part behind the colon.


Example
-------

You want to install docker-compose in a virtualenv. If you do::

   mkvirtualenv -p /opt/python3/bin/python /opt/util/docker-compose
   source !$/bin/activate
   pip install docker-compose
   deactivate
   virtualenvutils alias /opt/util

you will get::

   alias docker-compose='/opt/util/docker-compose/bin/docker-compose'

If you would have specified a different final  directory::

   mkvirtualenv -p /opt/python3/bin/python /opt/util/compose
   source !$/bin/activate
   pip install docker-compose
   deactivate
   virtualenvutils alias /opt/util

you will get::

  alias docker-compose='/opt/util/compose/bin/docker-compose'
  alias jsonschema='/opt/util/compose/bin/jsonschema'

In either of these two examples you can force the way the aliases are
generated (the example is based on the first)::

   echo 'dc:docker-compose' > /opt/util/docker-compose/virtualenvutils.conf
   virtualenvutils alias /opt/util

you will get::

   alias dc='/opt/util/docker-compose/bin/docker-compose'

and if you then append::

   echo 'docker-compose' >> /opt/util/docker-compose/virtualenvutils.conf

will get you::

   alias dc='/opt/util/docker-compose/bin/docker-compose'
   alias docker-compose='/opt/util/docker-compose/bin/docker-compose'

Usage ``.bashrc``
-----------------

You would normally put something like::

  /opt/util/virtualenvutils/bin/virtualenvutils alias /opt/util/ > /tmp/$$.alias
  source /tmp/$$.alias
  rm -f /tmp/$$.alias

in your ``~/.bashrc`` to get the appropriate aliases loaded (of course
assuming that you installed ``virtualenvutils`` in a virtualenv
``/opt/util/virtualenvutils``, which is not necessary, as long as
``bash`` can find the utility).

Updating existing virtualenvs
=============================

You can update all packages for all virtualenv utilities (under `/opt/util`) by using:

   virtualenvutils update /opt/util

The arguments to `update` are checked to see if they are virtualenvs. If they
are they get update on an individual basis. If they are not (as in the above
example) each of their subdirs are checked to be virtualenvs (non-recursive).

Installing a new util
=====================

You can install one or more new virtualenv based utilities using
something like:

  virtualenvutils install /opt/util/{docker-compose,ruamel.yaml.cmd}

``virtualenv`` has to be in your path for this, you can use ``--pkg``
to give a package name that differs from the final part of the path
(in which case you can of course only specify one path), and with
``--python /opt/python/3/bin/python`` you can explicitly
specify the python version to use.

Don't forget that you probably have to logout and login for if you set
your aliases through as scan initiated in ``.bashrc``, before you
can use the commands.
