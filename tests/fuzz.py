from __future__ import division

import random
import string
import struct
import time
import uuid
from datetime import date, datetime, timedelta

# Ridiculous optimization -- compute once ahead of time so choice() doesn't
# call len(string.printable) a bajillion times.  Amazing it makes a difference.
printable_len = len(string.printable)


import llsd
from llsd.base import is_string


class LLSDFuzzer(object):
    """Generator of fuzzed LLSD objects.

    The :class:`LLSDFuzzer` constructor accepts a *seed* argument, which becomes the
    seed of the PRNG driving the fuzzer.  If *seed* is None, the current time is
    used.  The seed is also stored in the seed attribute on the object, which
    is useful for producing deterministic trials.
    """
    def __init__(self, seed=None):
        self.r = random.Random()
        if seed is None:
            seed = time.time()
        self.seed = seed
        self.r.seed(seed)

    def random_boolean(self):
        """Returns a random boolean."""
        return bool(self.r.getrandbits(1))

    def random_integer(self):
        """Returns a random integral value."""
        return self.r.getrandbits(32) - 2**31

    def random_real(self):
        """Returns a random floating-point value."""
        return self.r.uniform(-1000000.0, 1000000.0)

    def random_uuid(self):
        """Returns a random UUID object."""
        # use bytes from our local Random, instead of the various uuid
        # constructors, so as to be completely deterministic
        return uuid.UUID(int= self.r.getrandbits(128))

    def _string_length(self):
        """Returns a 'reasonable' random length for a string.  The current
        distribution is such that it usually returns a number less than 25, but
        occasionally can return numbers as high as a few thousand."""
        return int(self.r.lognormvariate(2.7, 1.3))

    def random_printable(self, length = None):
        """Returns a string of random printable characters with length *length*.
        Uses a random length if none is specified."""
        if length is None:
            length = self._string_length()
        return ''.join([string.printable[int(self.r.random() * printable_len)]
                        for x in range(length)])

    def random_unicode(self, length = None):
        """Returns a string of random unicode characters with length *length*.
        Uses a random length if none is specified."""
        # length of the unicode string will be only vaguely
        # close to the specified length because we're not bothering
        # to generate valid utf-16 and therefore many of our
        # bytes may be discarded as invalid
        if length is None:
            length = self._string_length()
        bytes = self.random_bytes(length * 2)
        # utf-16 instead of utf-8 or 32 because it's way faster
        return bytes.decode('utf-16', 'ignore')

    def random_bytes(self, length = None):
        """Returns a string of random bytes with length *length*.
        Uses a random length if none is specified."""
        if length is None:
            length = self._string_length()

        if length % 8 == 0:
            num_chunks = length // 8
        else:
            num_chunks = length // 8 + 1

        # this appears to be the fastest way to generate random byte strings
        packstr = 'Q'*num_chunks
        randchunks = [self.r.getrandbits(64) for i in range(num_chunks)]
        return struct.pack(packstr, *randchunks)[:length]

    def random_binary(self, length=None):
        """Returns a random llsd.binary object containing *length* random
        bytes.  Uses a random length if none is specified."""
        return llsd.binary(self.random_bytes(length))

    def random_date(self):
        """Returns a random date within the range of allowed LLSD dates (1970
        to 2038)"""
        return datetime.utcfromtimestamp(0) + \
               timedelta(seconds=self.r.getrandbits(31))

    def random_uri(self, length=None):
        """Returns a random llsd.uri object containing *length* random
        printable characters (so, not necessarily a legal uri). Uses a random
        length if none is specified."""
        return llsd.uri(self.random_printable(length))

    def _container_size(self):
        "Returns a random 'reasonable' container size."
        return int(round(self.r.expovariate(0.3)+1))

    def random_map(self):
        """Returns a Python dictionary which has string keys and
        randomly-chosen values.  It is single-level; none of the
        values are themselves maps or arrays."""
        retval = {}
        for x in range(self._container_size()):
            if self.random_boolean():
                key = self.random_unicode()
            else:
                key = self.random_printable()
            value = self.random_atom(include_containers=False)
            retval[key] = value
        return retval

    def random_array(self):
        """Returns a random Python array which is populated
        with random values.  It is single-level; none of the
        values are themselves maps or arrays."""
        return [self.random_atom(include_containers=False)
                for x in range(self._container_size())]

    random_generators = [
        lambda self: None,
        random_boolean,
        random_integer,
        random_real,
        random_uuid,
        random_printable,
        random_unicode,
        random_binary,
        random_date,
        random_uri,
        random_map,
        random_array]

    def random_atom(self, include_containers=True):
        """Returns a random LLSD atomic value."""
        if include_containers:
            return self.r.choice(self.random_generators)(self)
        else:
            return self.r.choice(self.random_generators[:-2])(self)

    def permute_undef(self, val):
        """Permutes undef, the return value is always None."""
        return None

    def permute_boolean(self, val):
        """Permutes booleans, the return value is always a boolean."""
        return self.random_boolean()

    integer_options = [
        lambda s, v: -v,
        lambda s, v: 0,
        lambda s, v: v + s.r.randint(-(v**4), (v**4)),
        lambda s, v: 4294967296,  # 2^32
        lambda s, v: -2147483649,  # -2^31 - 1
        lambda s, v: 18446744073709551616, # 2^64
        lambda s, v: s.random_integer(),
        lambda s, v: v *  ((s.r.getrandbits(16) - 2**15) or 1),
        lambda s, v: v // ((s.r.getrandbits(16) - 2**15) or 1),
        lambda s, v: v + s.random_integer(),
        lambda s, v: v - s.random_integer(),
        lambda s, v: v *  ((s.r.getrandbits(8) - 2**7) or 1),
        lambda s, v: v // ((s.r.getrandbits(8) - 2**7) or 1)
    ]

    def permute_integer(self, val):
        """Generates variations on a given int or long,
        returned value is an int or a long."""
        return self.r.choice(self.integer_options)(self, val)

    real_options = [
        lambda s, v: -v,
        lambda s, v: 0.0,
        lambda s, v: v/float(2**64),
        lambda s, v: v*float(2**64),
        lambda s, v: 1E400,
        lambda s, v: -1E400,
        lambda s, v: float('nan'),
        lambda s, v: s.random_real(),
        lambda s, v: v * (s.r.random() - 0.5),
        lambda s, v: v / (s.r.random() - 0.5),
        lambda s, v: v + s.random_real(),
        lambda s, v: v - s.random_real(),
        lambda s, v: v * s.random_real(),
        lambda s, v: v / s.random_real()
    ]

    def permute_real(self, val):
        """Generates variations on a float, the returned
        value is a float."""
        return self.r.choice(self.real_options)(self, val)

    def permute_uuid(self, val):
        """ Generates variations on a uuid, the returned value is a uuid."""
        return uuid.UUID(int=self.r.getrandbits(128) ^ val.int)

    def rand_idx(self, val):
        """Return a random index into the value."""
        if len(val) == 0:
            return 0
        return self.r.randrange(0, len(val))

    stringlike_options = [
        lambda s,v,strgen: strgen() + v,
        lambda s,v,strgen: v + strgen(),
        lambda s,v,strgen: v[s.rand_idx(v):],
        lambda s,v,strgen: v[:s.rand_idx(v)],
        lambda s,v,strgen: v[:s.rand_idx(v)] + strgen() + v[s.rand_idx(v):]
        ]

    def _permute_stringlike(self, val, strgen):
        if len(val) == 0:
            return strgen()
        else:
            return self.r.choice(self.stringlike_options)(self, val, strgen)

    def permute_string(self, val):
        """Generates variations on a given string or unicode.  All
        generated values are strings/unicodes."""
        assert is_string(val)
        def string_strgen(length = None):
            if self.random_boolean():
                return self.random_printable(length)
            else:
                return self.random_unicode(length)
        return self._permute_stringlike(val, string_strgen)

    def permute_binary(self, val):
        """Generates variations on a given binary value.  All
        generated values are llsd.binary."""
        assert isinstance(val, llsd.binary)
        return llsd.binary(self._permute_stringlike(val, self.random_bytes))

    def _date_clamp(self, val):
        if val.year >= 2038:
            raise OverflowError()
        elif val.year < 1970:
            return date(1970, val.month, val.day)
        else:
            return val

    date_options = [
        lambda s, v: s._date_clamp(v + timedelta(
                                   seconds=s.r.getrandbits(21) - 2**20,
                                   microseconds=s.r.getrandbits(20))),
        lambda s, v: datetime.utcfromtimestamp(0),
        lambda s, v: date(v.year, v.month, v.day),
        lambda s, v: datetime.utcfromtimestamp(2**31-86400),
    ]

    def permute_date(self, val):
        """Generates variations on a given datetime.  All generated
        values are datetimes within the valid llsd daterange."""
        assert isinstance(val, (datetime, date))
        # have to retry a few times because the random-delta option
        # sometimes gets out of range
        while True:
            try:
                return self.r.choice(self.date_options)(self, val)
            except (OverflowError, OSError):
                continue

    def permute_uri(self, val):
        """Generates variations on a given uri.  All
        generated values are llsd.uri."""
        assert isinstance(val, llsd.uri)
        return llsd.uri(self._permute_stringlike(val, self.random_printable))

    def _permute_map_permute_value(self, val):
        if len(val) == 0:
            return {}
        # choose one of the keys from val
        k = self.r.choice(list(val))
        permuted = val.copy()
        permuted[k] = next(self.structure_fuzz(val[k]))
        return permuted

    def _permute_map_key_delete(self, val):
        if len(val) == 0:
            return {}
        # choose one of the keys from val
        k = self.r.choice(list(val))
        permuted = val.copy()
        permuted.pop(k, None)
        return permuted

    def _permute_map_new_key(self, val):
        permuted = val.copy()
        if len(val) > 0 and self.random_boolean():
            # choose one of the keys from val
            new_key = self.permute_string(self.r.choice(list(val)))
        else:
            new_key = self.random_unicode()

        permuted[new_key] = self.random_atom()
        return permuted

    def _permute_map_permute_key_names(self, val):
        if len(val) == 0:
            return {}
        # choose one of the keys from val
        k = self.r.choice(list(val))
        k = self.permute_string(k)
        permuted = val.copy()
        v = permuted.pop(k, None)
        permuted[k] = v
        return permuted


    map_sub_permuters = (_permute_map_permute_value,
                         _permute_map_permute_value,
                         _permute_map_key_delete,
                         _permute_map_new_key,
                         _permute_map_permute_key_names)

    def permute_map(self, val):
        """ Generates variations on an input dict via a variety of steps.
        The return value is a dict."""
        assert isinstance(val, dict)
        permuted = self.r.choice(self.map_sub_permuters)(self, val)
        for i in range(int(self.r.expovariate(0.5)) + 1):
            permuted = self.r.choice(self.map_sub_permuters)(self, permuted)
        return permuted

    def _permute_array_permute_value(self, val):
        idx = self.r.randrange(0, len(val))
        permuted = list(val)
        permuted[idx] = next(self.structure_fuzz(val[idx]))
        return permuted

    def _permute_array_subsets(self, val):
        return self.r.sample(val, self.r.randint(1, len(val)))

    def _permute_array_inserting(self, val):
        new_idx = self.r.randint(0, len(val))
        inserted = self.random_atom()
        permuted = list(val[:new_idx]) + [inserted] + list(val[new_idx:])
        return permuted

    def _permute_array_reorder(self, val):
        permuted = list(val)
        swaps = self.r.randrange(0, len(val))
        for s in range(swaps):
            i = self.r.randrange(0, len(val))
            j = self.r.randrange(0, len(val))
            permuted[i], permuted[j] = permuted[j], permuted[i]
        return permuted

    array_sub_permuters = (_permute_array_permute_value,
                           _permute_array_permute_value,
                           _permute_array_subsets,
                           _permute_array_inserting,
                           _permute_array_reorder)

    def permute_array(self, val):
        """ Generates variations on an input array via a variety of steps.
        The return value is a dict."""
        assert isinstance(val, (list, tuple))
        permuted = self.r.choice(self.array_sub_permuters)(self, val)
        for i in range(int(self.r.expovariate(0.5)) + 1):
            permuted = self.r.choice(self.array_sub_permuters)(self, permuted)
        if self.random_boolean():
            permuted = tuple(permuted)
        return permuted

    permuters = {
        type(None):       permute_undef,
        bool:             permute_boolean,
        int:              permute_integer,
        llsd.LongType:    permute_integer,
        float:            permute_real,
        uuid.UUID:        permute_uuid,
        str:              permute_string,
        llsd.UnicodeType: permute_string,
        llsd.binary:      permute_binary,
        datetime:         permute_date,
        date:             permute_date,
        llsd.uri:         permute_uri,
        dict:             permute_map,
        list:             permute_array,
        tuple:            permute_array}

    def structure_fuzz(self, starting_structure):
        """ Generates a series of Python structures
        based on the input structure."""
        permuter = self.permuters[type(starting_structure)]
        while True:
            if self.r.getrandbits(2) == 0:
                yield self.random_atom()
            else:
                yield permuter(self, starting_structure)

    def _random_numeric(self, length):
        return ''.join([self.r.choice(string.digits)
                        for x in range(length)])

    def _dirty(self, val):
        idx1 = self.rand_idx(val)
        idx2 = idx1 + int(round(self.r.expovariate(0.1)))
        if self.random_boolean():
            # replace with same-length string
            subst_len = idx2 - idx1
        else:
            subst_len = int(round(self.r.expovariate(0.1)))

        if self.random_boolean():
            # use printable
            if self.random_boolean():
                replacement = self._random_numeric(subst_len).encode('latin-1')
            else:
                replacement = self.random_printable(subst_len).encode('latin-1')
        else:
            replacement = self.random_bytes(subst_len)

        return val[:idx1] + replacement + val[idx2:]

    def _serialized_fuzz(self, it, formatter):
        while True:
            struct = next(it)
            try:
                text = formatter(struct)
            except llsd.LLSDSerializationError:
                continue
            yield text
            dirtied = self._dirty(text)
            for i in range(int(round(self.r.expovariate(0.3)))):
                dirtied = self._dirty(dirtied)
            yield dirtied

    def binary_fuzz(self, starting_structure):
        """ Generates a series of strings which are meant to be tested against
        a service that parses binary LLSD."""
        return self._serialized_fuzz(
                     self.structure_fuzz(starting_structure),
                     llsd.format_binary)

    def xml_fuzz(self, starting_structure):
        """ Generates a series of strings which are meant to be tested against
        a service that parses XML LLSD."""
        return self._serialized_fuzz(
                     self.structure_fuzz(starting_structure),
                     llsd.format_xml)

    def notation_fuzz(self, starting_structure):
        """ Generates a series of strings which are meant to be tested against
        a service that parses the LLSD notation serialization."""
        return self._serialized_fuzz(
                     self.structure_fuzz(starting_structure),
                     llsd.format_notation)