import json
import datetime
from pytz import tzinfo
import pytz
from digitalocean import Droplet


class DefaultResultEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            # return obj.strftime('%Y-%m-%d %H:%M:%S')
            return obj.isoformat()
        elif isinstance(obj, datetime.date):
            # return obj.strftime('%Y-%m-%d')
            return obj.isoformat()
        elif isinstance(obj, tzinfo.DstTzInfo):
            return str(obj)
        elif isinstance(obj, datetime.timedelta):
            return str(obj)
        elif isinstance(obj, Droplet):
            return json.loads(json.dumps(obj.__getstate__(), cls=DefaultResultEncoder, ensure_ascii=False, indent=2))
        try:
            json.dumps(obj)
        except TypeError:
            return str(obj)
        return json.JSONEncoder.default(self, obj)


def json_dumps_format(data: dict):
    return json.dumps(data, cls=DefaultResultEncoder, ensure_ascii=False, indent=2)


def task_data_encode(data):
    if isinstance(data, list):
        for i in range(len(data)):
            data[i] = task_data_encode(data[i])
    elif isinstance(data, dict):
        for k in data:
            data[k] = task_data_encode(data[k])
    elif isinstance(data, tzinfo.DstTzInfo):
        # data = f"timezone|{str(data.__repr__())}"
        data = f"timezone|{str(data)}"
        # data = f"timezone|"
    elif isinstance(data, datetime.timedelta):
        data = f"timedelta|{str(data.total_seconds())}"
    elif isinstance(data, datetime.datetime):
        data = f"datetime|{data.isoformat()}"
    elif isinstance(data, datetime.date):
        data = f"date|{data.isoformat()}"
    return data


pymongo_timedelta_tz = pytz.timezone('Asia/Shanghai')


def task_data_decode(data):
    global pymongo_timedelta_tz
    if isinstance(data, list):
        for i in range(len(data)):
            data[i] = task_data_decode(data[i])
    elif isinstance(data, dict):
        for k in data:
            data[k] = task_data_decode(data[k])
    elif isinstance(data, str):
        if data.startswith('timezone|'):
            # print('timezone: ', data)
            # tz = tzinfo.BaseTzInfo()
            # tz = tzinfo.DstTzInfo(tz)
            # tz.zone = data[len('timezone|'):]
            data = pytz.timezone(data[len('timezone|'):])
            pymongo_timedelta_tz = data
        elif data.startswith('timedelta|'):
            # print('timedelta: ', data)
            data = datetime.timedelta(seconds=float(data[len('timedelta|'):]))
        elif data.startswith('datetime|'):
            data = datetime.datetime.fromisoformat(data[len('datetime|'):])
            data = data.replace(tzinfo=pymongo_timedelta_tz)
            # data = pymongo_timedelta_tz.fromutc(data)
        elif data.startswith('date|'):
            data = datetime.date.fromisoformat(data[len("date|"):])
            # data = data.replace(tzinfo=pymongo_timedelta_tz)
            # data = pymongo_timedelta_tz.fromutc(data)
    elif isinstance(data, datetime.datetime):
        data = data.replace(tzinfo=pymongo_timedelta_tz)
        data = pymongo_timedelta_tz.fromutc(data)
    return data

# def serialize_time_value(value):
#     if isinstance(value, datetime.datetime):
#         return value.replace(microsecond=0).isoformat()
#     if isinstance(value, datetime.date):
#         return value.isoformat()
#     elif isinstance(value, tzinfo.DstTzInfo):
#         return str(value)
#     elif value is None:
#         return None
#     else:
#         return str(value)
