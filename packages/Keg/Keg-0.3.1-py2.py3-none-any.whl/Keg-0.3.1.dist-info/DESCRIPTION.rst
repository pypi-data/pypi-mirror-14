.. default-role:: code

Keg: more than Flask
####################


.. image:: https://coveralls.io/repos/level12/keg/badge.svg?branch=master
    :target: https://coveralls.io/r/level12/keg?branch=master

.. image:: https://codecov.io/github/level12/keg/coverage.svg?branch=master
    :target: https://codecov.io/github/level12/keg?branch=master

.. image:: https://img.shields.io/pypi/dm/Keg.svg   
    :target: https://img.shields.io/pypi/dm/Keg.svg

.. image:: https://img.shields.io/pypi/v/Keg.svg   
    :target: https://img.shields.io/pypi/v/Keg.svg 

.. image:: https://img.shields.io/pypi/l/keg.svg   
    :target: https://img.shields.io/pypi/l/keg.svg

.. image:: https://img.shields.io/pypi/pyversions/keg.svg   
    :target: https://img.shields.io/pypi/pyversions/keg.svg

.. image:: https://img.shields.io/pypi/status/Keg.svg   
    :target: https://img.shields.io/pypi/status/Keg.svg

Keg is an opinionated but flexible web framework built on Flask and SQLAlchemy.


Keg's Goal
==========

The goal for this project is to encapsulate Flask best practices and libraries so devs can avoid
boilerplate and work on the important stuff.

We will lean towards being opinionated on the big things (like SQLAlchemy as our ORM) while
supporting hooks and customizations as much as possible.

Think North of Flask but South of Django.

Features
========

Coming (maybe not so) soon.  :)

Installation
============

- pip install keg


App Configuration
=================

CLI Command
-----------

The command `<myapp> develop config` will give detailed information about the files and objects
being used to configure an application.

Profile Prority
---------------

All configuration classes with the name `DefaultProfile` will be applied to the app's config
first.

Then, the configuration classes that match the "selected" profile will be applied on top of the
app's existing configuration. This makes the settings from the "selected" profile override any
settings from the `DefaultProfile.`

Practically speaking, any configuration that applies to the entire app regardless of what context
it is being used in will generally go in `myapp.config` in the `DefaultProfile` class.

Selecting a Configuration Profile
---------------------------------

The "selected" profile is the name of the objects that the Keg configuration handling code will
look for.  It should be a string.

A Keg app considers the "selected" profile as follows:

    * If `config_profile` was passed into `myapp.init()` as an argument, use it as the
      selected profile.  The `--profile` cli option uses this method to set the selected profile and
      therefore has the highest priority.
    * Look in the app's environment namespace for "CONFIG_PROFILE".  If found, use it.
    * If running tests, use "TestProfile".  Whether or not the app is operating in this mode is
      controlled by the use of:

      - `myapp.init(use_test_profile=True)` which is used by `MyApp.testing_prep()`
      - looking in the app's environment namespace for "USE_TEST_PROFILE" which is used by
        `keg.testing.invoke_command()`

    * Look in the app's main config file (`app.config`) and all it's other
      config files for the variable `DEFAULT_PROFILE`.  If found, use the value from the file with
      highest priority.


Keg Development
===============

To develop on keg, begin by running our tests::

    git clone https://github.com/level12/keg keg-src
    cd keg-src
    cp cp keg_apps/db/user-config-tpl.py ~/.config/keg_apps.db/keg_apps.db-config.py
    # edit the DB connection info in this file (you don't have to use vim):
    vim ~/.config/keg_apps.db/keg_apps.db-config.py
    tox

You can then examine tox.ini for insights into our development process.  In particular, we:

* use `py.test` for testing (and coverage analysis)
* use `flake8` for linting
* store `pip` requirements files in `requirements/`
* cache wheels in `requirements/wheelhouse` for faster & more reliable CI builds

Dependency Management
---------------------

Adding a dependency involves:

#. Adding the dependency to one of the requirements files in `requirements/`.
#. Running `wheelhouse build`

Preview Readme
--------------

When updating the readme, use `restview --long-description` to preview changes.


Issues & Discussion
====================

Please direct questions, comments, bugs, feature requests, etc. to:
https://github.com/level12/keg/issues

Current Status
==============

Very Alpha, expect changes.



Changelog
=========

0.3.1 released 2013-03-17
-------------------------

- Fixed 0.3.0 build where readme wouldn't install correctly
- Cleaned up repo which had a coverage report commited
- Added a new build environment

0.3.0 released 2015-09-16
-------------------------

- better pypi classifiers
- use `Wheelhouse <https://github.com/level12/wheelhouse>`_ for dependency management
- Add tests for `BaseView` auto-assign feature.
- Add an asset manager.

    * Templates can now use the `assets_include` tag in Jinja templates to
      automatically include the content of a file with the same base name but a 'css' or 'js'
      suffix. See `keg_apps/templating/templates/assets_in_template.html` for example.
    * Templates can now use the `assets_content` tag to include content with a specific suffix.  See
      `keg_apps/templating/templates/assets_content.html` for example.

- Adjust DB clearing so that `prep_empty()` is called after during db_clear() and not
  only `db_init_with_clear().`
- Fix selection of configuration profile so that the ordering is consitent for app instances
  created by `testing_prep()` and `invoke_command()`.

Backwards incompatibility notes:

- In the unlikely event you were relying on `keg.db:DatabaseManager.prep_empty()` in a non-default
  way, you may have some adjustments to make.
- `myapp.config_profile` has been removed.  Use `myapp.config.profile` instead.
- the signature of `MyApp()` and `myapp.init()` has changed.


development version: 2015-05-25
-------------------------------

- Remove `Keg.testing_cleanup()`: wasn't really needed
- Fix db init when SQLALCHEMY_BINDS config option not present but DB feature enabled
- Adjust the way Jinja filters and globals are handled.  Keg will now process `.template_filters` and
  `.template_globals` (both should be dicts) if defined on an app.
- add signals and commands for database init and clearing
- new `Keg.visit_modules` attribute & related functionality to have Keg load Python modules after
  the app has been setup.

BC changes required:

- if you were using `Keg.testing_cleanup()` explicitly, remove it.
- If using `.jinja_filters` on your app, rename to `.template_filters`

development version: 2015-05-23
-------------------------------

Making changes to the way database interactions are handled.

- Move `keg.sqlalchemy` to `keg.db`
- `keg.Keg`'s `sqlalchemy_*` properties have been renamed, see `db_*` variables instead.
- All database management is being delegated to an application specific instance of
  `keg.db.DatabaseManager`.  The class used to manage the db is selected by
  `keg.Keg.db_manager_cls` so custom db management functionality for an app can be easily
  implemented by overriding that method on an app and specifying a different DB manager.
- `keg.db.DatabaseManager` is multi-connection aware using the "bind" functionality adopted by
  Flask-SQLAlchemy.
- Added `keg_apps.db` application and related tests.
- Added `keg.db.dialect_ops` to manager RDBMS specific database interactions.
- Move `clear_db()` functionality into `keg.db.dialect_ops`
- Add concept of dialect options to Keg config handling (`KEG_DB_DIALECT_OPTIONS`).  The
  PostgreSQL dialect handles the option `postgresql.schemas` to facilitate the testing setup of
  multiple schemas in a PostgreSQL database.  See `keg_apps.db.config` for example usage.

BC changes required:

- On your app, if you have `sqlalchemy_enabled` set, change it to `db_enabled`
- If importing from `keg.sqlalchemy` change to `keg.db`.


