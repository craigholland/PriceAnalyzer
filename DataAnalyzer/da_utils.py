"""Utils associated with Data Analyzer."""
from common import PriceDataMessage as PDM


def DataTransform_fromJSON(data):
  pass

def DataTransform_fromCSV(data):
  pass

def DataTransform(data):
  """Detects Incoming Data format (JSON, CSV, etc)."""
  condition1 = True
  condition2 = True
  if condition1:
    return DataTransform_fromJSON(data)
  elif condition2:
    return DataTransform_fromCSV(data)



