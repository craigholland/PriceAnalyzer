"""PriceData object holds data for targeted markets/tickers."""
from common import BaseModel as BM
from common import config
from common import PriceDataMessage as PDM

import ImportManager as IM

PDMu = PDM.PDMu

def newObjectTemplate(name):
  return type(name,(BM.BaseObject,), {})

class PriceData(BM.BaseObject):

  def __init__(self):
    super(PriceData, self).__init__()
    self.markets = []
    self.Market = newObjectTemplate('Market')

    # Build as per config file
    for market, ticker_list in config.WATCHLIST.iteritems():
      marketEnum = PDMu.MarketSearch(market)
      if marketEnum:
        self.markets.append(market)
        setattr(self.Market, market, newObjectTemplate(market))
        mkt_obj = getattr(self.Market, market)
        setattr(mkt_obj, 'tickers', [])
        setattr(mkt_obj, 'Ticker', newObjectTemplate('Ticker'))
        setattr(mkt_obj, 'type', marketEnum)

        for ticker in ticker_list:
          if ticker in marketEnum.tickers:
            tickerEnum = marketEnum.value[ticker]
            mkt_obj.tickers.append(ticker)
            ticker_obj = getattr(mkt_obj, 'Ticker')
            setattr(ticker_obj, ticker, newObjectTemplate(ticker))
            spc_ticker_obj = getattr(ticker_obj, ticker)
            setattr(spc_ticker_obj, 'type', tickerEnum)
            setattr(spc_ticker_obj, 'data', [])
          else:
            pass
            # Error - Ticker in Config file not found in given Market
      else:
        pass
        # Error - Market in Config file not found in MarketSearch



  def GetMarketTickerObj(self, market_name, ticker_name=None):
    returnObj = None
    if isinstance(market_name, str):
      mkt = market_name.lower()
      if mkt in self.markets:
        returnObj = getattr(self.Market, mkt)

    if isinstance(ticker_name, str):
      tck = ticker_name.upper()
      if tck in returnObj.tickers:
        returnObj = getattr(returnObj.Ticker, tck)

    return returnObj

  def Filter(self, pdm):
    """Receives PriceDataMessage object, sorts it into appropriate PriceData bin.

    If PDM doesn't fit in PriceData model, ignore it.
    """
    if PDM.isPDM(pdm):
      for mkt in self.markets:
        mkt_obj = getattr(self.Market, mkt)
        if mkt_obj.type == pdm.market:
          for ticker in mkt_obj.tickers:
            tck_obj = getattr(mkt_obj.Ticker, ticker)
            if tck_obj.type == pdm.ticker:
              return self.GetMarketTickerObj(mkt, ticker)
    return None

  def Add(self, pdm):
    bin = self.Filter(pdm)
    if bin:
     if pdm not in bin.data:
       bin.data.append(pdm)

  def Data(self, market_name, ticker_name):
    """Retrieve current data set for Market-ticker combo."""
    ticker_obj = self.GetMarketTickerObj(market_name, ticker_name)
    if ticker_obj:
      return ticker_obj.data
    return None

def test():
  p = PriceData()
  i = IM.ImportManager()
  i.StartImport()
  return p, i

def DisplayPriceData(pd_obj):
  indent = ' ' * 3
  if isinstance(pd_obj, PriceData):
    for mkt in pd_obj.markets:
      mkt_obj = getattr(pd_obj.Market, mkt)
      for tck in mkt_obj.tickers:
        print 'Data for MARKET: {0}; TICKER- {1}'.format(mkt, tck)
        data_set = pd_obj.Data(mkt, tck)
        for pdm in data_set:
          print indent, pdm
        print indent

