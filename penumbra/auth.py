from flask import request, abort
from penumbra import app
from functools import wraps

LOG = app.logger

ADMINISTRATIVE_USERS = app.config.get('ADMINISTRATIVE_USERS', [])
ADMINISTRATIVE_GROUPS = app.config.get('ADMINISTRATIVE_GROUPS', [])

class RemoteUserManager(object):
    def __init__(self):
        self.remote_user = request.headers.get('REMOTE_USER', None)
        self.remote_groups = request.headers.get('REMOTE_GROUPS', [])

    def _is_administrator(self):
        return self.remote_user in ADMINISTRATIVE_USERS or \
            bool(set(self.remote_groups).intersection(ADMINISTRATIVE_GROUPS))

    def _is_in_group(self, group):
        return group in self.remote_groups

    def is_administrator(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if self._is_administrator():
                result = func(*args, **kwargs)
            else:
                LOG.info("user '%s' is not authenticated as an administrator!" % self.remote_user)
                result = abort(403)
            return result
        return wrapper

    def is_in_group(self, group):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                if self._is_in_group(group):
                    result = func(*args, **kwargs)
                else:
                    LOG.info("user '%s' is not a part of group '%s'!" % (self.remote_user, group))
                    result = abort(403)
                return result
            return wrapper
        return decorator
