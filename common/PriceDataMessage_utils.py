import collections
from enum import Enum
import datetime as dt
import PriceDataMessage_utils_maps as PDMum

def MarketSearch(val):
  if isinstance(val, str):
    for item in Market:
      if val.lower() == item.name.lower():
        return item
  return None

class Ticker(Enum):
  """Base Enum class for Ticker Enums."""
  def valid(self, market):
    return type(self) == market.value


def _buildForexEnum():
  counter = 0
  enum_list = []
  for base in PDMum.FOREX_BASES:
    for match in [x for x in PDMum.FOREX_BASES if x != base]:
      pair = '{0}{1}'.format(base[0], match[0])
      enum_list.append((pair, counter))
      counter += 1
  return dict(enum_list)

def _buildGenericEnum(ticker_map):
  return dict([(ticker[0], i) for i, ticker in enumerate(ticker_map)])


TickerForex = type('TickerForex', (Ticker,), _buildForexEnum())
TickerNYSE = type('TickerNYSE', (Ticker,), _buildGenericEnum(PDMum.NYSE_TICKERS))
TickerIndex = type('TickerIndex', (Ticker,), _buildGenericEnum(PDMum.WORLD_ECON_INDEXES))

class Market(Enum):
  Forex = TickerForex
  NYSE = TickerNYSE
  Index = TickerIndex

  @property
  def tickers(self):
    return [item.name for item in self.value]



def _buildProperties(cls):
  """Dynamically builds properties for PriceDataMessage based on PROPERTY_TYPES."""
  def _property(key):
    return property(lambda self: self._getVal(key), lambda self, x: self._setVal(key, x), lambda self: self._delVal(key))

  for k in PROPERTY_TYPES.keys():
    setattr(cls, k, _property(k))


def _buildProperties_explicit(cls):
  """Older version of _buildProperties.  Works, but not being used"""
  setattr(cls, 'date', property(lambda self: self._getVal('date'),
                               lambda self, x: self._setVal('date', x),
                               lambda self: self._delVal('date')))

  setattr(cls, 'time', property(lambda self: self._getVal('time'),
                               lambda self, x: self._setVal('time', x),
                               lambda self: self._delVal('time')))

  setattr(cls, 'market', property(lambda self: self._getVal('market'),
                               lambda self, x: self._setVal('market', x),
                               lambda self: self._delVal('market')))

  setattr(cls, 'ticker', property(lambda self: self._getVal('ticker'),
                               lambda self, x: self._setVal('ticker', x),
                               lambda self: self._delVal('ticker')))

  setattr(cls, 'bid', property(lambda self: self._getVal('bid'),
                               lambda self, x: self._setVal('bid', x),
                               lambda self: self._delVal('bid')))

  setattr(cls, 'ask', property(lambda self: self._getVal('ask'),
                               lambda self, x: self._setVal('ask', x),
                               lambda self: self._delVal('ask')))

PROPERTY_TYPES = collections.OrderedDict([
  ('date', dt.date),
  ('time', dt.time),
  ('market', Market),
  ('ticker', Ticker),
  ('bid', float),
  ('ask', float)]
)
