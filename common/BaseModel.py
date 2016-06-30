"""Common Model object."""
import inspect
import string
import Log_collector


lcase = list(string.lowercase)
ucase = list(string.uppercase)

# (A , B, C)
#  A: Startswith,  B: First/All letters in list (1: First), C: Ends with
CLASS_DEF_NAME_STARTS = {
  'Built-In': ('__', (lcase, 1), '__'),
  'BaseModel Property': ('_', (lcase, 1), '_base'),
  'BaseModel Function': ('_', (ucase, 1), '_base'),
  'Private User Property': ('_', (lcase, 1), None),
  'Private User Function': ('_', (ucase, 1), None),
  'Public User Property': (None, (lcase, 1), None),
  'Public User Function': (None, (ucase, 1), None),
  'Private Constant': ('_', (ucase, 0), None),
  'Public Constant': (None, (ucase, 0), None)
}


def InspectUtil(cls_name, errors=None):
  if isinstance(cls_name, str):
    for rule in CLASS_DEF_NAME_STARTS.iteritems():
      rule_name, rule_def = rule
      r_start, r_case, r_end = rule_def
      r_case_list, r_case_type = r_case

      if r_start:
        rs_pass = cls_name.startswith(r_start)
      else:
        rs_pass = True

      if r_end:
        re_pass = cls_name.endswith(r_end)
      else:
        re_pass = not cls_name.endswith('_base')

      startpos = len(r_start) if r_start else 0
      endpos = len(cls_name) - len(r_end) if r_end else len(cls_name)
      test_segment = cls_name[startpos: startpos+1] if r_case_type else cls_name[startpos: endpos]

      case_pass = True
      for char in test_segment:
        if not char in r_case_list:
          case_pass = False

      if rs_pass and case_pass and re_pass:
        return rule_name
    if errors is not None:
      errors.Add('BASE', 'Not Found')
  else:
    if errors is not None:
      errors.Add('BASE', 'Inspect Error')

  return False




class BaseObject(object):

  ErrorLog = Log_collector.Log('__genericError__')
  ActivityLog = Log_collector.Log('__genericActivity__')
  CommLog = Log_collector.Log('__genericComm__')

  def __init__(self):
    pass

  def _Inspectclass_base(self, nomagic=True, exception=['BaseModel Property', 'BaseModel Function']):
    for name, stuff in inspect.getmembers(self):
      name_type = InspectUtil(name, self.ErrorLog)
      if not name_type in exception:
        if (nomagic and name_type != 'Built-In') or not nomagic:
          print name, stuff

  def _to_dict(self):
    members = [attr for attr in dir(self) if not callable(attr) and not attr.startswith('_') and attr[0] not in list(string.uppercase)]
    new_dict = {}
    for mem in members:
      new_dict[mem] = getattr(self, mem)
    return new_dict












