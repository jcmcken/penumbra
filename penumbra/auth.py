from flask import request, abort
from penumbra import app
from functools import wraps

LOG = app.logger

ADMINISTRATIVE_USERS = app.config.get('ADMINISTRATIVE_USERS', [])
ADMINISTRATIVE_GROUPS = app.config.get('ADMINISTRATIVE_GROUPS', [])

class RemoteUserManager(object):
    def __init__(self):
        self._remote_user = None
        self._remote_groups = []

    @property
    def remote_user(self):
        if not self._remote_user:
            self._remote_user = request.headers.get('REMOTE_USER', None)
        return self._remote_user

    @property
    def remote_groups(self):
        if not self._remote_groups:
            self._remote_groups = request.headers.get('REMOTE_GROUPS', [])
        return self._remote_groups

    def _is_administrator(self):
        return self.remote_user in ADMINISTRATIVE_USERS or \
            bool(set(self.remote_groups).intersection(ADMINISTRATIVE_GROUPS))

    def _is_in_group(self, group):
        return group in self.remote_groups

    def is_administrator(self):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                if self._is_administrator():
                    result = func(*args, **kwargs)
                else:
                    LOG.info("user '%s' is not authenticated as an administrator!" % self.remote_user)
                    result = abort(403)
                return result
            return wrapper
        return decorator

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

_MECHANISMS = {
  'remote_user': RemoteUserManager,
}

requires_user = AUTH_MECHANISM = _MECHANISMS.get(app.config.get('AUTH_MECHANISM', 'remote_user'))()

@requires_user.is_administrator()
def auth_get_single(instance_id=None, **kw):
    pass 

AUTH_MAP = {
  'GET_SINGLE': [auth_get_single],
}
