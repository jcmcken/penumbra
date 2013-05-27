import datetime
from formencode.validators import Int, String, StringBool, Number
from formencode.api import Invalid
from penumbra.exc import InvalidDataType

def validate_datetime(x):
    if isinstance(x, datetime.datetime):
        result = x
    else:
        try:
            result = datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S.%f")
        except (ValueError, TypeError), e:
            raise InvalidDataType('datetime must conform to ISO 8601, i.e. "YYYY-MM-DD HH:MM:SS.mmmmmm"')
    return str(result) # datetime objects are not JSON-serializable

def _wrap_formencode(func):
    def wrapped(x):
        try:
            func(x)
        except Invalid, e:
            raise InvalidDataType(e.args[0])
    return wrapped

# Take arbitrary input, validate, and return an object
#
# To convert back, run ``str`` against the object.
TYPES = {
  'float': _wrap_formencode(Number.to_python),
  'integer': _wrap_formencode(Int.to_python),
  'string': _wrap_formencode(String.to_python),
  'boolean': _wrap_formencode(StringBool.to_python),
  'datetime': validate_datetime,
}
