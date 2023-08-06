"""User authentication with the ObjectRocket API."""
import copy
import functools

from flask import request
from flask import g
from flask.ext.restful import abort
from flask.ext.restful import Resource

from objectrocket import Client

#: The base URL of the environment.
objectrocket_base_url = None

#: Bind the authenticated ObjectRocket user to flask.g.
objectrocket_bind_user = True

#: Bind a cached copy of the authenticated ObjectRocket user's instances to flask.g.
objectrocket_bind_instances = True


class ObjectRocket(object):

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        global objectrocket_base_url, objectrocket_bind_user, objectrocket_bind_instances
        self.app = app
        objectrocket_base_url = app.config.setdefault('OBJECTROCKET_BASE_URL', None)
        objectrocket_bind_user = app.config.setdefault('OBJECTROCKET_BIND_USER', True)
        objectrocket_bind_instances = app.config.setdefault('OBJECTROCKET_BIND_INSTANCES', True)


def objectrocket_authentication(func):
    """RESTful middleware for authentication with ObjectRocket APIv2."""

    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        try:
            # Extract and evaluate credentials.
            token = request.headers.get('x-auth-token', None)
            if token is None:
                raise ValueError('No credentials provided.')

            # Verify token with APIv2.
            client_kwargs = {'base_url': objectrocket_base_url} if objectrocket_base_url else {}
            user_data = Client(**client_kwargs).auth._verify(token)
            if user_data is None:
                raise ValueError('Invalid credentails provided.')

            # Bind the user object for the duration of this request.
            if objectrocket_bind_user:
                g.user = ObjectRocketUser(user_data=user_data, token=token)

            # Cache the user's instances for the duration of this request.
            if objectrocket_bind_instances:
                g.instances = []

        except ValueError as ex:
            abort(401, message=str(ex))

        return func(*args, **kwargs)

    return wrapped


class ObjectRocketResource(Resource):
    """A RESTful resource enforcing token authentication with the ObjectRocket API.

    Ensure this is one of the first resources in inheritance tree to guarantee that
    authentication & authorization takes place before other middleware handlers.
    """

    @property
    def method_decorators(self):
        # Elements later in the list wrap earlier elements.
        decorators = super(ObjectRocketResource, self).method_decorators
        return [objectrocket_authentication] + decorators


class ObjectRocketUser(object):

    def __init__(self, user_data, token):
        user_data = copy.deepcopy(user_data)
        uid = user_data.pop('_id', None) or user_data.pop('id', None)
        login = user_data.pop('login', None)
        if not uid or not login:
            raise ValueError(
                'A user ID and login is required for ObjectRocket users.'
            )

        client_kwargs = {'base_url': objectrocket_base_url} if objectrocket_base_url else {}
        self.id = uid
        self.login = login
        self.token = token
        self.__client = Client(**client_kwargs)
        self.__client.auth._token = token

        for key, val in user_data.items():
            if key not in ['id', 'login', 'token', 'client']:
                setattr(self, key, val)

    @property
    def client(self):
        """This users ObjectRocket client object."""
        return self.__client
