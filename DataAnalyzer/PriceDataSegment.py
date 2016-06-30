"""Segment and SegmentType classes"""
import numpy as np
import pandas as pd

from enum import Enum
from common import util
from common import validations


class SegmentType(Enum):
    fiveminute = 1
    fifteenminute = 2
    thirtyminute = 3
    onehour = 4
    fourhour = 5
    halfday = 6
    oneday = 7
    oneweek = 8
    fourweek = 9
    halfyear = 10
    oneyear = 11

    def _sameyear(self, dtobj_1, dtobj_2):
      return dtobj_1.year == dtobj_2.year

    def _samemonth6(self, dtobj_1, dtobj_2):
      half1 = dtobj_1.month <= 6
      half2 = dtobj_2.month <= 6

      return self._sameyear(dtobj_1, dtobj_2) and half1 == half2

    def _samemonth(self, dtobj_1, dtobj_2):
      return dtobj_1.month == dtobj_2.month

    def _sameweek(self, dtobj_1, dtobj_2):
      same_week = dtobj_1.isocalendar()[0] == dtobj_2.isocalendar()[0]
      same_week = same_week and dtobj_1.isocalendar()[1] == dtobj_2.isocalendar()[1]
      return same_week

    def _sameday(self, dtobj_1, dtobj_2):
      return dtobj_1.isocalendar() == dtobj_2.isocalendar()

    def _samehour12(self, dtobj_1, dtobj_2):
      same_day = self._sameday(dtobj_1, dtobj_2)
      halfday1 = dtobj_1.hour < 12
      halfday2 = dtobj_2.hour < 12
      return same_day and halfday1 == halfday2

    def _samehour4(self, dtobj_1, dtobj_2):
      if self._samehour12(dtobj_1, dtobj_2):
        for i in xrange(0, 24, 4):
          rng = range(i, i + 4)
          if dtobj_1.hour in rng and dtobj_2.hour in rng:
            return True
      return False

    def _samehour(self, dtobj_1, dtobj_2):
      return self._sameday(dtobj_1, dtobj_2) and dtobj_1.hour == dtobj_2.hour

    def _sameminute30(self, dtobj_1, dtobj_2):
      samehour = self._samehour(dtobj_1, dtobj_2)
      halfhour1 = dtobj_1.minute < 30
      halfhour2 = dtobj_2.minute < 30
      return samehour and halfhour1 == halfhour2

    def _sameminute15(self, dtobj_1, dtobj_2):
      if self._sameminute30(dtobj_1, dtobj_2):
        for i in xrange(0, 60, 15):
          rng = range(i, i + 15)
          if dtobj_1.minute in rng and dtobj_2.minute in rng:
            return True
      return False

    def _sameminute5(self, dtobj_1, dtobj_2):
      if self._sameminute15(dtobj_1, dtobj_2):
        for i in xrange(0, 60, 5):
          rng = range(i, i + 5)
          if dtobj_1.minute in rng and dtobj_2.minute in rng:
            return True
      return False

    def _validateTimeStamps(self, old_val, new_val):
      if validations.isNumeric(old_val) or validations.isTimestamp(old_val):
        if validations.isNumeric(old_val):
          old_val = util.convertTimeStamp(old_val)
        new_val = util.equalizeTimestamps(old_val, new_val)
        return old_val, new_val
      return None, None

    # Rules determine if two timestamps belong in the same segment or not.
    def _rule_fiveminute(self, old_val, new_val):
      old_val, new_val = self._validateTimeStamps(old_val, new_val)
      if old_val and new_val:
        return self._sameminute5(old_val, new_val)
      return False

    def _rule_fifteenminute(self, old_val, new_val):
      old_val, new_val = self._validateTimeStamps(old_val, new_val)
      if old_val and new_val:
        return self._sameminute15(old_val, new_val)
      return False

    def _rule_thirtyminute(self, old_val, new_val):
      old_val, new_val = self._validateTimeStamps(old_val, new_val)
      if old_val and new_val:
        return self._sameminute30(old_val, new_val)
      return False

    def _rule_onehour(self, old_val, new_val):
      old_val, new_val = self._validateTimeStamps(old_val, new_val)
      if old_val and new_val:
        return self._samehour(old_val, new_val)
      return False

    def _rule_fourhour(self, old_val, new_val):
      old_val, new_val = self._validateTimeStamps(old_val, new_val)
      if old_val and new_val:
        return self._samehour4(old_val, new_val)
      return False

    def _rule_halfday(self, old_val, new_val):
      old_val, new_val = self._validateTimeStamps(old_val, new_val)
      if old_val and new_val:
        return self._samehour12(old_val, new_val)
      return False

    def _rule_oneday(self, old_val, new_val):
      old_val, new_val = self._validateTimeStamps(old_val, new_val)
      if old_val and new_val:
        return self._sameday(old_val, new_val)
      return False

    def _rule_oneweek(self, old_val, new_val):
      old_val, new_val = self._validateTimeStamps(old_val, new_val)
      if old_val and new_val:
        return self._sameweek(old_val, new_val)
      return False

    def _rule_fourweek(self, old_val, new_val):
      old_val, new_val = self._validateTimeStamps(old_val, new_val)
      if old_val and new_val:
        return self._sameweek(old_val, new_val)
      return False

    def _rule_halfyear(self, old_val, new_val):
      old_val, new_val = self._validateTimeStamps(old_val, new_val)
      if old_val and new_val:
        return self._samemonth6(old_val, new_val)
      return False

    def _rule_oneyear(self, old_val, new_val):
      old_val, new_val = self._validateTimeStamps(old_val, new_val)
      if old_val and new_val:
        return self._sameyear(old_val, new_val)
      return False


    def _getValidationFunc(self):
      """Maps ListType to corresponding validation function.

      ex: RollingListType.NumericalList gets mapped to _validNumericalList.
      """
      _VALIDATION_FUNC_PREFIX = '_rule_'
      this_name = '{0}{1}'.format(_VALIDATION_FUNC_PREFIX, self.name)
      if hasattr(self, this_name):
        return getattr(self, this_name)
      else:
        return this_name

    def Validate(self, old_val, new_val):
      test_func = self._getValidationFunc()

      if not isinstance(test_func, str):
        return test_func(old_val, new_val)
      else:
        return 'Error: No such validation function: {0}'.format(test_func)


class Segment(object):
  _SEGMENT_CODE_MAP={
    'fiveminute': ['5m','5M'],
    'fifteenminute': ['15m', '15M'],
    'thirtyminute' : ['30m', '30M'],
    'onehour' : ['1h', '1H'],
    'fourhour' : ['4h', '4H'],
    'halfday' : ['12h', '12H'],
    'oneday' : ['1d', '1D'],
    'oneweek' : ['1w', '1W', '7d', '7D'],
    'fourweek' : ['4w', '4W', '1m', '1M'],
    'halfyear' : ['6m', '6M', '26w', '26W'],
    'oneyear' : ['1y', '1Y', '12m', '12M', '52w', '52W']
  }

  def __init__(self, Open=None, sType=None, Ts=None):
    self.segment_values = base_utils.RollingList_NumericalPlus()
    self.segment_values.SetLimit(60)
    self.open = Open
    self.init_timestamp = Ts
    self._setSeg(sType)
    if Open:
      self.segment_values.add(Open)

  def __repr__(self):
    result = '<Segment (type: {4}; open: {0}; close: {1}; low: {2}; high: {3};)>'
    return result.format(self.open, self.close, self.low, self.high, self.segmenttype.name)


  def _setSeg(self, val):
    a = None
    if isinstance(val, int):
      try:
        a = SegmentType(val)
      except:
        pass

    if not a and val in self._SEGMENT_CODE_MAP.keys():
      a = SegmentType[val]
    elif not a  and val in [i for j in self._SEGMENT_CODE_MAP.values() for i in j]:
      for k, v in self._SEGMENT_CODE_MAP.iteritems():
        if val in v:
          a = SegmentType[k]

    if a:
      self._segmenttype = a
    else:
      pass
      # Error Handling here for invalid SegmentType

  def _getSeg(self):
    return self._segmenttype

  @property
  def close(self):
    return self.segment_values.get

  @property
  def high(self):
    return self.segment_values.high

  @property
  def low(self):
    return self.segment_values.low

  segmenttype = property(_getSeg,_setSeg)

