"""Accept Header."""
#
# Copyright 2012 keyes.ie
#
# License: http://jkeyes.mit-license.org/
#

from .media_range import MediaRange


class AcceptHeader(object):
    """Representation of an Accept header."""

    def __init__(self, raw_header):
        """Initialize the header."""
        self.media_ranges = []

        mranges = raw_header.split(',')
        for mr in mranges:
            mr = mr.strip()
            self.media_ranges.append(MediaRange(mr))
        self.media_ranges.sort(reverse=True)

    def __iter__(self):
        """Iterate over the media ranges in the header."""
        for mr in self.media_ranges:
            yield mr
