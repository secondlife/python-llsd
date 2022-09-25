"""
Concealing some gnarly import logic in here. This should export
the interface of elementtree.

The parsing exception raised by the underlying library depends on the
ElementTree implementation we're using, so we provide an alias here.

Generally, you can use this module as a drop in replacement for how
you would use ElementTree or cElementTree.

<pre>
from fastest_elementtree import fromstring
fromstring(...)
</pre>

Use ElementTreeError as the exception type for catching parsing
errors.
"""

##
# Using cElementTree might cause some unforeseen problems, so here's a
# convenient off switch during development and testing.
_use_celementree = True

try:
    if not _use_celementree:
        raise ImportError()
    # Python 2.3 and 2.4.
    from cElementTree import *
    ElementTreeError = SyntaxError
except ImportError:
    try:
        if not _use_celementree:
            raise ImportError()
        # Python 2.5 and above.
        from xml.etree.cElementTree import *
        ElementTreeError = SyntaxError
    except ImportError:
        # Pure Python code.
        try:
            # Python 2.3 and 2.4.
            from elementtree.ElementTree import *
        except ImportError:
            # Python 2.5 and above.
            from xml.etree.ElementTree import *

        # The pure Python ElementTree module uses Expat for parsing.
        from xml.parsers.expat import ExpatError as ElementTreeError
