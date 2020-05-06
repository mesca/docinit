DocInit
=======

DocInit is an opiniated, yet flexible documentation generator for your Python projects.
It removes the burden of rewriting the same configuration files over and over, and favors a simple, non-repetitive declarative style instead. It uses `Sphinx <https://www.sphinx-doc.org/>`__ and `Sphinx AutoAPI <https://github.com/readthedocs/sphinx-autoapi>`__ behind the scenes.

Features
--------

- Entirely configurable from your `setup.cfg` file
- Automatically fills the blanks so you don't have to repeat yourself
- Allows master and sub projects
- Compatible with `Read the Docs <https://readthedocs.org/>`_
- Flexible and extensible

Install
-------

.. code::

    pip install docinit

Usage
-----

Write your documentation
~~~~~~~~~~~~~~~~~~~~~~~~

Or not. If you don't do anything, DocInit will automatically find your packages, generate API documentation, and create an index page (using either your repo's `README.rst` file or a default paragraph).

You can add your own `.rst` files in the `doc` directory, and overwrite the default `index.rst`. Put your logo and favicon in `doc/_static/logo.png` and `doc/_static/favicon.ico`, respectively.

If you need to configure further, do it in the ``docinit`` section of your `setup.cfg <https://setuptools.readthedocs.io/en/latest/setuptools.html#configuring-setup-using-setup-cfg-files>`__. Refer to the configuration_ section for details.

Setup a sphinx project
~~~~~~~~~~~~~~~~~~~~~~

The following will take care of initializing everything:

.. code::

    python setup.py docinit

Don't worry, nothing will be overwritten if a file with the same name already exists. There is no need to re-run this command, even if you modify your `setup.cfg`. But if you do, nothing bad will happen.

Build
~~~~~

.. code::

    cd doc
    make html

You can now find your generated documentation in `doc/_build/html/`.

By default, the `make` command will return an error (but will still build everything) in case of warning. This allows for easy integration in your CI/CD pipelines.

.. _configuration:

Configuration
-------------

The following options are accepted:

===============  ====
Key              Type
===============  ====
``doc_dir``      str
``name``         str
``parent_url``   str
``logo_url``     str
``favicon_url``  str
``version``      str
``release``      str
``packages``     list
``author``       str
``copyright``    str
===============  ====

There is no required option. If not set, DocInit will try to find an appropriate value elsewhere. If it fails, it will settle on a default value.

doc_dir
~~~~~~~

This is where your documentation lives.

======= =======
Default Lookups
======= =======
``doc`` - ``source-dir`` in the ``build_sphinx`` section
======= =======

name
~~~~

The name of your project.

=========== =======
Default     Lookups
=========== =======
``Project`` - ``project`` in the ``build_sphinx`` section
            - ``name`` in the ``metadata`` section
            - name of the current Git repo
=========== =======

parent_url
~~~~~~~~~~

If you are managing a `subproject <https://docs.readthedocs.io/en/stable/subprojects.html>`__, this is the URL of the main project. When set, DocInit adds a `Back` entry in the menu, and configures the `intersphinx mapping <https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html>`__.

======== =======
Default  Lookups
======== =======
``None``
======== =======

logo_url
~~~~~~~~

The URL of an image that will be downloaded to `doc/_static/logo.png`. Useful for subprojects.

======== =======
Default  Lookups
======== =======
``None``
======== =======

favicon_url
~~~~~~~~~~~

The URL of an image that will be downloaded to `doc/_static/favicon.ico`. Useful for subprojects.

======== =======
Default  Lookups
======== =======
``None``
======== =======

version
~~~~~~~

The `semantic version <https://semver.org/>`__ of your package. If it is not explicitly defined, DocInit will use `pbr <https://docs.openstack.org/pbr/latest/user/features.html#version>`__ to fetch it from git tags.

============== =======
Default        Lookups
============== =======
From git tags  - ``version`` in the ``build_sphinx`` section
               - ``version`` in the ``metadata`` section
============== =======

release
~~~~~~~

The full version of your package, including VCS status. If it is not explicitly defined, DocInit will use `pbr <https://docs.openstack.org/pbr/latest/user/features.html#version>`__ to fetch it from git tags.

============== =======
Default        Lookups
============== =======
From git tags  - ``release`` in the ``build_sphinx`` section
============== =======

packages
~~~~~~~~

The list of packages for which the API documentation will be generated. If it is not specified, DocInit will discover packages from the root of your project (where `setup.cfg` is located).

========= =======
Default   Lookups
========= =======
``find:`` - ``packages`` in the ``options`` section
========= =======

author
~~~~~~

The author of the project.

============= =======
Default        Lookups
============= =======
``Anonymous``  - ``author`` in the ``metadata`` section
               - From the first commit in the current git repository
============= =======

copyright
~~~~~~~~~

The copyright for this project. If it is not defined, it will be constructed from the year of the first commit, the current year, and ``author``.

========== =======
Default    Lookups
========== =======
Generated  - ``copyright`` in the ``build_sphinx`` section
========== =======

Arbitrary options
~~~~~~~~~~~~~~~~~

That is not all: you can pass arbitrary options, and they will be injected in `conf.py`. For example, setting: ``autoapi_generate_api_docs = 0`` will disable API documentation. Please refer to the official `Sphinx <https://www.sphinx-doc.org/en/master/usage/configuration.html>`__ and `Sphinx AutoAPI <https://sphinx-autoapi.readthedocs.io/en/latest/reference/config.html>`__ documentation for recognized options.

