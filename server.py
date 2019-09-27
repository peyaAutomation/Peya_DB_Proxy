from flask_cors import CORS
from flask import Flask, request
from flask_dotenv import DotEnv
from mysql.connector import ProgrammingError
from libs.Utils import Utils
from libs.MySQL_driver import MySQLDriver
from services.AdminQueryService import AdminQueryService

app = Flask(__name__)
CORS(app)


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

    if name is not None and name != '':
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

    request.args.get('user')
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

    if name is not None and name != '':
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
    error = True
    if error:
        return app.response_class(
            response=Utils.json_response({
                "error": "Query not found"
            }),
            status=404,
            mimetype='application/json'
        )
    else:
        return app.response_class(
            response=Utils.json_response({
                "result": ''
            }),
            status=200,
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

    alternative_result_mapping = False

    if 'alternative_result_mapping' in data.keys():
        alternative_result_mapping = data['alternative_result_mapping']

    driver_db = MySQLDriver()
    driver_db.connect()
    try:
        result = driver_db.execute_query(query=data['query'], alternative_result_mapping=alternative_result_mapping)
    except ProgrammingError as error:
        return app.response_class(
            response=Utils.json_response({
                "error": str(error)
            }),
            status=400,
            mimetype='application/json'
        )

    return app.response_class(
        response=Utils.json_response({
            "result": result
        }),
        status=200,
        mimetype='application/json'
    )


app.run(host='0.0.0.0', port=4400, debug=True)
