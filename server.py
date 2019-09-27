from flask_cors import CORS
from flask import Flask, request
from mysql.connector import ProgrammingError
from libs.Utils import Utils
from services.AdminQueryService import AdminQueryService
from services.QueryRunnerService import QueryRunnerService

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

    alternative_result_mapping = False

    if 'alternative_result_mapping' in data.keys():
        alternative_result_mapping = data['alternative_result_mapping']

    try:
        return app.response_class(
            response=Utils.json_response({
                "result": QueryRunnerService.run_custom_query(data['query'], alternative_result_mapping)
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


app.run(host='0.0.0.0', port=4400, debug=True)
