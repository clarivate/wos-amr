"""
Expects an incoming CSV file with ISSNs and will generate output from AMR.

E.g.

ISSN
0265-0568
0028-0836
0028-4793

You can optionally include an ID column for the journal
ID,ISSN
1,0265-0568
2,0028-0836
3,0028-4793

Run as:

$ python issns_to_jcr.py issns_example.csv outputfile.csv

"""

import csv
import sys
import xml.etree.ElementTree as ET

import client


request_template = u"""<?xml version="1.0" encoding="UTF-8" ?>
<request xmlns="http://www.isinet.com/xrpc41" src="app.id=InternalVIVODemo">
  <fn name="LinksAMR.retrieve">
    <list>
      <!-- authentication -->
      <map>
        <val name="username">{user}</val>
        <val name="password">{password}</val>
      </map>
      <!-- what to to return -->
       <map>
        <list name="JCR">
          <val>impactGraphURL</val>
          <val>issn</val>
        </list>
      </map>
       <!-- LOOKUP DATA -->
       {items}
    </list>
  </fn>
</request>
"""


def prep_request(items):
    """
    <map name="cite_1">
        <val name="{id_type}">{value}</val>
    </map>
    """
    map_items = ET.Element("map")
    for item_id, issn in [i for i in items if i is not None]:
        if (item_id is None) or (issn is None):
            continue
        this_item = ET.Element("map", name=str(item_id))
        de = ET.Element("val", name="issn")
        de.text = issn
        this_item.append(de)
        map_items.append(this_item)

    request_items = ET.tostring(map_items).decode("utf-8")
    xml = request_template.format(user=client.USER, password=client.PASSWORD, items=request_items)
    return xml


def main():
    found = []
    journals = []
    with open(sys.argv[1]) as infile:
        for num, row in enumerate(csv.DictReader(infile)):
            print("Processing {}".format(row['ISSN']))
            jid = row.get('ID', num)
            journals.append((jid, row['ISSN']))

    lookup_groups = client.grouper(journals, client.BATCH_SIZE)
    for idx, batch in enumerate(lookup_groups):
        xml = prep_request(batch)
        print("Processing batch {}".format(idx))
        # Post the batch
        rsp = client.get(xml)
        found.append(rsp)

    with open(sys.argv[2], 'w') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(('number', 'ISSN', 'JCR'))
        for grp in found:
            for item in grp:
                writer.writerow([item, grp[item].get('issn', 'na'), grp[item].get('impactGraphURL', 'na')])


if __name__ == "__main__":
    main()
