import common.BaseModel as BM
from common import util
from common import xml_utils as xm
from common import config


class ImportManager(BM.BaseObject):
  _data_source = config.DATA_SOURCE_ROOT
  _ERRORLOG_KEY = '__ImportManager_Error__'
  _ACTIVITYLOG_KEY = _COMMLOG_KEY = '__ImportManager__'

  class ImportQueue(object):
    pass

  def __init__(self):
    super(ImportManager, self).__init__()
    self.ActivityLog.Add(self._ACTIVITYLOG_KEY, 'INITIALIZING IMPORT MANAGER - {0}'.format(util.Timestamp()))
    self.markets = []
    self.raw_data = []
    self.transformed_data = []
    for market, source_info in config.MARKET_DATA_SOURCE_MAP.iteritems():
      self.markets.append(market)
      setattr(self, market, self._newSubClass(market))

      # Create Market object in Import Manager
      market_obj = getattr(self, market)

      # Add path/sources info to Market Obj
      setattr(market_obj, 'path', '{0}.{1}'.format(self._data_source, source_info['path']))
      setattr(market_obj, 'sources', [])

      # Create Source object for  Market Obj
      setattr(market_obj, 'Sources', self._newSubClass('Sources'))

      # Build Import Queues
      setattr(self.ImportQueue, market, [])

      for source in source_info['sources']:
        market_obj.sources.append(source['name'])
        setattr(market_obj.Sources, source['name'], self._newSubClass(source['name']))

        source_obj = getattr(market_obj.Sources, source['name'])
        setattr(source_obj, 'path', '{0}.{1}'.format(market_obj.path, source['path']))
        setattr(source_obj, 'active', source['active'])

        # Only put 'active' sources in ImportQueue.
        if source['active']:
          getattr(self.ImportQueue, market).append((source['name'], self.GetImportObj(market, source['path'])))

    self.ActivityLog.Add(self._ACTIVITYLOG_KEY, 'FINISHED INITIALIZING IMPORT MANAGER - {0}'.format(util.Timestamp()))


  @property
  def queues(self):
    return [x for x in dir(self.ImportQueue) if not x.startswith('_')]

  def _newSubClass(self, name):
    return type(name, (object,), {})

  def GetSources(self, market_name):
    if isinstance(market_name, str):
      if hasattr(self, market_name.lower()):
        return getattr(self, market_name.lower()).sources, getattr(self, market_name.lower()).Sources

  def GetSourcePath(self, market_name, source_name):
    sources, source_obj = self.GetSources(market_name)

    if source_name.upper() in sources:
      src_obj = getattr(source_obj, source_name.upper())
      return src_obj.path

  def IsSourceActive(self, market_name, source_name):
    sources, source_obj = self.GetSources(market_name)

    if source_name.upper() in sources:
      src_obj = getattr(source_obj, source_name.upper())
      return src_obj.active


  def GetImportObj(self, market_name, source_name):
    if market_name in self.markets:
      mkt_obj = getattr(self, market_name)
      if source_name.upper() in mkt_obj.sources:
        path = self.GetSourcePath(market_name, source_name)
        return __import__(path, fromlist=source_name)

  def _validateSourceObject(self, source_obj):
    """Validates imported Source Objects."""

    # A source is a module that contains one dict (SOURCE_MAP) and one function (ConvertXMLtoPDM) specific to
    # that particular source.

    return hasattr(source_obj, 'SOURCE_MAP') and hasattr(source_obj, 'ConvertXMLtoPDM')


  def StartImport(self):
    self.ActivityLog.Add(self._ACTIVITYLOG_KEY, 'Starting Data Import: {0}'.format(util.Timestamp()))
    for market in self.queues:
      self.ActivityLog.Add(self._ACTIVITYLOG_KEY, 'Preparing to import source data for market: {0}'.format(market))
      for source_name, source_obj in getattr(self.ImportQueue, market):
        if self._validateSourceObject(source_obj):
          src_map, conversion_func = source_obj.SOURCE_MAP, source_obj.ConvertXMLtoPDM
          url = src_map['url']

          self.ActivityLog.Add(self._ACTIVITYLOG_KEY, 'SRC Name: {0}; SRC URL: {1}'.format(source_name, url))
          raw_data = xm.GetXMLfromSource(url)
          self.raw_data.append(raw_data)
          self.ActivityLog.Add(self._ACTIVITYLOG_KEY, 'Raw Data Obtained from {0} ...Converting Data'.format(url))

          data_set = xm.IterateXML(market, raw_data, conversion_func)
          self.transformed_data.extend(data_set)
          self.ActivityLog.Add(self._ACTIVITYLOG_KEY, 'PDM Data Ready for {0}: Message count: {1}...'.format(market, len(data_set)))
        else:
          self.ErrorLog.Add(self._ERRORLOG_KEY, 'Improperly Formatted Source File: {0}'.format(source_name))
          self.ActivityLog.Add(self._ACTIVITYLOG_KEY, 'Ignoring Source File: {0}'.format(source_name))

      self.ActivityLog.Add(self._ACTIVITYLOG_KEY, 'Data Import Finished: {0}'.format(util.Timestamp()))

