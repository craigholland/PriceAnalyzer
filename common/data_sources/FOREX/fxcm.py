import datetime as dt
import common.PriceDataMessage as PDM
import common.time_utils as tu

url = 'http://rates.fxcm.com/RatesXML'

def ConvertXMLtoPDM(market, etree_child_obj):
  pdm = PDM.PriceDataMessage()
  if PDM.PDMu.MarketSearch(market):
    ticker = etree_child_obj.attrib['Symbol']
    bid = float(etree_child_obj.find('.//Bid').text)
    ask = float(etree_child_obj.find('.//Ask').text)
    time = etree_child_obj.find('.//Last').text.split(':')
    time = dt.time(int(time[0]), int(time[1]), int(time[2]))
    date = dt.date.today()


    pdm.market = market
    pdm.ticker = ticker
    pdm.bid = bid
    pdm.ask = ask
    pdm.date = date
    pdm.time = time

    timestamp = tu.Time((date, time), 'US/Pacific')
    pdm.epoch = timestamp.asEpoch

    return pdm

