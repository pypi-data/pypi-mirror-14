import psycopg2
import psycopg2.extensions

class Database:
    def __init__(self, config=None,profile=None):
        try:
            self.conn = psycopg2.connect(config.dsn())
            self.cur = self.conn.cursor()
        except psycopg2.OperationalError as e:
            print('Could not get a database connection' + e.pgerror)
    def __del__(self):
        self.conn.close()
    def execute(self,sql):
        try:
            self.conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
            self.cur.execute(sql)
        except psycopg2.Error as e:
            self.conn.rollback()
            return e
        else:
            return True
    def fetchall(self,sql):
        try:
            self.conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
            self.cur.execute(sql)
            return self.cur.fetchall()
        except psycopg2.Error as e:
            return e
    def executemany(self,sql):
        try:
            for command in sql:
                self.conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED)
                self.cur.execute(command)
                print(self.cur.rowcount)
        except psycopg2.Error as e:
            self.conn.rollback()
            return e
        else:
            self.conn.commit()
            return True