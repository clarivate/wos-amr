"""
Expects an incoming CSV file with local ID, PMID, or DOI headers and wil post to
AMR in batches of 50.

E.g.

UT
01234
02394
039039

PMID
2093030
2405903
95930303

Run as:

$ python batch_lookup.py sample_file.csv outputfile.csv

"""

import csv
import sys
import xml.etree.ElementTree as ET

import client


# Template for fetching ids and timesCited from AMR
id_request_template = u"""<?xml version="1.0" encoding="UTF-8" ?>
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
         <list name="WOS">
           <val>sourceURL</val>
           <val>ut</val>
           <val>doi</val>
           <val>pmid</val>
           <val>timesCited</val>
         </list>
       </map>
       <!-- LOOKUP DATA -->
       {items}
    </list>
  </fn>
</request>
"""


def prep_request(items, local_id="id"):
    """
    Process the incoming items into an AMR request.

    <map name="cite_1">
        <val name="{id_type}">{value}</val>
    </map>
    """
    map_items = ET.Element("map")
    for idx, pub in enumerate(items):
        if pub is None:
            continue
        local_id_value = pub.get(local_id) or pub.get(local_id.upper())
        if local_id_value is None:
            local_id_value = str(idx)
        this_item = ET.Element("map", name=local_id_value)
        for k, v in pub.items():
            if v is None:
                continue
            de = ET.Element("val", name=k.lower())
            de.text = v.strip()
            this_item.append(de)
        map_items.append(this_item)

    request_items = ET.tostring(map_items)
    xml = id_request_template.format(user=client.USER, password=client.PASSWORD, items=request_items)
    return xml


def main():
    try:
        infile = sys.argv[1]
        outfile = sys.argv[2]
    except IndexError:
        raise Exception("An input and outpfile file is required.")
    found = []
    to_check = []
    with open(infile) as inf:
        for row in csv.DictReader(inf):
            d = {}
            for k, v in row.items():
                d[k.lower()] = v.strip()
            to_check.append(d)

    lookup_groups = client.grouper(to_check, client.BATCH_SIZE)
    for idx, batch in enumerate(lookup_groups):
        xml = prep_request(batch)
        print>> sys.stderr, "Processing batch", idx
        # Post the batch
        rsp = client.get(xml)
        found.append(rsp)

    # Write the results to a csv file.
    with open(outfile, 'wb') as of:
        writer = csv.writer(of)
        writer.writerow(('id', 'ut', 'doi', 'pmid', 'times cited', 'source'))
        for grp in found:
            for k, item in grp.items():
                ut = item.get('ut')
                if ut is not None:
                    ut = "WOS:" + ut
                writer.writerow([k, ut, item.get('doi', ""), item.get('pmid', ""), item.get('timesCited', '0'),
                                 item.get('sourceURL', 'N/A')])

if __name__ == "__main__":
    main()