from flask_cors import CORS
from flask import Flask, request
from mysql.connector import ProgrammingError, errors
from libs.Utils import Utils
from services.AdminQueryService import AdminQueryService
from services.QueryRunnerService import QueryRunnerService

app = Flask(__name__)
CORS(app)


@app.route('/check', methods=["GET"])
def check_server():
    return app.response_class(
        response=Utils.json_response({'message': '', 'status': 'online'}),
        status=200,
        mimetype='application/json'
    )


@app.route('/check_jumper', methods=["GET"])
def check_jumper():
    jumper_status = QueryRunnerService.check_connection()
    if jumper_status:
        response = {'message': '', 'status': 'online'}
        status_code = 200
    else:
        response = {'message': 'Jumper may be offline', 'status': 'offline'}
        status_code = 200

    return app.response_class(
        response=Utils.json_response(response),
        status=200,
        mimetype='application/json'
    )


@app.route('/queries', methods=["GET"])
def list_queries_predefined():
    return app.response_class(
        response=Utils.json_response({
            "result": AdminQueryService.list_all_queries()
        }),
        status=200,
        mimetype='application/json'
    )


@app.route('/queries/<query_id>', methods=["GET"])
def view_query_predefined_by_id(query_id):
    return app.response_class(
        response=Utils.json_response({
            "result": AdminQueryService.get_one_query_by_id(query_id)
        }),
        status=200,
        mimetype='application/json'
    )


@app.route('/queries', methods=["POST"])
def create_query_predefined():
    data = request.json

    required_fields = ['name', 'query']

    for f in required_fields:
        if f not in data.keys():
            return app.response_class(
                response=Utils.json_response({
                    "error": "The field '%s' is required" % f
                }),
                status=400,
                mimetype='application/json'
            )

    return app.response_class(
        response=Utils.json_response({
            "result": AdminQueryService.create_query(data)
        }),
        status=201,
        mimetype='application/json'
    )


@app.route('/queries/<query_id>', methods=["PUT"])
def edit_query_predefined_by_id(query_id):
    data = request.json

    required_fields = ['name', 'query']

    for f in required_fields:
        if f not in data.keys():
            return app.response_class(
                response=Utils.json_response({
                    "error": "The field '%s' is required" % f
                }),
                status=400,
                mimetype='application/json'
            )

    return app.response_class(
        response=Utils.json_response({
            "result": AdminQueryService.edit_query_by_id(query_id, data)
        }),
        status=200,
        mimetype='application/json'
    )


@app.route('/queries', methods=["PUT"])
def edit_query_predefined_by_name():
    name = request.args.get('name')

    if name is None and name != '':
        return app.response_class(
            response=Utils.json_response({
                "error": "The param 'name' is required"
            }),
            status=400,
            mimetype='application/json'
        )

    data = request.json

    required_fields = ['name', 'query']

    for f in required_fields:
        if f not in data.keys():
            return app.response_class(
                response=Utils.json_response({
                    "error": "The field '%s' is required" % f
                }),
                status=400,
                mimetype='application/json'
            )

    return app.response_class(
        response=Utils.json_response({
            "result": AdminQueryService.edit_query_by_name(name, data)
        }),
        status=200,
        mimetype='application/json'
    )


@app.route('/queries/<query_id>', methods=["DELETE"])
def delete_query_predefined_by_id(query_id):
    AdminQueryService.delete_query_by_id(query_id)
    return app.response_class(
        status=204,
        mimetype='application/json'
    )


@app.route('/queries', methods=["DELETE"])
def delete_query_predefined_by_name():
    name = request.args.get('name')

    if name is None and name != '':
        return app.response_class(
            response=Utils.json_response({
                "error": "The param 'name' is required"
            }),
            status=400,
            mimetype='application/json'
        )

    AdminQueryService.delete_query_by_id(name)
    return app.response_class(
        status=204,
        mimetype='application/json'
    )


@app.route('/', methods=["GET"])
def execute_predefined_query():
    name = request.args.get('name')

    if name is None and name != '':
        return app.response_class(
            response=Utils.json_response({
                "error": "The param 'name' is required"
            }),
            status=400,
            mimetype='application/json'
        )

    try:
        return app.response_class(
            response=Utils.json_response({
                "result": QueryRunnerService.run_query_by_name(name)
            }),
            status=200,
            mimetype='application/json'
        )
    except ProgrammingError as error:
        return app.response_class(
            response=Utils.json_response({
                "error": str(error)
            }),
            status=400,
            mimetype='application/json'
        )


@app.route('/', methods=["POST"])
def execute_custom_query():
    data = request.json

    required_fields = ['query']

    for f in required_fields:
        if f not in data.keys():
            return app.response_class(
                response=Utils.json_response({
                    "error": "The field '%s' is required" % f
                }),
                status=400,
                mimetype='application/json'
            )
    lower_query = str.lower(data['query'])
    black_list_statements = ['insert ', 'update ', 'delete ', 'drop table', 'create ',
                             'truncate ', 'backup ', 'alter table']

    if [statement for statement in black_list_statements if (statement in lower_query)]:
        return app.response_class(
            response=Utils.json_response({
                "error": "Forbidden. You can't execute this query."
            }),
            status=403,
            mimetype='application/json'
        )

    alternative_result_mapping = False

    if 'alternative_result_mapping' in data.keys():
        alternative_result_mapping = data['alternative_result_mapping']

    database = 'peyadb'

    if 'data_base' in data.keys():
        database = data['data_base']
        if Utils.get_env_var(str.upper(database)) is None:
            return app.response_class(
                response=Utils.json_response({
                    "error": "Check database name provided"
                }),
                status=403,
                mimetype='application/json'
            )

    try:
        return app.response_class(
            response=Utils.json_response({
                "result": QueryRunnerService.run_custom_query(data['query'], alternative_result_mapping,
                                                              database=database)
            }),
            status=200,
            mimetype='application/json'
        )
    except ProgrammingError as error:
        return app.response_class(
            response=Utils.json_response({
                "error": str(error)
            }),
            status=400,
            mimetype='application/json'
        )
    except errors.DatabaseError as db_error:
        return app.response_class(
            response=Utils.json_response({
                "error": str(db_error)
            }),
            status=400,
            mimetype='application/json'
        )


@app.route('/user/updatephone', methods=["POST"])
def execute_update_user_phone():
    data = request.json
    query = """UPDATE peyadb.user set mobile = %s where email = %s;"""
    required_fields = ['mobile', 'email']

    return __execute(query, data, required_fields)


@app.route('/restaurant/updateaceptspreorder', methods=["POST"])
def execute_update_restaurant_pre_order():
    data = request.json
    query = """UPDATE peyadb.restaurant set accepts_pre_order = %s where name = %s;"""
    required_fields = ['accepts_pre_order', 'name']

    return __execute(query, data, required_fields)


def __get_query_data(required_fields, data):
    query_data = []
    for f in required_fields:
        query_data.append(data[f])
    return tuple(query_data)


def __execute(query, data, required_fields):

    for f in required_fields:
        if f not in data.keys():
            return app.response_class(
                response=Utils.json_response({
                    "error": "The field '%s' is required" % f
                }),
                status=400,
                mimetype='application/json'
            )

    query_data = __get_query_data(required_fields, data)

    alternative_result_mapping = False

    if 'alternative_result_mapping' in data.keys():
        alternative_result_mapping = data['alternative_result_mapping']

    database = 'peyadb'

    if 'data_base' in data.keys():
        database = data['data_base']
        if Utils.get_env_var(str.upper(database)) is None:
            return app.response_class(
                response=Utils.json_response({
                    "error": "Check database name provided"
                }),
                status=404,
                mimetype='application/json'
            )

    try:
        return app.response_class(
            response=Utils.json_response({
                "result": QueryRunnerService.run_custom_query(query, alternative_result_mapping, query_data, database)
            }),
            status=200,
            mimetype='application/json'
        )
    except ProgrammingError as error:
        return app.response_class(
            response=Utils.json_response({
                "error": str(error)
            }),
            status=400,
            mimetype='application/json'
        )
    except errors.DatabaseError as db_error:
        return app.response_class(
            response=Utils.json_response({
                "error": str(db_error)
            }),
            status=400,
            mimetype='application/json'
        )


app.run(host='0.0.0.0', port=4500, debug=True)