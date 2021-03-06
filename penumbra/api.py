from flask.ext.restless import APIManager
from penumbra import app, db
from penumbra.models import Host, Datum
from penumbra.auth import AUTH_MECHANISM, AUTH_MAP

manager = APIManager(app, flask_sqlalchemy_db=db)

host_blueprint = manager.create_api(Host, 
    methods=['GET', 'POST', 'DELETE'],
    exclude_columns = ['data'], 
    preprocessors = {
      'GET_SINGLE': AUTH_MAP['GET_SINGLE'],
      'GET_MANY': AUTH_MAP['GET_MANY'],
    },
)
datum_blueprint = manager.create_api(Datum,
    exclude_columns = ['_value', 'key', 'host'],
)
