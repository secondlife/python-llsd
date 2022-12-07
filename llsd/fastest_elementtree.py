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

# TODO: drop version sensitivity, replacing entire module with:
#from xml.etree.ElementTree import *
#ElementTreeError = ParseError

##
# Using cElementTree might cause some unforeseen problems, so here's a
# convenient off switch during development and testing.
_use_celementree = True

# xml.etree.cElementTree has been deprecated since Python 3.3.
# For speed in the common case of Python 3.3+, don't even start with that.
import sys
if sys.version_info[:2] >= (3, 3):
    _use_celementree = False

try:
    # nat wishes for a nicer way to skip even attempting cElementTree than by
    # explicitly raising ImportError. The problem is that we want to be able
    # to 'import *' into the global namespace, which forbids packaging any of
    # this logic in a function. Nor can we 'return' early from a module. It
    # seems the only way to avoid the explicit exception would be to restate
    # the entirety of each 'except ImportError' clause, which would be worse.
    if not _use_celementree:
        raise ImportError()
    # Python 2.5 and above.
    from xml.etree.cElementTree import *
    ElementTreeError = SyntaxError
except ImportError:
    try:
        # Python 2.5 and above: the common case.
        from xml.etree.ElementTree import *
        try:
            # Python 3
            ElementTreeError = ParseError
        except NameError:
            # The older Python ElementTree module uses Expat for parsing.
            from xml.parsers.expat import ExpatError as ElementTreeError
    except ImportError:
        # Python 2.3 and 2.4.
        try:
            if not _use_celementree:
                raise ImportError()
            from cElementTree import *
            ElementTreeError = SyntaxError
        except ImportError:
            from elementtree.ElementTree import *
