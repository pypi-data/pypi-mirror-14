PyRDW
=====

Supports Python 2.6, 2.7, 3.3, 3.4 and 3.5

PyRDW gives a basic way of fetching licensenumber-data from the RDW, the dutch department of road transport.
Keys in data returned (by the RDW) are in dutch, unfortunately.

See the RDW for data-documentation:

https://www.rdw.nl/opendata/Paginas/handleidingen.aspx?path=Portal/OpenData

Regular expressions copied from:

http://blog.kenteken.tv/2011/05/06/code-snippets-formatteren-rdw-kenteken/



###Usage


```
>>> from pyrdw.license_number import LicenseNumber
>>>
>>> license_number = LicenseNumber('8tgj72')
>>> license_number.formatted
'8-TGJ-72'
>>> license_number.data['Merk']
u'FERRARI'
>>> license_number.data['Handelsbenaming']
u'458'
>>> license_number.data['Aantalzitplaatsen']
2
>>> license_number.data['BPM']
50193

```


###Version-history

1.1 - 2016-04-21 - Added Python 3 support;
1.0 - 2014-12-23 - Release;
1.0b - 2014-12-23 - Basic functionality with license_number validation and an RDW call.
