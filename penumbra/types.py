import formencode
from formencode.validators import Int, String, StringBool, Number

def validate_document(x):
    assert isinstance(x, dict), 'must be a document'
    return str(x)

TYPES = {
  'float': Number.to_python,
  'int': Int.to_python,
  'string': String.to_python,
  'document': validate_document,
  'boolean': StringBool.to_python,
}
