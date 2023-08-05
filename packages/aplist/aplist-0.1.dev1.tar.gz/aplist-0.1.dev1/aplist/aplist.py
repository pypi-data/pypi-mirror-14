"""Airport List Query package.

Aiport List module: Main class.
"""

from aplist.data_provider import DataProvider
from aplist.processor import Processor
from aplist.decoder import Decoder


class AirportList(object):
    """Airport List class."""

    def __init__(self):
        """Constructor."""
        self.prov = DataProvider()
        self.proc = Processor()
        self.dec = Decoder()
        self.dec.assign_processor(processor=self.proc)
        self.proc.load(dataset=self.prov.data)

    def query(self, query):
        """Execute a query."""
        return self.dec.query(query=query)


if __name__ == '__main__':
    al = AirportList()
    # print('## {}'.format(al.query({'search': {'icao': 'LFPG'}})))
    # print('## {}'.format(al.query({'search': {'icao': 'LFPO'}})))
    # print('## {}'.format(al.query({'search': {'icao': 'RJBB'}})))
    print('## {}'.format(al.query({'search': {'country': 'Japan'}})))
