from lxml import etree as et
from DataAnalyzer import data_import


def GetXMLfromSource(url):
  """Retrieves Raw XML from url and returns etree object."""
  # Set up XML parser
  parser = et.XMLParser(remove_blank_text=True)

  # Retrieve raw XML.
  raw_xml = data_import.GetDataFromURL(url)

  # Create XML object.
  parsed_xml = et.XML(raw_xml)

  # Clean it up a bit.
  for element in parsed_xml.iter('*'):
    if element.text is not None and not element.text.strip():
      element.text = None

  return parsed_xml


def IterateXML(market, xml_data, conversion_func):
  data_set=[]
  for child in xml_data.iterchildren():
    pdm = conversion_func(market, child)
    if pdm.ticker:
      data_set.append(pdm)

  return data_set
