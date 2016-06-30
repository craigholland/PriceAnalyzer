from functools import reduce
import datetime as dt

def isNumeric(data, NoEmptyList = True, allow_numbers_as_string=False):
  """Truth value testing to check if value is float/int.

  Data can be singular value or list/tuple of values.  Function
  can handle nested sets, but empty lists will return False (unless
  NoEmptyList is switched to False)
  """
  def isValNumeric(val):
    try:
      float(val)
      if isinstance(val, bool):
        return False
      if isinstance(val, str) and not allow_numbers_as_string:
        return False
      return True
    except (ValueError, TypeError):
      return False
  if isList(data):
    result = True
    if data or not NoEmptyList:
      for idx in data:
        result = result and isNumeric(idx)
    else:
      result = False
    return result
  else:
    return isValNumeric(data)

def isType(data, data_type, NoEmptyList = True):
  """Truth value testing to check if value is of data_type.

  Data can be a singular value or list/tuple of values.  Function
  can handle nested sets, but empty lists will return False (unless
  NoEmptyList is switched to False)
  """
  if isinstance(type(data_type), type):
    if isList(data):
      if data and NoEmptyList:
        return reduce((lambda x, y: x and y), map(lambda i: isinstance(i, data_type), data))
      elif not NoEmptyList:
        return True
      return False
    else:
      return isinstance(data, data_type)
  else:
    #Error Handling here for bad data type
    return False



def isList(val):
  if isinstance(val, list) or isinstance(val, tuple):
    return True
  return False

def isTimestamp(val):
  if isinstance(val, dt.datetime):
    return True
  return False
