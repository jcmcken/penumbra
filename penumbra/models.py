import datetime
from penumbra import db
from penumbra.types import TYPES

class TimestampMixin(object):
    """
    A ``db.Model`` mixin that adds an ``updated_at`` and ``created_at``
    field, which are automatically set to the correct value in most instances.
    """
    created_at = db.Column(db.DateTime, default=datetime.datetime.now, nullable=False)
    updated_at = db.Column(db.DateTime, 
        onupdate=datetime.datetime.now, default=datetime.datetime.now, nullable=False)

    def update_timestamp(self):
        self.updated_at = datetime.datetime.now()

class BaseMixin(object):
    @property
    def column_names(self):
        return self.__table__.columns.keys()

class Host(BaseMixin, TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(length=255), nullable=False)
    # IPv4 addresses are a maximum of 15 chars
    ip = db.Column(db.Unicode(length=15), nullable=False)
    data = db.relationship('Datum', backref='host', lazy='dynamic')

    def __repr__(self):
        return "<Host(name=%s, ip=%s)>" % (self.name, self.ip)

class Datum(BaseMixin, TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.Unicode(length=255), nullable=False)
    # IPv4 addresses are a maximum of 15 chars
    value = db.Column(db.Unicode(length=15), nullable=False)
    type = db.Column(db.Enum(*TYPES.keys()), nullable=False)
    host_id = db.Column(db.Integer, db.ForeignKey(Host.id))

    def __repr__(self):
        return "<Datum(key=%s, value=%s, type=%s)>" % (self.key, self.value, self.type)
