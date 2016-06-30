import urllib2
from common import constants


def GetDataFromURL(url, head=constants.URL_HEADER):
  response = urllib2.Request(url, headers=head)
  con = urllib2.urlopen(response)
  return con.read()









