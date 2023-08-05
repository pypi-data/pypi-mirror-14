#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2014 Martin Raspaud

# Author(s):

#   Martin Raspaud <martin.raspaud@smhi.se>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
"""

import requests
import os
auth = ("mraspaud", "esasucks")
#params = {'q': "+".join('productType:"GRD"  AND  swathIdentifier:"EW"  AND( ingestionDate:[2014-12-07T00:00:00.000Z TO 2014-12-08T23:59:59.999Z ] )  AND ( footprint:"Intersects(POLYGON ((6.1299197292328 53.42977963583,30.299841604233 53.42977963583,30.299841604233 66.120926899993,6.1299197292328 66.120926899993,6.1299197292328 53.42977963583)))" )'.split())}
params = {
    #'q': 'footprint:"Intersects(POLYGON((-4.53 29.85,26.75 29.85,26.75 46.80,-4.53 46.80,-4.53 29.85)))"'
    #'q': 'footprint:"Intersects(POLYGON ((6.29 61.61,24.54 67.40,31.48 60.43,26.78 54.46,6.12 50.86,6.29 61.61)))"'
    #'q': 'beginPosition:[NOW-3MONTHS TO NOW] AND endPosition:[NOW-3MONTHS TO NOW]'
    #'q': 'swathIdentifier:"EW" AND footprint:"Intersects(POLYGON ((6.1299197292328 53.42977963583,30.299841604233 53.42977963583,30.299841604233 66.120926899993,6.1299197292328 66.120926899993,6.1299197292328 53.42977963583)))"'
    'q': 'swathIdentifier:"EW"'
}


# r = requests.get(
#    'https://scihub.esa.int/dhus/search', params=params, auth=auth)
# print r.text


import subprocess as sp
proc = sp.Popen(["curl", "-gu", "mraspaud:esasucks",
                 #"https://scihub.esa.int/dhus/search?q=ingestiondate:[NOW-200DAYS+TO+NOW]+AND+producttype:GRD+AND+swathIdentifier:EW+AND+footprint:\"Intersects(POLYGON+((53.4300000000000%206.1300000000000,66.1200000000000%206.1300000000000,66.1200000000000%2030.3000000000000,53.4300000000000%2030.3000000000000,53.4300000000000%206.1300000000000%20))))\"&rows=10000&start=0"
                 #"https://scihub.esa.int/dhus/search?q=ingestiondate:[1970-12-05T16:33:18.525585299Z%20TO%20NOW]%20AND%20producttype:GRD+AND+(%20footprint:%22Intersects(POLYGON((53.43%206.13,66.12%206.13,66.12%2030.30,53.43%2030.30,53.43%206.13%20)))%22)&rows=10000&start=0"
                 "https://scihub.esa.int/dhus/search?q=ingestiondate:[NOW-7DAYS+TO+NOW]+AND+producttype:GRD+AND+swathIdentifier:\"EW\"+AND+footprint:\"Intersects(POLYGON+((6.13+53.43,6.13+66.15,30.30+66.12,30.30+53.43,6.13+53.43)))\"&rows=10000&start=0"
                 ], stdout=sp.PIPE, stderr=sp.PIPE)

text, errors = proc.communicate()

print text

import feedparser
from datetime import datetime, timedelta
d = feedparser.parse(text)

print d.feed.title
print len(d.entries)


def download_file(url, local_filename):
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True, auth=auth)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()
    return local_filename

for entry in d.entries:
    date = datetime.strptime(entry['summary'].split(',')[0].split()[1],
                             "%Y-%m-%dT%H:%M:%S.%fZ")
    if date > datetime.utcnow() - timedelta(days=2):
        fname = os.path.join(
            "/data/temp/Martin.Raspaud/sentinel1", entry.title)
        if not os.path.exists(fname):
            url = "https://scihub.esa.int/dhus/odata/v1/Products('" + \
                entry.id + "')/$value"
            print "downloading", fname, "..."
            download_file(url, fname)
        else:
            print "skipping", fname
