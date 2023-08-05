"""Media Range."""
#
# Copyright 2012 keyes.ie
#
# License: http://jkeyes.mit-license.org/
#


class MediaRange(object):
    """A MediaRange class."""

    def __init__(self, media_range):
        """Initialize the object by parsing media ragnge."""
        if ';' in media_range:
            content_type, params = media_range.split(';', 1)
        else:
            content_type, params = media_range, None

        content_type = content_type.strip()
        if '/' in content_type:
            self.mtype, self.subtype = content_type.split('/')
        elif content_type == '*':
            self.mtype = self.subtype = '*'
        else:
            self.mtype = content_type
            self.subtype = '*'

        if self.mtype == "*" and self.subtype == "*":
            self.quality = int(0)
        else:
            self.quality = int(1)
        self.extensions = {}

        parts = ['%s' % content_type]
        if params:
            params = params.split(';')
            for par in params:
                name, value = par.split('=')
                name = name.strip()
                value = value.strip()
                parts.append("%s=%s" % (name, value))
                if name == 'q':
                    self.quality = float(value)
                else:
                    self.extensions[name] = value
        self._str = ";".join(parts)

    @property
    def content_type(self):
        """Return the content_type of the range."""
        return '%s/%s' % (self.mtype, self.subtype)

    @property
    def any_media(self):
        """Return whether this range accepts any media."""
        return "*/*" == self.content_type

    @property
    def any_subtype(self):
        """Return whether this range accepts any subtype."""
        return self.subtype == "*"

    def __lt__(self, other):
        """Return whether this range is less than the `other` range."""
        if self == other:
            return False
        if self.quality == other.quality:
            if self.mtype == "*":
                if other.mtype != "*":
                    return True
                return False
            if self.subtype == "*":
                if other.subtype != "*":
                    return True
                return False
            if len(self.extensions) == 0 and len(other.extensions) > 0:
                return True
            elif len(self.extensions) > 0 and len(other.extensions) == 0:
                return False
        return self.quality < other.quality

    def __gt__(self, other):
        """Return whether this range is greater than the `other` range."""
        if not self == other:
            return not self < other
        return False

    def __eq__(self, other):
        """Return whether this range is equal to the `other` range."""
        return self.mtype == other.mtype and \
            self.subtype == other.subtype and \
            self.quality == other.quality and \
            self.extensions == other.extensions

    def __str__(self):
        """Return a string representation of this range."""
        return self._str
