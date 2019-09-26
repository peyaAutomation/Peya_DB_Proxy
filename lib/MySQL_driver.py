import os

import mysql
from mysql.connector import MySQLConnection


class MySQLDriver:
    database: MySQLConnection

    def connect(self):
        self.database = mysql.connector.connect(
            user=os.environ['MY_SQL_USER'],
            password=os.environ['MY_SQL_PASS'],
            host=os.environ['MY_SQL_HOST'],
            port=int(os.environ['MY_SQL_PORT']),
            database=os.environ['MY_SQL_DATABASE']
        )

    def execute_query(self, query):
        """

        :rtype: object
        """
        cursor = self.database.cursor(named_tuple=True)
        cursor.execute(query)
        results = cursor.fetchall()
        result_dict = {}

        """
        for r in results:
            result_dict.append(dict(zip(cursor.column_names, r)))
        """

        for i, c in enumerate(cursor.column_names, start=0):
            result_dict[c] = []
            for r in results:
                result_dict[c].append(str(r[i]))

        return result_dict
