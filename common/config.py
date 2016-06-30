"""Configuration File for PriceAnalyzer"""

# DATA_SOURCE_ROOT is the base folder for data sources
DATA_SOURCE_ROOT = 'common.data_sources'

# MARKET_DATA_SOURCE_MAP instructs the program where to look for data sources within DATA_SOURCE_ROOT.
# It has the following structure:
#     {
#       <market_name>: {
#           'path': DATA_SOURCE_ROOT.<foldername>,
#           'sources': [
#             {
#               'name': <arbitrary name of source>,
#               'path': DATA_SOURCE_ROOT.(path from above).<subfoldername>,
#               'active': <True/False> (On/Off switch to use this definition as a source)
#             },
#             {
#               (Supplemental source(s) for the same market)
#             }
#           ]
#       },
#
#       (Other Markets)
#     }

MARKET_DATA_SOURCE_MAP = {
  'forex': {
    'path': 'FOREX',
    'sources': [
      {
      'name': 'FXCM',
      'path': 'fxcm',
      'active': True
      },
    ]
  },

  'index': {
    'path': 'FOREX',
    'sources': [
      {
      'name': 'FXCM',
      'path': 'fxcm',
      'active': True
      },
    ]
  },
}

# During initialization, WATCHLIST is used to create the necessary market/ticker objects used in DataAnalysis.  It
# is also used in the data import filtration process in distributing incoming PriceDataMessage objects.
WATCHLIST = {
  'forex': ['EURUSD', 'GBPUSD', 'USDCHF', 'EURCHF'],
  'index': ['USDOLLAR', 'US30', 'SPX500', 'NAS100', 'UK100', 'UKOIL', 'SUI20', 'EUSTX50', 'BUND']
}