from types import MethodType
import requests


class MixCloudError(Exception):
    pass


def check_response(response):
    from client import MixcloudObject
    if 'error' in response:
        raise MixCloudError(response['error'])
    else:
        return MixcloudObject(response)


def get_next_paging(obj):
    return check_paging(obj, requests.get(obj.paging.next).json())


def get_previous_paging(obj):
    return check_paging(obj, requests.get(obj.paging.previous).json())


def check_paging(cls, response):
    obj = check_response(response)
    if response['paging'].get('next', None):
        obj.next_paging = MethodType(get_next_paging, obj)
    if response['paging'].get('previous', None):
        obj.previous_paging = MethodType(get_previous_paging, obj)
    return obj
