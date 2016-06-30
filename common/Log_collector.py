"""Data structure for collecting logging messages."""

import collections
import json
import pprint

class Log(object):
  """Data structure for collecting log messages.

  Usage:

  >>> errors = Log()

  # Add a log message
  >>> errors.Add('a key', 'a message')

  # Or add multiple messages at once
  >>> errors.Add('some key', 'some message', 'another message')

  # Use None to specify "generic" errors
  >>> errors.Add(None, 'generic message')

  # Or, explicitly
  >>> errors.Add(errors.DEFAULT_KEY, 'generic message')

  # Logs are "truthy"
  >>> if errors:
  ...   DoSomethingWith(errors)

  # Get a JSON string
  >>> errors.AsJson()
  '{"some key": "some message\\nanother message",
    "__generic__": "generic message", "a key": "a message"}'
  """

  DEFAULT_KEY = '__generic__'

  DEFAULT_FMT = '\n'.join

  def __init__(self, log_type=None):
    self._log = collections.defaultdict(list)
    self._log_type = log_type

  def __nonzero__(self):
    return bool(self._log)

  def __contains__(self, key):
    return key in self._log

  def __len__(self):
    return sum(len(messages) for messages in self._log.itervalues())

  def __iter__(self):
    return iter(self._log)

  def __repr__(self):
    return '<Logs: %s>' % pprint.pformat(dict(self._log))

  def Clear(self):
    self._log.clear()

  def Get(self, key):
    """Gets log messages by key.

    Args:
      key: str, the key whose messages to retrieve. If omitted, the messages
          associated with the default key are retrieved.

    Returns:
      A list of messages for the given key, or None if the key is not present.
    """
    if not key:
      key = self._log_type if self._log_type else self.DEFAULT_KEY
    messages = self._log.get(key)
    if messages:
      return list(messages)
    return None

  def GetAll(self):
    """Gets a copy of the internal log dictionary."""
    return self._log.copy()

  def Add(self, key, message, *messages):
    """Associates one or more messages with a given key.

    Args:
      key: str, the key to associate with a message. If omitted, the messages
          are associated with the default key.
      message: str, the message to associate with the key.
      *messages: additional messages to associate with the key.
    """
    if not key:
      key = self._log_type if self._log_type else self.DEFAULT_KEY
    messages = map(str, (message,) + messages)
    self._log[key].extend(messages)

  def AsJson(self, format_func=DEFAULT_FMT):
    """Gets a JSON string representation of the log object.

    Args:
      format_func: function, used to format the list of messages for each key
          before transforming to JSON. The function should accept a list of
          strings and return a value that is JSON-serializable. The default
          behavior is to join each list of messages with a newline character.

    Returns:
      A JSON string of key/messages pairs.
    """
    logs = {k: format_func(v) for k, v in self._log.iteritems()}
    return json.dumps(logs)

  def Merge(self, other):
    """Adds all logs from another logs object to this one.

    Args:
      other: an logs instance to merge into this one.
    """
    for key, messages in other.GetAll().iteritems():
      self.Add(key, *messages)

  def Raise(self, exception, key, message, *messages):
    """Adds log message(s) and raises the given exception."""
    self.Add(key, message, *messages)
    raise exception(self.AsJson())

  def RaiseIfAny(self, exception):
    """Raises the given exception with the logs as the message, if any."""
    if self:
      raise exception(self.AsJson())

  def LogIfAny(self, logging_func):
    """Records the logs using the given logging_func."""
    if self:
      logging_func(self.AsJson())

