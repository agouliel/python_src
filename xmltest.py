# Python in a nutshell 3rd edition (doesn't seem to work)
# https://stackoverflow.com/questions/1912434/how-to-parse-xml-and-get-instances-of-a-particular-node-attribute
# https://stackoverflow.com/questions/44381249/treat-a-string-as-a-file-in-python

import xml.etree.ElementTree as ET
#from io import StringIO

myxml = """
<breakfast_menu>
<food>
  <name lang="eng">Belgian Waffles</name>
  <calories>650</calories>
</food>
<food>
  <name lang="fr">Strawberry Belgian Waffles</name>
  <calories>900</calories>
</food>
</breakfast_menu>
"""

#f = StringIO(myxml)
#tree = ET.parse(f)
#root = tree.getroot()

# https://docs.python.org/3/library/xml.etree.elementtree.html
root = ET.fromstring(myxml)

foodnames = root.findall('food/name')
for foodname in foodnames:
  print(foodname.get('lang'), foodname.text)
