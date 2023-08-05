import time
import multiprocessing as mlt

import MySQLdb
from pysqlite2 import dbapi2 as sqlite

from generaltools import log_tools
from generaltools.server_tools import GeneralServer


class BaseDB(object):
    """ Wrapper class around MySQLdb"""
    def __init__(self, database=None, user=None, host=None, password=None,
                 lock=False, sqlite_filename=None, sqlite=False, **kwargs, log=False):
        if not self.log:
            self.log = log_tools.init_logger("/var/log/db_log")
        else:
            self.log = log
        self.check_lock = lock or mlt.Lock()
        self.database = database
        self.user = user
        self.host = host
        self.password = password
        self.conn = MySQLdb.connect(host=self.host, user=self.user,
                                    passwd=self.password, db=self.database)
        self.cursor = self.conn.cursor()

    def execute(self, sql):
        success=False
        i=0
        while not success:
            try:
                self.cursor.execute(sql)
                success=True
            except OperationalError as e:
                i +=1
                self.log.error("failed to execute will try again {0}" \
                               "\nFollowing error {1}".format(i, str(e)))
                time.sleep(1)
        return self.cursor

    def execute(self, sql):
        """Run and SQL command"""
        self.log.info(sql)
        self.cursor.execute(sql)
        return self.cursor

    def commit(self):
        """Commit changes to the database"""
        self.conn.commit()

    def close_connection(self):
        """Close the database connection"""
        self.conn.close()


class GenDB(BaseDB):
    """ Providing basic procedures to work with databases"""
    def __init__(self):
        BaseDB.__init__(self)
        self.tables = None

    def drop_table(self, table_name):
        """Drop table with table_name"""
        self.execute('SET FOREIGN_KEY_CHECKS = 0;')
        sql = "DROP table if exists {}".format(table_name)
        try:
            self.execute(sql)
        except MySQLdb.ProgrammingError:
            self.log.error("can not drop table does it exists")
        self.execute('SET FOREIGN_KEY_CHECKS = 1;')
        self.commit()

    def update_table_list(self):
        """get a list of existing tables"""
        sql = "SHOW TABLES"
        self.execute(sql)
        self.tables = self.cursor.fetchall()
        self.tables = [table[0] for table in self.tables]

    def check_if_table_exists(self, table_name):
        """Check if table with table_name exists"""
        self.update_table_list()
        if table_name in self.tables:
            return True
        else:
            return False

    def add_column_to_table(self, table_name, column_name, column_type):
        """Add a column to the table"""
        sql = "ALTER TABLE {} ADD COLUMN {} {} "\
              "DEFAULT NULL".format(table_name, column_name, column_type)
        self.execute(sql)
        self.commit()

    def get_column_names(self, table_name):
        """Read the names of the columns of a table"""
        if self.type_ == "MySQL":
            sql = "describe {}".format(table_name)
        if self.type_ == "SQLLite":
            sql = "describe {}".format(table_name)
        self.execute(sql)
        names = [str(name[0]) for name in self.cursor.fetchall()]
        return names

    def add_table(self, table_name, columns):
        """Add a new table to the database if it does not exist

        Parameters
        ----------
        table_name : str
            The name of the table
        columns : dict
            Dictionary with the names of the colums as keys and the type as
            lookup values.

        """
        sql = "CREATE TABLE if not exists {} "\
              "(id INT PRIMARY KEY NOT NULL AUTO_INCREMENT ".format(table_name)
        for column in columns.keys():
            sql += ", {} {}".format(column, columns[column])
        sql += ")"
        self.execute(sql)
        self.commit()

class MySQLConnection(GenDB):
    def __init__(self, database=None, user=None, host=None,
                 password=None):
        GenDB.__init__(self)
        self.database = database
        self.user = user
        self.host = host
        self.password = password
        self.conn = MySQLdb.connect(host=self.host, user=self.user,
                                    passwd=self.password, db=self.database)
        self.cursor = self.conn.cursor()
        self.type_ = "MySQL"

class SQLLiteConnection(GenDB):
    def __init__(self, file_name=None):
        GenDB.__init__(self)
        self.conn = sqlite.connect(file_name)
        self.cursor = self.conn.cursor()
        self.type_ = "SQLLite"
