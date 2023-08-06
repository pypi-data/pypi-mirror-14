from app_version import get_versions

__version__, VERSION = get_versions('jasco_parser')


class JASCOParser(object):
    """JASCO data text parser"""
    def parse(self, iterable, delimiter=None, translator=float):
        """Parse JASCO data text and yield columns"""
        datamode = False
        for row in iterable:
            row = row.strip()
            if datamode and not row:
                break
            if datamode:
                col = row.split(delimiter)
                yield [translator(x) for x in col]
            elif row.startswith(b'XYDATA'):
                datamode = True

    def load(self, filename, delimiter=None, translater=float):
        if filename.lower().endswith('.csv') and not delimiter:
            delimiter = ','
        with open(filename, 'rb') as fi:
            return list(self.parse(fi, delimiter, translater))


def parse(iterable, delimiter=None):
    """
    Parse JASCO style text and return XY or XYZ numerical data

    Args:
        iterable: An iterable object
        delimiter: A delimiter. Default is None

    Returns:
        A list
    """
    return JASCOParser().parse(iterable, delimiter)


def load(filename, delimiter=None):
    """
    Load JASCO style text and return XY or XYZ numerical data

    Args:
        filename: A filename
        delimiter: A delimiter. Default is None

    Returns:
        A list
    """
    return JASCOParser().load(filename, delimiter)
