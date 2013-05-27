from penumbra import db
from penumbra.types import TYPES
import datetime
from sqlalchemy.ext.hybrid import hybrid_property

_now = datetime.datetime.now

class TimestampMixin(object):
    """
    A ``db.Model`` mixin that adds an ``updated_at`` and ``created_at``
    field, which are automatically set to the correct value in most instances.
    """
    created_at = db.Column(db.DateTime, default=_now, nullable=False)
    updated_at = db.Column(db.DateTime, 
        onupdate=_now, default=_now, nullable=False)

    def update_timestamp(self):
        self.updated_at = _now()

class BaseMixin(object):
    @property
    def column_names(self):
        return self.__table__.columns.keys()

class Host(BaseMixin, TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=255), nullable=False)
    # IPv4 addresses are a maximum of 15 chars
    ip = db.Column(db.String(length=15), nullable=False)
    data = db.relationship('Datum', backref='host', lazy='dynamic')
    
    __table_args__ = (
        # Each host name/IP combination should be unique
        db.UniqueConstraint('name', 'ip', name='_host_ip_uc'),
    )

    def __repr__(self):
        return "<Host(name=%s, ip=%s)>" % (self.name, self.ip)

class Datum(BaseMixin, TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(length=255), nullable=False)
    # IPv4 addresses are a maximum of 15 chars
    _value = db.Column(db.String(length=15), nullable=False)
    type = db.Column(db.Enum(*TYPES.keys()), nullable=False)
    host_id = db.Column(db.Integer, db.ForeignKey(Host.id), nullable=False)

    __table_args__ = (
        # Each host can only have a single key with a certain name
        db.UniqueConstraint('host_id', 'key', name='_host_key_uc'),
    )

    def __init__(self, key, value, type):
        self.key = key
        self.type = type
        self.value = value

    def __repr__(self):
        return "<Datum(key=%s, value=%s, type=%s)>" % (self.key, self.value, self.type)

    @hybrid_property
    def value(self):
        converter = TYPES.get(self.type)
        return converter(self._value)

    @value.setter
    def value(self, value):
        converter = TYPES.get(self.type)
        self._value = str(converter(value))
