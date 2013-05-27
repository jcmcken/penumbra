import datetime
from formencode.validators import Int, String, StringBool, Number

def validate_datetime(x):
    try:
        result = datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S.%f")
    except (ValueError, TypeError), e:
        raise ValueError('datetime must conform to ISO 8601, i.e. "YYYY-MM-DD HH:MM:SS.mmmmmm"')
    return result

# Take arbitrary input, validate, and return an object
#
# To convert back, run ``str`` against the object.
TYPES = {
  'float': Number.to_python,
  'integer': Int.to_python,
  'string': String.to_python,
  'boolean': StringBool.to_python,
  'datetime': validate_datetime,
}
