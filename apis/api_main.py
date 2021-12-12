import json
from flask import Flask, Response
from flask_cors import CORS
from flask_restful import Resource, Api
from utils.logger import logger
from utils.make_result import make_result
from utils.docs import get_class_docs
from do_api import DoCliAPI


class MainAPI(Resource):
    """
    Document test
    """

    def get(self):
        """
        Get all docs for APIs
        """
        return make_result(data={'document': {endpoint: get_class_docs(resources[endpoint]) for endpoint in resources}})


resources = {}


def add_resource(class_type: Resource, endpoint: str):
    global resources
    resources[endpoint] = class_type


def apply_resource():
    for endpoint in resources:
        api.add_resource(resources[endpoint], endpoint)


app = Flask(__name__)
api = Api(app)
add_resource(MainAPI, '/docs')
add_resource(DoCliAPI, '/')
apply_resource()

CORS(app)


@app.after_request
def api_after(res: Response):
    if len(res.data) > 0:
        try:
            js = json.loads(res.data)
            js['code'] = res.status_code
            res.data = json.dumps(js).encode()
            if js['code'] != 200:
                logger.warning(f'response: {js}')
        except Exception as e:
            logger.error(e)
            logger.error(f'data: {res.data}')
        # print(res.data)
    return res


if __name__ == '__main__':
    app.run()
