import json

from flask_cors import CORS
from flask import Flask, request
from mysql.connector import ProgrammingError

from lib.MySQL_driver import MySQLDriver
from lib.Utils import Utils

app = Flask(__name__)
CORS(app)


@app.route('/', methods=["POST"])
def create_feature():

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

    driver_db = MySQLDriver()
    driver_db.connect()
    try:
        result = driver_db.execute_query(query=data['query'])
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


app.run(host='0.0.0.0', port=4000, debug=True)
