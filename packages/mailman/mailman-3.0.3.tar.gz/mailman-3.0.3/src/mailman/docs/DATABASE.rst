========================
Setting up your database
========================

Mailman uses the SQLAlchemy_ ORM to provide persistence of data in a
relational database.  By default, Mailman uses Python's built-in SQLite3_
database, however, SQLAlchemy is compatible with PostgreSQL_ and MySQL, among
possibly others.

Currently, Mailman is known to work with either the default SQLite3 database,
or PostgreSQL.  (Volunteers to port it to other databases are welcome!).  If
you want to use SQLite3, you generally don't need to change anything, but if
you want Mailman to use PostgreSQL, you'll need to set that up first, and then
change a configuration variable in your ``/etc/mailman.cfg`` file.

Two configuration variables control which database Mailman uses.  The first
names the class implementing the database interface.  The second names the URL
for connecting to the database.  Both variables live in the ``[database]``
section of the configuration file.


SQLite3
=======

As mentioned, if you want to use SQLite3 in the default configuration, you
generally don't need to change anything.  However, if you want to change where
the SQLite3 database is stored, you can change the ``url`` variable in the
``[database]`` section.  By default, the database is stored in the *data
directory* in the ``mailman.db`` file.  Here's how you'd force Mailman to
store its database in ``/var/lib/mailman/sqlite.db`` file::

    [database]
    url: sqlite:////var/lib/mailman/sqlite.db


PostgreSQL
==========

First, you need to configure PostgreSQL itself.  This `Ubuntu article`_ may
help.  Let's say you create the `mailman` database in PostgreSQL via::

    $ sudo -u postgres createdb -O $USER mailman

You would then need to set both the `class` and `url` variables in
`mailman.cfg` like so::

    [database]
    class: mailman.database.postgresql.PostgreSQLDatabase
    url: postgres://myuser:mypassword@mypghost/mailman

That should be it.

If you have any problems, you may need to delete the database and re-create
it::

    $ sudo -u postgres dropdb mailman
    $ sudo -u postgres createdb -O myuser mailman

My thanks to Stephen A. Goss for his contribution of PostgreSQL support.


Database Migrations
===================

Mailman uses `Alembic`_ to manage database migrations.  Let's say you change
something in the models, what steps are needed to reflect that change in the
database schema?  You need to create and enter a virtual environment, install
Mailman into that, and then run the ``alembic`` command.  For example::

    $ virtualenv -p python3 /tmp/mm3
    $ source /tmp/mm3/bin/activate
    $ python setup.py develop
    $ alembic -c src/mailman/config/alembic.cfg revision --autogenerate -m
      "<migration_name>"

This would create a new migration which would automatically be migrated to the
database on the next run of Mailman.  Note that the database needs to be in
the older state so that Alembic can track the changes in the schema and
autogenerate a migration.  If you don't have the database in the older state
you can remove the `--autogenerate` flag in the above command.  It would then
create a new empty revision which you can edit manually to reflect your
changes in the database schema.

People upgrading Mailman from previous versions need not do anything manually,
as soon as a new migration is added in the sources, it will be automatically
reflected in the schema on first-run post-update.

**Note:** When auto-generating migrations using Alembic, be sure to check
the created migration before adding it to the version control.  You will have
to manually change some of the special data types defined in
``mailman.database.types``.  For example, ``mailman.database.types.Enum()``
needs to be changed to ``sa.Integer()``, as the ``Enum`` type stores just the
integer in the database.  A more complex migration would be needed for
``UUID`` depending upon the database layer to be used.


.. _SQLAlchemy: http://www.sqlalchemy.org/
.. _SQLite3: http://docs.python.org/library/sqlite3.html
.. _PostgreSQL: http://www.postgresql.org/
.. _MySQL: http://dev.mysql.com/
.. _`Ubuntu article`: https://help.ubuntu.com/community/PostgreSQL
.. _`Alembic`: https://alembic.readthedocs.org/en/latest/
