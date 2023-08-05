sqlitemodel
===========

sqlitemodel is a wrapper for the sqlite3 database that enables you to
create models you can easily save, query and retrieve from the database.

This is build with three classes who abstract the database communication
and the object management.

Installation
------------

Install through **pip**.

::

    $ pip install sqlitemodel

or get from source

::

    $ git clone https://github.com/gravmatt/sqlitemodel.git
    $ cd sqlitemodel
    $ python setup.py install

Classes
-------

-  `**Model** - Abstraction class to build database models <#model>`__

-  `**SQL** - SQL query builder <#sql>`__

-  `**Database** - sqlite database interface <#database>`__

Model
-----

Class to abstract the model communication with the database.

Usage
~~~~~

**Import**

::

    from sqlitemodel import Model, Database

    # IMPORTANT
    Database.DB_FILE = 'path/to/database.db'

**Set the path to the database when your application starts or before
you try to accessing the database.**

Example
^^^^^^^

Building a user class that inherits the Model class to show how it
works.

::

    class User(Model):
        def __init__(self, id=None):
            Model.__init__(self, id)

            self.firstname = ''
            self.lastname = ''
            self.age = ''

            # Tries to fetch the object by its rowid from the database
            self.getModel()


        # Tells the database class the name of the database table
        def tablename(self):
            return 'users'


        # Tells the database class more about the table columns in the database
        def columns(self):
            return [
                {
                  'name': 'firstname',
                  'type': 'TEXT'
                },
                {
                  'name': 'lastname',
                  'type': 'TEXT'
                },
                {
                  'name': 'age',
                  'type': 'INTEGER'
                }
            ]

The two methods ``tablename()`` and ``columns()`` are required so that
the Database class knows how the table and its columns are called.

``id`` argument and the ``getModel()`` method in the constructor are
optional.

**The ``Model`` class constructor has an optional ``dbfile`` argument.
If it is set, the static variable ``Database.DB_FILE`` is ignored.**

Working with the User class
^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Creating a new User**

::

    # create a new user
    user = User()

    # creating the table inside the database
    user.createTable()

    # add infos about the user
    user.firstname = 'Rene'
    user.lastname = 'Tanczos'
    user.age = 25

    # save the user into the database
    user.save()

**Retriving the User from the database**

::

    # get it by id
    user = User(1)

    # get the user by his firstname and lastname
    # User().selectOne(SQL())
    user = User().selectOne(SQL().WHERE('firstname', '=', 'Rene').AND().WHERE( 'lastname', '=', 'Tanczos'))

    # Or get more the one user
    # this method will return an array of matching users
    users = User().select(SQL().WHERE('age', '=', 25))

SQL
---

Class to build SQL query to reduce misspelling and to abstract this
problem a bit.

Usage
~~~~~

**Import**

::

    from sqlitemodel import SQL

**INSERT**

::

    sql = SQL().INSERT('users').VALUES(firstname='Rene', lastname='tanczos')

    print sql.toStr()
    # INSERT INTO users (firstname,lastname) VALUES (?,?);

    print sql.getValues()
    # ('Rene', 'tanczos')

**UPDATE**

::

    sql = SQL().UPDATE('users').SET('firstname', 'Rene').SET('lastname', 'Tanczos').WHERE('firstname', '=', 'Rene').AND().WHERE('lastname', '=', 'Tanczos')

    print sql.toStr()
    # UPDATE users SET firstname=?, lastname=? WHERE firstname=? AND lastname=?;

    print sql.getValues()
    # ('Rene', 'Tanczos', 'Rene', 'Tanczos')

**SELECT**

::

    sql = SQL().SELECT('name', 'age', 'size').FROM('users').WHERE('age', '=', 27).AND().WHERE('size', '<', 190).ORDER_BY('age', 'ASC').LIMIT(0, 10)

    print sql.toStr()
    # SELECT name, age, size FROM users WHERE age=? AND size<? ORDER BY age ASC LIMIT 0,10;

    print sql.getValues()
    # (27, 190)

**DELETE**

::

    sql = SQL().DELETE('users').WHERE('id', '=', 4)

    print sql.toStr()
    # DELETE FROM users WHERE id=?;

    print sql.values
    # (4,)

Database
--------

Represents the database.

Usage
~~~~~

First you should set the database file path to your sqlite3 database.

Don't worry if it doesn't exist yet. Sqlite3 automatically creates a
database file on the selected path if it doesn't exists.

::

    from sqlitemodel import Database

Set the path to the database
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

It is recommended to set the path to the database after starting the
application by the static variable inside the *Database* class.

::

    Database.DB_FILE = 'path/to/database.db'

    db = Database()

But the path can be also set inside the *Database* constructor while the
object initializes.

::

    db = Database('path/to/database.db')

**with** statement
^^^^^^^^^^^^^^^^^^

The *Database* class supports the *with* statement whitch is recommended
to use.

::

    with Database() as db:
        users = db.select(SQL().SELECT().FROM('users'))

The database connection get automatically closed after the *with* block
is processed.

Methods
^^^^^^^

All of this method using a *Model* object as first argument, so that the
*Database* object knows how to use it.

::

    close()
    # close connection

    createTable(model)
    # create the database table if not exists by the the model object

    save(model)
    # create or update a model object and return it id

    delete(model)
    # delete a model object and return True/False

    select(model, SQL() | sql query , values=())
    # return a array of the given model

    selectOne(model, SQL() | sql query, values=())
    # return the first matching entry of the given model

    selectById(model, id)
    # return the a model object by his id

But if there is some data without a *Model*, it can be retrieved as
*list* or *list* of *Dict* objects.

::

    getRaw(SQL() | sql query, values=(), max=-1)
    # return an array of results.
    # index 0 is the header of the table

    getDict(SQL() | sql query, values=(), max=-1)
    # return a list array with a Dict object.
    # the key of the Dict object is the column name

Licence
-------

The MIT License (MIT)

Copyright (c) 2016 René Tanczos

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
