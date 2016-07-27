

import datetime as dt
import common.PriceDataMessage as PDM
import common.time_utils as tu


SOURCE_MAP = {
  'source_name': 'fxcm',
  'url': 'http://rates.fxcm.com/RatesXML',
  'source_timezone': 'US/Eastern'
}

def ConvertXMLtoPDM(market, etree_child_obj):
  pdm = PDM.PriceDataMessage()
  if PDM.PDMu.MarketSearch(market):
    ticker = etree_child_obj.attrib['Symbol']
    bid = float(etree_child_obj.find('.//Bid').text)
    ask = float(etree_child_obj.find('.//Ask').text)
    src_time = etree_child_obj.find('.//Last').text.split(':')
    src_time = dt.time(int(src_time[0]), int(src_time[1]), int(src_time[2]))
    src_date = dt.date.today()

    # Convert SRC date/time to proper format
    datetime = tu.Time((src_date, src_time), SOURCE_MAP['source_timezone'])
    #
    # print 'Datetime: {0}'.format(datetime)
    # print 'Datetime TS: {0}'.format(datetime.timestamp)
    # print 'Datetime Date: {0}'.format(datetime.timestamp.date())
    # print 'Datetime Time: {0}'.format(datetime.timestamp.time())
    # print 'Datetime TZ: {0}'.format(datetime.timestamp.tzinfo)
    # print 'Datetime Epoch: {0}\n\n'.format(datetime.asEpoch)

    pdm.market = market
    pdm.ticker = ticker
    pdm.bid = bid
    pdm.ask = ask
    pdm.date = datetime.timestamp.date()
    pdm.time = datetime.timestamp.time()
    pdm.timezone = datetime.timestamp.tzinfo
    pdm.utc_epoch = datetime.asEpoch

    return pdm

