"""
The DBcm.UseDatabase context manager for working with MySQL/MariaDB and SQLite3.

The 1.x release of this module was based on code created for the second edition 
of Head First Python. See chapters 7, 8, 9, and 11 of the that book for information
on how this module was created.  

To install the second edition release, please use: pip install DBcm=1.7.4

For the third edition of Head First Python, DBcm moved to release 2. The option to use 
SQLite3 is now supported in this new release.

Simple example usage (for a MySQL/MariaDB backend):

    from DBcm import UseDatabase, SQLError

    config = { "host": "127.0.0.1",
               "user": "myUserid",
               "password": "myPassword",
               "database": "myDB" }

    with UseDatabase(config) as cursor:
        try:
            _SQL = "select * from log"
            cursor.execute(_SQL)
            data = cursor.fetchall()
        except SQLError as err:
            print("Your query caused an issue:", str(err))

If a filename (string) is used in place of a config dictionary when using 
DBcm.UseDataBase, the data is assumed to reside in a local SQLite file (which
gets created if it doesn't previously exist).
"""

##############################################################################
# Context manager for connecting/disconnecting to a database.
##############################################################################

import mysql.connector  # An external dependency.
import sqlite3  # Included with the PSL.


class ConnectionError(Exception):
    """Raised if the backend-database cannot be connected to."""

    pass


class CredentialsError(Exception):
    """Raised if the database is up, but there's a login issue."""

    pass


class SQLError(Exception):
    """Raised if the query caused problems."""

    pass


class UseDatabase:
    def __init__(self, config):
        """Add the database configuration parameters to the object.

        A dictionary (MySQL/MariaDB) or string (SQLite) is supplied in "config".

        String case: a filename identifying the local SQLite database.

        Dictionary case: a single dictionary argument which needs to assign
        the appropriate values to (at least) the following keys:

            host - the IP address of the host running MariaDB.
            user - the MariaDB username to use.
            password - the user's password.
            database - the name of the database to use.

        """
        if isinstance(config, dict):
            self.configuration = config
            self.type = "MySQL"
        elif isinstance(config, str):
            self.dbfilename = config
            self.type = "SQLite3"
        else:
            raise TypeError("DBcm error: Only dict or str allowed here.")

    def __enter__(self):
        """Connect to the database and create a DB cursor.

        Return the database cursor to the context manager.
        Raise ConnnectionError if the database can't be found.
        Raise CredentialsError if the wrong username/password used.
        """
        if self.type == "MySQL":
            try:
                self.conn = mysql.connector.connect(**self.configuration)
            except mysql.connector.InterfaceError as err:
                raise ConnectionError(err) from err
            except mysql.connector.ProgrammingError as err:
                raise CredentialsError(err) from err
        elif self.type == "SQLite3":
            self.conn = sqlite3.connect(self.dbfilename)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """Destroy the cursor as well as the connection (after committing).

        Raise ProgrammingError as an SQLError, and re-raise anything else
        as required.
        """
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
        if exc_type is mysql.connector.ProgrammingError:
            raise SQLError(exc_value)
        elif exc_type:
            raise exc_type(exc_value)
