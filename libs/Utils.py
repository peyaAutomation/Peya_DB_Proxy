import json
from datetime import date, datetime
from dotenv.main import DotEnv


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


class Utils:

    @staticmethod
    def json_response(data):
        return json.dumps(data, indent=4, sort_keys=True, default=json_serial)

    @staticmethod
    def get_env_var(var_name):
        dot_env = DotEnv('.env')
        return dot_env.get(var_name)
