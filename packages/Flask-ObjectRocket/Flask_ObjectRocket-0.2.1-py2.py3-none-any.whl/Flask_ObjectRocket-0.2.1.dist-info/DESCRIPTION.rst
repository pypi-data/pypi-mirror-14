[![Circle CI](https://circleci.com/gh/objectrocket/Flask-ObjectRocket.svg?style=svg)](https://circleci.com/gh/objectrocket/Flask-ObjectRocket) [![codecov.io](https://codecov.io/github/objectrocket/Flask-ObjectRocket/coverage.svg?branch=master)](https://codecov.io/github/objectrocket/Flask-ObjectRocket?branch=master) [![Coverage Status](https://coveralls.io/repos/github/objectrocket/Flask-ObjectRocket/badge.svg?branch=master)](https://coveralls.io/github/objectrocket/Flask-ObjectRocket?branch=master)

Flask-ObjectRocket
==================
A Flask / Flask-RESTful extension implementing support for user authentication with the ObjectRocket API.

#### install
This package is distributed on pypi. You can install it via pip:
```bash
pip install flask-objectrocket
```

#### configuration & usage
Configure this extension as you would any other Flask extension:

```python
from flask import Flask
from flask.ext.objectrocket import ObjectRocket

app = Flask(__name__)
app.config.from_pyfile('app-config.cfg')

# Initialize the extension with init_app.
objectrocket = ObjectRocket()
objectrocket.init_app(app)

# Or initialize the extension directly.
objectrocket = ObjectRocket(app)
```

The following Flask configuration attributes are available for this extension:
```python
# The ObjectRocket APIv2 URL (you should never have to change this).
OBJECTROCKET_BASE_URL = None
# Bind the authenticated user object to flask.g.user for request duration.
OBJECTROCKET_BIND_USER = True
# Cache the authenticated user's instances to flask.g.instances for request duration.
OBJECTROCKET_BIND_INSTANCES = True
```

Now that the extension is initialized, use it with [Flask-RESTful](http://flask-restful.readthedocs.org/en/latest/):

```python
from flask.ext.objectrocket import ObjectRocketResource

class MyResource(ObjectRocketResource):
    """All of this resource's handlers are now protected with ObjectRocket token authentication."""

    def get(self):
        ...

    def post(self):
        ...
```

If you are not using Flask-RESTful, you can also use the [objectrocket_authentication](https://github.com/objectrocket/Flask-ObjectRocket/blob/master/flask_objectrocket.py) decorator and the [ObjectRocketUser](https://github.com/objectrocket/Flask-ObjectRocket/blob/master/flask_objectrocket.py) class directly.

#### tests
`tox` should get you where you need to be. As of this writing, test coverage is at `100%`. It is a good idea to keep it that way.

#### license
Flask-ObjectRocket is distributed under MIT license, see `LICENSE` for more details.


