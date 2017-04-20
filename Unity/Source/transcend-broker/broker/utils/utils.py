import json


def jsonify(data):
    """
    Convert a Python dictionary into a JSON string

    :param data: Python dictionary
    :return: JSON String
    """

    return json.dumps(data)


def unjsonify(data):
    """
    Convert a JSON string into a Python dictionary

    :param data: JSON String
    :return: Success: Python dictionary
             Failure: None
    """

    try:
        data = data.replace("'", '"')
        return json.loads(data)

    except json.decoder.JSONDecodeError:
        return None
