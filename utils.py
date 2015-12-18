import datetime


def json_serializer(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    raise TypeError ('Type {} not serializable'.format(type(obj)))

