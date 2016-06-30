import BaseModel as BM
import PriceDataMessage_utils as PDMu
import validations

class PriceDataMessage(BM.BaseObject):
  _ERRORLOG_KEY = '__PriceDataMessage_Error__'
  _ACTIVITYLOG_KEY = _COMMLOG_KEY = '__PriceDataMessage__'

  def __init__(self, **kwargs):
    super(PriceDataMessage, self).__init__()

    # Create private attributes as per PDMu.PROPERTY_TYPES map.
    for key in PDMu.PROPERTY_TYPES.keys():
      setattr(self, '_{0}'.format(key), None)

    # The Market attribute must be defined prior to Ticker, so look for that.
    if 'market' in kwargs.keys():
      self.market = kwargs['market']

    # Assign all remaining attributes.
    for key, val in kwargs.iteritems():
      if hasattr(self, key):
        setattr(self, key, val)
      else:
        self.ErrorLog.Add(self._ERRORLOG_KEY, 'Unexpected attribute during PDM Init: {0}'.format(key))

  def __repr__(self):
    result = '<PriceDataMessage ( '
    for key in PDMu.PROPERTY_TYPES.keys():
      result += '{0}: {1}; '.format(key, getattr(self, key))
    result += ')>'
    return result

  @property
  def isValid(self):
    return reduce(lambda x, y: x and y,
                  map(lambda x: getattr(self, '_{0}'.format(x)) is not None,
                      PDMu.PROPERTY_TYPES.keys()),
                      True)

  def _validateData(self, val, proptype_key):
    if proptype_key in PDMu.PROPERTY_TYPES.keys():
      return isinstance(val, PDMu.PROPERTY_TYPES[proptype_key])
    else:
      self.ErrorLog.Add(self._ERRORLOG_KEY, 'Unexpected Attribute: {0}'.format(proptype_key))


  def _setValSpecialCase(self, prop_name, val):
    err_msg = None
    if PDMu.PROPERTY_TYPES[prop_name] == float and validations.isNumeric(val):
      setattr(self, '_{0}'.format(prop_name), float(val))
      return None

    if isinstance(val, str) and (prop_name == 'market' or prop_name == 'ticker'):
      if prop_name == 'market':
        market = PDMu.MarketSearch(val)
        if market:
          setattr(self, '_{0}'.format(prop_name), market)
        else:
          # Error - No Market found
          err_msg = 'No market found: {0}'.format(val)
      if prop_name == 'ticker':
        if self.market:
          ticker = None
          for tick in self.market.tickers:
            if val.lower() == tick.lower():
              ticker = tick.upper()
          if ticker:
            setattr(self, '_{0}'.format(prop_name), self.market.value[ticker])
          else:
            # Error - Ticker not found in Market
            err_msg = 'Ticker ({0}) not found in Market ({1}). Ignoring.'.format(val, self.market.name)
        else:
          # Error - Must add market first
          err_msg = 'Cannot set ticker ({0}) without market.'.format(val)
    else:
      err_msg = -1
    return err_msg

  def _setVal(self, prop_name, val):
    if hasattr(self, '_{0}'.format(prop_name)):
      if self._validateData(val, prop_name):
        setattr(self, '_{0}'.format(prop_name), val)
      else:
        setVal_special = self._setValSpecialCase(prop_name, val)
        if setVal_special:
          if isinstance(setVal_special, str):
            self.ErrorLog.Add(self._ERRORLOG_KEY, setVal_special)
          else:
            # Error - Wrong type
            self.ErrorLog.Add(self._ERRORLOG_KEY, 'Wrong type for {0}. Expected {1}, got {2} ({3}).'.format(prop_name, PDMu.PROPERTY_TYPES[prop_name], type(val), val))
    else:
      # Error - Invalid Object prop
      self.ErrorLog.Add(self._ERRORLOG_KEY, 'No Attribute named {0}'.format(prop_name))


  def _getVal(self, prop_name):
    return getattr(self, '_{0}'.format(prop_name))

  def _delVal(self, prop_name):
    if hasattr(self, '_{0}'.format(prop_name)):
      setattr(self, '_{0}'.format(prop_name), None)
    else:
      # Error - Invalid Object prop
      self.ErrorLog.Add(self._ERRORLOG_KEY, 'No Attribute named {0}'.format(prop_name))

  def copy(self):
    newPDM = PriceDataMessage()
    for key in PDMu.PROPERTY_TYPES.keys():
      setattr(newPDM, key, getattr(self, key))
    return newPDM

  def __eq__(self, other):
    if isinstance(other, PriceDataMessage):
      for key in PDMu.PROPERTY_TYPES.keys():
        if getattr(self, key) != getattr(other, key):
          return False
      return True
    else:
      return False

  def __ne__(self, other):
    if isinstance(other, PriceDataMessage):
      for key in PDMu.PROPERTY_TYPES.keys():
        if getattr(self, key) != getattr(other, key):
          return True
      return False
    else:
      return False


PDMu._buildProperties(PriceDataMessage)

def isPDM(obj):
  if isinstance(obj, PriceDataMessage):
    return True
  return False