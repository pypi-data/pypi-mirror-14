"""Airport List Query package.

Data provider module: provides raw data from web or cached file.
"""

from ast import literal_eval
import csv
import json
import os
import requests


class DataProvider(object):
    """Provide sanitized airport/stations list data."""

    # Default local cached data filename
    _filename = './cache/airports.dat'
    # Default CSV file URI
    _uri = ('https://raw.githubusercontent.com/jpatokal/openflights/'
            'master/data/airports.dat')
    # Character substitution map for raw data
    char_subs_map = {
        '\\N': 'None',
        ', ': '',  # coma with a space for not selecting the CSV separator
        '\'': ''
    }
    fields = ['uid', 'name', 'city', 'country', 'iata', 'icao', 'latitude',
              'longitude', 'altitude', 'tzoffset', 'dst', 'tzname']

    def __init__(self, filename=None, uri=None, use_cache=True):
        """Constructor."""
        self.filename = filename if filename else self._filename
        self.uri = uri if uri else self._uri
        if os.path.isfile(path=self.filename) and use_cache:
            self.load_data_from_file()
            self.cache_hit = True
        else:
            dirname = os.path.dirname(self.filename)
            if not os.path.isdir(dirname):
                os.mkdir(dirname)
            self.load_data_from_uri()
            self.save_data_to_file()
            self.cache_hit = False

    def load_data_from_file(self):
        """Load data from cached file."""
        with open(file=self.filename) as f:
            self.data = json.load(f)

    def save_data_to_file(self):
        """Load data into cache file."""
        with open(file=self.filename, mode='w') as f:
            json.dump(self.data, f)

    def load_data_from_uri(self):
        """Download contents from the given URI."""
        raw_data = self._extract(uri=self.uri)
        self.data = self._transform(raw_data=raw_data)

    def _extract(self, uri):
        """Extract data from the given URI."""
        rq = requests.get(uri)
        rq.raise_for_status()
        rq.connection.close()  # avoid ResourceWarning: unclosed socket
        return rq.text

    def _transform(self, raw_data):
        """Convert raw data into list."""
        # not very clever but we don't iterate more than several times
        for old, new in self.char_subs_map.items():
            raw_data = raw_data.replace(old, new)
        # break-down into rows
        rows = csv.reader(raw_data.split('\n'), quoting=csv.QUOTE_NONE)
        rows = list(filter(None, rows))
        rows = [list(map(literal_eval, row)) for row in rows]
        # add matching fields to values
        rows = [dict(zip(self.fields, r)) for r in rows]
        # remove rows not airport related (no ICAO or IATA data)
        rows = [r for r in rows if r['icao'] and r['iata']]
        return rows
