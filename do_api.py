from utils.api_tools import *
from digitalocean import TokenError
from do_cli import DoCli
from utils.logger import logger


class DoCliAPI(Resource):
    """
    API for do-cli
    """

    args_get = reqparse.RequestParser(bundle_errors=True) \
        .add_argument("Token", help="token of your digital ocean api", type=str, required=True, location=["headers", ]) \
        .add_argument("name", help="name to use filter (fetch all if None)", type=str, required=False,
                      location=["args", ])

    args_post = reqparse.RequestParser(bundle_errors=True) \
        .add_argument("Token", help="token of your digital ocean api", type=str, required=True, location=["headers", ]) \
        .add_argument("name", help="name of droplet", type=str, required=True, location=["json", ]) \
        .add_argument("region", help="region of droplet", type=str, required=True, location=["json", ]) \
        .add_argument("image", help="image of droplet", type=str, required=False, location=["json", ]) \
        .add_argument("size_slug", help="size of droplet", type=str, required=False, location=["json", ]) \
        .add_argument("backups", help="enable backup", type=bool, required=False, location=["json", ])

    args_delete = reqparse.RequestParser(bundle_errors=True) \
        .add_argument("Token", help="token of your digital ocean api", type=str, required=True, location=["headers", ]) \
        .add_argument("name", help="name of droplet (destroy all if None)", type=str, required=False,
                      location=["args", ])

    @args_required_method(args_get)
    def get(self):
        """
        Get your droplet list
        :return: droplets: List[Droplet]
        """
        args = self.args_get.parse_args()
        args = {k.lower(): args[k] for k in args}
        token, name = args.get('token'), args.get('name')
        try:
            cli = DoCli(token=token, local_token=True, no_upload_keys=True, quiet=True)
            droplets = [droplet.__getstate__() for droplet in cli.find_droplets(name=name)]
            # for d in droplets:
            #     try:
            #         if '_log' in d:
            #             del d['_log']
            #         if '_session' in d:
            #             del d['_session']
            #     except Exception as e:
            #         logger.error(f"{e}")
        except TokenError:
            return make_result(403, message='Token error')
        return make_result(data={"droplets": droplets})

    @args_required_method(args_post)
    def post(self):
        """
        Create a droplet
        :return: droplet: droplet info
        """
        args = self.args_post.parse_args()
        args = {k.lower(): args[k] for k in args}
        token = args.get('token')
        del args['token']
        try:
            cli = DoCli(token=token, local_token=True, no_upload_keys=True, quiet=True)
            cli.create(**args, with_keys=True, wait_complete=True)
        except TokenError:
            return make_result(403, message='Token error')
        return make_result(data={
            "droplet": cli.find_droplet(name=args.get('name'))
        })

    @args_required_method(args_delete)
    def delete(self):
        """
        Destroy your droplet
        :return:
        """
        args = self.args_delete.parse_args()
        args = {k.lower(): args[k] for k in args}
        token, name = args.get('token'), args.get('name')
        del args['token']
        try:
            cli = DoCli(token=token, local_token=True, no_upload_keys=True, quiet=True)
            cli.destroy(name=name, wait_complete=True)
        except TokenError:
            return make_result(403, message='Token error')
        return make_result()
