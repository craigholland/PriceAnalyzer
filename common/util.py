import datetime as dt
import validations

def convertTimeStamp(timestamp):
  if validations.isTimestamp(timestamp):
    part1 = int(timestamp.strftime('%s'))
    part2 = int(timestamp.strftime('%f'))
    return float('{0}.{1}'.format(part1, part2))

  if validations.isNumeric(timestamp):
    return dt.datetime.fromtimestamp(timestamp)
  return None

def equalizeTimestamps(ts1, ts2):
  """
  Ensures that timestamp2 (ts2) is of the same form as ts1
  """
  if not (validations.isNumeric(ts1) or validations.isTimestamp(ts1)):
    return None
  if not (validations.isNumeric(ts2) or validations.isTimestamp(ts2)):
    return None

  if validations.isTimestamp(ts1) and not validations.isTimestamp(ts2):
    ts2 = convertTimeStamp(ts2)
  elif validations.isNumeric(ts1) and not validations.isNumeric(ts2):
    ts2 = convertTimeStamp(ts2)

  return ts2


def Timestamp():
  return dt.datetime.now()

