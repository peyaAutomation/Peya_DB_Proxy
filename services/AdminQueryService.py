from peewee import DoesNotExist

from models.models import QueryEntity


class AdminQueryService:

    @staticmethod
    def list_all_queries():
        try:
            return QueryEntity().select().dicts().get()
        except DoesNotExist:
            return []

    @staticmethod
    def get_one_query_by_id(query_id):
        return QueryEntity().select().where(QueryEntity.id == query_id).dicts().first()

    @staticmethod
    def get_one_query_by_name(query_name):
        return QueryEntity().select().where(QueryEntity.name == query_name).dicts().first()

    @staticmethod
    def create_query(query_data):
        query = QueryEntity()
        query.name = query_data['name']
        query.query = query_data['query']
        query.save()

    @staticmethod
    def edit_query_by_id(query_id, query_data):
        query = QueryEntity().select().where(QueryEntity.id == query_id).first()

        query.name = query_data['name']
        query.query = query_data['query']

        query.save()

    @staticmethod
    def edit_query_by_name(query_name, query_data):
        query = QueryEntity().select().where(QueryEntity.name == query_name).first()

        query.name = query_data['name']
        query.query = query_data['query']

        query.save()

    @staticmethod
    def delete_query_by_id(query_id):
        QueryEntity().get_by_id(query_id).delete().execute()

    @staticmethod
    def delete_query_by_name(query_name):
        QueryEntity().select().where(QueryEntity.name == query_name).first().delete().execute()
