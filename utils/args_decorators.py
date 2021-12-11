from utils.logger import logger


def args_required_method(parser):
    def decorator(fn):
        def wrapper(*args, **kwargs):
            # logger.warning(f"warpper now: {fn}, {dir(fn)}")
            # if '__inner__' in dir(fn):
            #     logger.error(f"{fn.__inner__}")
            if 'Resource.dispatch_request' in str(fn) or \
                    ('__args_not_required__' in dir(fn) and fn.__args_not_required__ is True) or \
                    ('__inner__' in dir(fn) and (
                            "Resource.dispatch_request" in str(fn.__inner__) or
                            "__args_not_required__" in str(fn.__inner__))):
                return fn(*args, **kwargs)
            args_ = parser.parse_args()
            logger.info(f'args: {args_}')
            return fn(*args, **kwargs)

        wrapper.__inner__ = fn
        wrapper.__args_parser__ = parser
        return wrapper

    return decorator


def args_required(parser):
    def class_builder(cls):
        class NewClass(cls):
            def __getattribute__(self, item):
                attr = super(NewClass, self).__getattribute__(item)
                if '__' not in item and callable(attr):
                    return args_required_method(parser)(attr)
                return attr

        return NewClass

    return class_builder


def args_not_required(fn):
    def wrapper(*args, **kwargs):
        return fn(*args, **kwargs)

    wrapper.__args_not_required__ = True
    return wrapper


def auth_not_required(fn):
    def wrapper(*args, **kwargs):
        return fn(*args, **kwargs)

    wrapper.__auth_not_required__ = True
    return wrapper
