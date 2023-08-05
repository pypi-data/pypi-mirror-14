# -*- coding: utf-8 -*-

from threading import local

_user = local()


class CurrentUserMiddleware(object):
    def process_request(self, request):
        _user.value = request.user


def get_current_user():
    return _user.value if hasattr(_user, 'value') else None


def get_current_user_id():
    current_user = get_current_user()
    return current_user.id if current_user else 0
