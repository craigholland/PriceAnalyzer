import datetime as dt
import pytz
import validations
from dateutil import relativedelta as rd
import math

from dateutil.parser import parse

LOCAL_TIMEZONE = 'US/Pacific'

class Time(object):
  utc = pytz.utc
  local_tz = pytz.timezone(LOCAL_TIMEZONE)
  epoch_utc_time = utc.localize(pytz.tzinfo._epoch)

  def __init__(self, val=None, tz=None):
    self._inputVal = val
    self._inputTz = tz

    self._date = None
    self._time = None
    self._tz = None

    self.ParseInput(val)

  def __repr__(self):
    return str(self.timestamp)

  @property
  def timestamp(self):
    d = self._date
    t = self._time
    return self._tz.localize(dt.datetime(d.year, d.month, d.day, t.hour, t.minute, t.second, t.microsecond))

  @property
  def asLocal(self):
    return self.timestamp.astimezone(self.local_tz)

  @property
  def asUTC(self):
    return self.timestamp.astimezone(pytz.utc)

  @property
  def asEpoch(self):
    return (self.asUTC - self.epoch_utc_time).total_seconds()

  def _epochToDateConvert(self, val):
    yr_sec = 31556926
    mt_sec = 2629743
    dy_sec = 86400
    hr_sec = 3600
    Rdelta = rd.relativedelta

    if validations.isNumeric(val):
      #print ('Start: {0}'.format(val))
      years = int(math.floor(val/yr_sec))
      val -= years * yr_sec
      #print ('Years: {0}, New Val{1}'.format(years, val))
      months = int(math.floor(val/mt_sec))
      val -= months * mt_sec
      #print ('Months: {0}, New Val{1}'.format(months, val))
      days = int(math.floor(val/dy_sec))
      val -= days * dy_sec
      #print ('Days: {0}, New Val{1}'.format(days, val))
      hours = int(math.floor(val/hr_sec))
      val -= hours * hr_sec
      #print ('Hours: {0}, New Val{1}'.format(hours, val))
      minutes = int(math.floor(val/60))
      val -= minutes * 60
      #print ('Minutes: {0}, New Val{1}'.format(minutes, val))
      seconds = int(math.floor(val))
      micro = int((val - seconds)*100000)
      #print ('Seconds: {0}, New Val{1}'.format(seconds, val))
      #print ('Micro: {0}'.format(micro))

      return self.epoch_utc_time + Rdelta(years=years,
                                              months=months,
                                              days=days,
                                              hours=hours,
                                              minutes=minutes,
                                              seconds=seconds,
                                              microseconds=micro)
    return None




  def _validateTZinp(self, tzinput):
    """returns datetime.tzinfo object."""
    if isinstance(tzinput, dt.tzinfo):
      return tzinput
    else:
      try:
        return pytz.timezone(tzinput)
      except:
        return None


  def _parseInpDT(self, val):
    """Parse Input as a Datetime Object.

    Args:
      val: datetime.datetime
    """
    input_tz = self._validateTZinp(self._inputTz)
    local_tz = self.local_tz
    if input_tz:
      # Use input_tz as dominant/override tz
      if val.tzinfo:
        val = val.astimezone(input_tz)
      else:
        val = input_tz.localize(val).astimezone(input_tz)
    elif val.tzinfo is None:
      # Refactor naive datetime with local timezone
      val = local_tz.localize(val).astimezone(local_tz)
    else:
      # Use embedded tz as default tz
      pass

    self._date, self._time, self._tz = val.date(), val.time(), val.tzinfo

  def ParseInput(self, inp, from_tuple=False):

    # Parse input as datetime object
    if isinstance(inp, dt.datetime):
      self._parseInpDT(inp)

    # Parse input as tuple
    elif isinstance(inp, tuple) and not from_tuple:
      for val in inp:
        self.ParseInput(val, True)

    # Parse input as int/float -- Assume UTC input
    elif validations.isNumeric(inp):
      self.ParseInput(self._epochToDateConvert(inp))

    # Parse input as date or time object
    elif isinstance(inp, dt.date) or isinstance(inp, dt.time):
      input_tz = self._validateTZinp(self._inputTz)
      self._tz = input_tz if (input_tz and not self._tz) else self._tz if self._tz else self.local_tz

      if isinstance(inp, dt.date):
        # Assign date value
        if not self._date:
          self._date = inp

      # Parse input as Time object
      else:
        # Assign time value
        if not self._time:
          self._time = inp

    # Attempt to parse string
    elif isinstance(inp, str):
      try:
        self.ParseInput(parse(inp))
      except:
        self.ParseInput(None, False)

    # No input (or bad input). Create new Timestamp
    elif inp is None:
      input_tz = self._validateTZinp(self._inputTz)
      self._tz = input_tz if (input_tz and not self._tz) else self._tz if self._tz else self.local_tz
      # Create new DT
      new_dt = self._tz.localize(dt.datetime.now())
      self._date = new_dt.date()
      self._time = new_dt.time()
    else:
      # Raise error
      pass






















    # if isinstance(inp, tuple) and len(inp)==2:
    #   for item in inp:
    #     if isinstance(item, datetime.date):
    #       self._date = item
    #     if isinstance(item, datetime.time):
    #       self._time = item
    # elif isinstance(inp, type(datetime.datetime.now())):
    #   if inp.tzinfo is not None and inp.tzinfo != self._tz:
    #     # Convert inp to self._tz
    #     inp = inp.astimezone(self._tz)
    #
    #   self._date = inp.date()
    #   self._time = inp.time()
    # else:
    #   try:
    #     self.ParseInput(parse(inp))
    #   except:
    #     self.ParseInput(self.local_tz.localize(datetime.datetime.now()).astimezone(self._tz))












