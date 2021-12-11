from flask_restful import Resource, reqparse
from utils.args_decorators import args_required_method
from utils.make_result import make_result
from data.config import Statics
import exceptions

args_selector = reqparse.RequestParser() \
    .add_argument("limit", type=int, required=False, location=["args", ]) \
    .add_argument("offset", type=int, required=False, location=["args", ])
