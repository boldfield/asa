from functools import partial
import requests

from asa import config


def get(uri, params=None):
    return _do_requst('get', uri, params=params)


def _do_requst(method, uri, params=None, data=None):
    func = getattr(requests, method)

    if params is not None:
        func = partial(func, params=params)

    if data is not None:
        func = partial(func, data=data)

    conf = config.get()
    url = make_url(uri)
    resp = func(url, headers={'Authorization': 'Bearer {}'.format(conf['api_token'])})
    data = resp.json()
    data = data['data'] if 'data' in data else data
    return data


def make_url(uri):
    conf = config.get()
    return 'https://{}/api/1.0/{}'.format(conf['api_host'], uri.lstrip('/'))
