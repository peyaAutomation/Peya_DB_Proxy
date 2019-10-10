import mysql
from mysql.connector import MySQLConnection

from libs.Utils import Utils


class MySQLDriver:
    database: MySQLConnection

    def connect(self, database='peyadb'):
        prefix = Utils.get_env_var(str.upper(database))

        self.database = mysql.connector.connect(
            user=Utils.get_env_var('MY_SQL_USER' + prefix),
            password=Utils.get_env_var('MY_SQL_PASS' + prefix),
            host=Utils.get_env_var('MY_SQL_HOST' + prefix),
            port=int(Utils.get_env_var('MY_SQL_PORT' + prefix)),
            database=Utils.get_env_var('MY_SQL_DATABASE' + prefix)
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
