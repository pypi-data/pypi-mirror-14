"""Airport List Query package.

Decoder module: decodes high-level queries into low-level actions.
"""


class Decoder(object):
    """Decoder class."""

    def __init__(self):
        """Construct a query instance."""
        self.processor = None

    def assign_processor(self, processor):
        """Assign the processor queried by low-level commands."""
        self.processor = processor

    def query(self, query):
        """Execute a high-level query request."""
        self._start_timer()
        if not self.processor:
            raise Exception
        # Reset processor
        self.processor.reload()
        # Filter
        if 'search' in query:
            for field, value in query['search'].items():
                self.processor.filter_eq(field=field, value=value)
        # Sort
        if 'sort' in query:
            for field, direction in query['sort'].items():
                self.processor.sort(field=field, direction=direction)
        # Paginate
        if 'page' in query:
            if set(('offset', 'limit')) == query['page'].keys():
                self.processor.paginate(
                    offset=query['page']['offset'],
                    limit=query['page']['limit'])
        # Grab results
        results = self.processor.get_selection()
        self._stop_timer()
        return results

    def _start_timer(self):
        pass

    def _stop_timer(self):
        pass
