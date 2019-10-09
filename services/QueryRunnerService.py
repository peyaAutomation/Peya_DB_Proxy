from libs.MySQL_driver import MySQLDriver
from models.models import QueryEntity


def run_query(query, alternative_result_mapping=False, data=None):
    my_sql_driver = MySQLDriver()
    my_sql_driver.connect()
    return my_sql_driver.execute_query(query=query, alternative_result_mapping=alternative_result_mapping, data=data)


class QueryRunnerService:

    @staticmethod
    def run_query_by_name(query_name, alternative_result_mapping=False):
        query_dict = QueryEntity().select().where(QueryEntity.name == query_name).dicts().first()
        return run_query(query=query_dict['query'], alternative_result_mapping=alternative_result_mapping)

    @staticmethod
    def run_custom_query(query, alternative_result_mapping=False, data=''):
        return run_query(query=query, alternative_result_mapping=alternative_result_mapping, data=data)
