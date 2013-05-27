from flask.ext.restless import APIManager
from penumbra import app, db
from penumbra.models import Host, Datum

manager = APIManager(app, flask_sqlalchemy_db=db)

host_blueprint = manager.create_api(Host, methods=['GET', 'POST', 'DELETE'])
datum_blueprint = manager.create_api(Datum)
