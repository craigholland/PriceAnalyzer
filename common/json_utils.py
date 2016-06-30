"""Utilities for working with JSON."""

import collections

import datetime
import decimal
import json


DEFAULT_SEPARATORS = (', ', ': ')

COMPACT_SEPARATORS = (',', ':')

INDENT_SEPARATORS = (',', ': ')


class EncoderPlus(json.JSONEncoder):
  """Encodes datatime, decimal and other types."""

  pass


def Dump(obj, **kwargs):
  """Serialize a Python object into a JSON string.

  Args:
    obj: *, The object to serialize.
    **kwargs: dict, Inherited keyword arguments.

  Returns:
    The serialized JSON string.
  """
  kwargs.setdefault('cls', EncoderPlus)
  kwargs.setdefault('separators', COMPACT_SEPARATORS)
  kwargs.setdefault('sort_keys', True)
  return json.dumps(obj, **kwargs)


# Just an alias because we don't need a custom JSONDecoder yet.
Load = json.loads  # pylint: disable=g-bad-name


# A sentinel default value.
_SENTINEL = object()


def GetPath(obj, path, default=None):
  """Retrieves a value from a nested mapping by key path.

  Example:
    GetPath({'a': {'b': {'c': 'foo'}}}, 'a.b.c') == 'foo'

  Args:
    obj: dict, the dict to query.
    path: str, the path to query.
    default: *, optional default value to return if path isn't found.

  Returns:
    The value if it exists, otherwise None.
  """
  result = obj
  for k in path.split('.'):
    if isinstance(result, collections.Mapping):
      result = result.get(k, _SENTINEL)
    else:
      return default
  return default if result is _SENTINEL else result


def Get(mapping, key, default):
  """Decode the value for a key in a dict-like object.

  Args:
    mapping: dict-like object, something that has a __getitem__ method.
    key: *, some key that may be in the dict.
    default: *, returned if the key is absent, non-optional.

  Returns:
    The JSON-decoded value if it exists, otherwise default.
  """
  try:
    value = mapping[key]
  except KeyError:
    return default
  return Load(value)

def GetServerDataPath(*paths):
  """Returns absolute path to resource in the server directory."""
  return os.path.join(resources.GetRunfilesDir(),
                      constants.SERVER_BASE_PATH, *paths)

def LoadTestDataJson(test_data_path):
  """Locate and load test data.

  Args:
    test_data_path: String path relative to the netdesign/server folder.
                    e.g. 'locations/testdata/building.json'

  Returns:
    list<dict>: A list of model test data.
  """
  with open(GetServerDataPath(test_data_path)) as f:
    return json_utils.Load(f.read())


