import os
import sqlparse


class SQL:

    def parse_statements(sql_location):
        if os.path.isfile(sql_location) and os.access(sql_location, os.R_OK):
            file = open(sql_location, 'r')
            content = file.read()
            sql = filter(None,sqlparse.split(content))
            assert isinstance(sql, list)
            return sql
        else:
            print('SQL file not found or not accessible')