import mysql
from mysql.connector import MySQLConnection

from libs.Utils import Utils


class MySQLDriver:
    database: MySQLConnection

    def connect(self):
        self.database = mysql.connector.connect(
            user=Utils.get_env_var('MY_SQL_USER'),
            password=Utils.get_env_var('MY_SQL_PASS'),
            host=Utils.get_env_var('MY_SQL_HOST'),
            port=int(Utils.get_env_var('MY_SQL_PORT')),
            database=Utils.get_env_var('MY_SQL_DATABASE')
        )

    def execute_query(self, query, alternative_result_mapping, data):
        cursor = self.database.cursor(named_tuple=True)
        cursor.execute(query, data)

        if cursor.description is None:
            self.database.commit()
            result_dict = {"message": "Query executed Successfully", "affectedRows": cursor.rowcount}
        else:
            results = cursor.fetchall()

            if alternative_result_mapping:
                result_dict = []
                for r in results:
                    result_dict.append(dict(zip(cursor.column_names, r)))
            else:
                result_dict = {}
                for i, c in enumerate(cursor.column_names, start=0):
                    result_dict[c] = []
                    for r in results:
                        result_dict[c].append(str(r[i]))
        return result_dict
