from flask import jsonify
from data.config import Constants
import json
from utils.formats import json_dumps_format


class ResultRules:
    code_message = {
        200: "OK",
        400: "Bad Request",
        404: "The Requested URL Was Not Found",
        403: "Forbidden",
        422: "Bad Token",
        423: "Need to Refresh Access Token",
        424: "Need to Re-login",
        500: "Internal Server Error",
    }


def make_result(code=200, message=None, data=None):
    result = {
        'code': code,
        'data': {},
        'message': message
    }
    if result['message'] is None:
        del result['message']
    if code != 200:
        result['error'] = ResultRules.code_message.get(code, "Unknown Error")
    if data is not None:
        result['data'] = data
    result = json.loads(json_dumps_format(result))
    return result, code


def limit_list(li: list, offset: int = None, limit: int = None):
    offset = offset if offset is not None else 0
    limit = limit if limit is not None else Constants.FIND_LIMIT
    res = li[offset: offset + limit]
    return res
