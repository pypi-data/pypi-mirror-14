.. module:: score.projects
.. role:: default
.. role:: confkey

**************
score.projects
**************

This module will help you manage your virtual environments for all your
projects.


.. _projects_quickstart:

Quickstart
==========

To create a new project called *myblog*, just use the following:

.. code-block:: console

    sirlancelot@spamalot:~$ score projects create myblog
    Will create the project folder in the following directory:
    /home/sirlancealot/myblog
    Is that OK? [y/N]: 
      ...

After confirming, the command line application will do the following:

- it will copy the default project template into the designated folder,
- create a :mod:`virtual environment <python:venv>` in
  `~/.score/projects/myblog` and
- install your newly created project into this virtualenv.

If you want to create a virtualenv for a project, that you already have checked
out, you can *register* it instead:

.. code-block:: console

    sirlancelot@spamalot:~$ score projects register cheeseshop
      ...


.. _projects_configuration:

Configuration
=============

This module adheres to our :ref:`module initialization guiedlines
<module_initialization>`, but does not require any configuration: calling its
:func:`init` without arguments is sufficient:

>>> import score.projects
>>> ctx_conf = score.projects.init()


.. _projects_details:

Details
=======

A project basically consists of a :mod:`virtual environment <venv>` and an
associated folder. That's why the ``register`` command just creates a new
virtualenv and installs the given project in the new virtualenv.

When you ``create`` a new project, this module will clone a :term:`project
template`, fill in all the blanks, move it to the specified folder and
``register`` it as described earlier.


.. _projects_virtualenv:

Virtualenv
----------

This module will add a new folder called ``projects`` in your score
configuration folder (as defined by the global :func:`score.cli.conf.rootdir`).
On UNIX systems, this is usually ``~/.score/projects``.

This folder contains all your virtual environments, as well as a configuration
file storing the project folder of each project.


.. _projects_templates:

Templates
---------

The ``create`` command accepts a :term:`project template`, that it will use. By
default, it will use the template "minimal", which ships with the module
itself. If you want a different template, you will have to provide it as an
option to the shell command:

.. code-block:: console

    sirlancelot@spamalot:~$ score projects register cheeseshop --template=git://example.com/custom-project-template.git
      ...

The ``--template`` option accepts the following values:

- A git URL starting with ``git://...``
- A git http[s] URL like ``git+http://...``
- A mercurial http[s] URL like ``hg+http://...``
- A path to a local folder

It will download/copy the given template and modify it while copying it to its
final destination. The modification just consists of string replacements in all
files:

- ``__PROJECT_NAME__`` will be replaced by the given project name,
- ``__PACKAGE_NAME__`` will be replaced by the name of the python package and
- ``__PACKAGE_NAME_CAMELCASE__`` will be the camel-cased version of the project
  name (``score.projects`` becomes ``ScoreProjects``, for example).

If a *folder* is encountered, that is called ``__PROJECT_NAME__``, it will
potentially be replaced by *multiple* folders to match the python package
structure. If you were to create a project for the module ``score.projects``,
you would end up with the following folder structure::

  score/
    __init__.py
    projects/


.. _projects_api:

API
===

Configuration
-------------

.. autofunction:: score.projects.init

.. autoclass:: score.projects.ConfiguredProjectsModule

    .. automethod:: get

    .. automethod:: register

    .. automethod:: rename

    .. automethod:: relocate

    .. automethod:: delete

    .. automethod:: all

Project
-------

.. autoclass:: score.projects.project.Project

    .. attribute:: name

        The project name

    .. attribute:: folder

        The folder containing this project's python source.

    .. attribute:: venvdir

        The folder containing the projects virtualenv. This value is
        dynamically generated and will change if you change the project name
        (by setting a new value).

    .. automethod:: score.projects.project.Project.recreate_venv

    .. automethod:: score.projects.project.Project.install

    .. automethod:: score.projects.project.Project.spawn_shell

    .. automethod:: score.projects.project.Project.vex
