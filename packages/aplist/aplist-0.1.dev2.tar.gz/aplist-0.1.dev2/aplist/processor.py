"""Airport List Query package.

Process module: execute low-level actions on a given dataset.
"""

import operator


class Processor(object):
    """Processor class."""

    def __init__(self):
        """Constructor."""
        self.base_dataset = []
        self.dataset = []

    def load(self, dataset):
        """Load dataset as a list of records."""
        self.base_dataset = dataset
        self.reload()

    def reload(self):
        """Reload base dataset as live dataset."""
        self.dataset = self.base_dataset

    def filter_eq(self, field, value):
        """Filter records where the contents of the given field matches."""
        self.dataset = [r for r in self.dataset if r[field] == value]

    def sort(self, field, direction):
        """Sort filtered records."""
        rev = direction == 'des'
        self.dataset = sorted(
            self.dataset, key=operator.itemgetter(field), reverse=rev)

    def paginate(self, offset, limit):
        """Extract a part of the records."""
        self.dataset = self.dataset[offset:offset+limit]

    def get_selection(self):
        """Return paginated records."""
        return self.dataset
