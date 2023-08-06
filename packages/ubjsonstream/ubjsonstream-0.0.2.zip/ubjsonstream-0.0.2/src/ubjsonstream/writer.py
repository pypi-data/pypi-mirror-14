'''
Created on 10 lut 2016

@author: dyucu_000
'''

# pylint: disable=too-few-public-methods

from decimal import Decimal
from logging import getLogger
from struct import pack

from ubjsonstream import NOOP


class SerializationException(Exception):
    """
        Exception raised when unsupported object is to be serialized.
    """


class Serializer():
    """
        Base class for all serializers.
    """

    def __init__(self, obj):
        """
            @param obj: Object to be serialized.
        """

        self._obj = obj
        self.log = getLogger(self.__class__.__name__)

    @classmethod
    def get_marker(cls):
        """
            Returns get_marker this class serializes.
            @return int
        """

    # pylint: disable=R0201
    def get_value(self):
        """
            Generates serialized bytearray of this object.
            @return bytearray
        """

        return bytearray()

    def serialize(self):
        """
            Returns bytearray with both get_marker and get_value.
            @return bytearray
        """
        return bytearray([self.get_marker()]) + self.get_value()

    def pretty_marker(self):
        """
            Returns prettily-serialized market.
            @return str
        """
        return "[" + chr(self.get_marker()) + "]"

    # pylint: disable=unused-argument
    def pretty_value(self, indent=0):
        """
            Returns prettily-serialized get_value.
            @param indent: Optional information about indentation of self.
            This is used by array/object serializers to corrently indent their children.
            @return str
        """
        return ""

    def _pretty_indent(self, indent):
        return "".join(["    " for _ in range(indent)])

    def pretty_serialize(self, indent=0):
        """
            Prettily serializes both get_marker and get_value.
            @param indent: Optional information about indentation of self.
            This is used by array/object serializers to corrently indent their children.
            @return str
        """
        return self.pretty_marker() + self.pretty_value(indent)


class SerializerMatcher():
    """
        Base class of serializer matchers. Serializer matcher chooces the best
        serializer for given object. Or none.
    """

    # pylint: disable=unused-argument
    # pylint: disable=no-self-use
    def matches_to(self, obj):
        """
            @param obj: Object to serialize.
            @returns SerializerMatcher subclass, or None.
        """

        return False


class NullSerializer(Serializer):

    """
        Serializes null.
    """

    @classmethod
    def get_marker(cls):
        return 90


class NullMatcher(SerializerMatcher):

    """
        Matches None.
    """

    def matches_to(self, obj):
        if obj is None:
            return NullSerializer


class NoopSerializer(Serializer):

    """
        Serializes noop.
    """
    @classmethod
    def get_marker(cls):
        return 78


class NoopMatcher(SerializerMatcher):

    """
        Matches noop.
    """

    def matches_to(self, obj):
        if obj == NOOP:
            return NoopSerializer


class TrueSerializer(Serializer):

    """
        Serializes true.
    """
    @classmethod
    def get_marker(cls):
        return 84


class TrueMatcher(SerializerMatcher):

    """
        Matches true.
    """

    def matches_to(self, obj):
        if obj is True:
            return TrueSerializer


class FalseSerializer(Serializer):

    """
        Serializes false.
    """
    @classmethod
    def get_marker(cls):
        return 70


class FalseMatcher(SerializerMatcher):

    """
        Matches false.
    """

    def matches_to(self, obj):
        if obj is False:
            return FalseSerializer


class Uint8Serializer(Serializer):

    """
        Serializes uint8.
    """

    @classmethod
    def get_marker(cls):
        return 85

    def get_value(self):
        return pack('B', self._obj)

    def pretty_value(self, indent=0):
        return "[" + str(self._obj) + "]"


class Int8Serializer(Serializer):

    """
        Serializes int8.
    """

    @classmethod
    def get_marker(cls):
        return 105

    def get_value(self):
        return pack('b', self._obj)

    def pretty_value(self, indent=0):
        return "[" + str(self._obj) + "]"


class Int16Serializer(Serializer):

    """
        Serializes int16.
    """

    @classmethod
    def get_marker(cls):
        return 73

    def get_value(self):
        return pack('h', self._obj)

    def pretty_value(self, indent=0):
        return "[" + str(self._obj) + "]"


class Int32Serializer(Serializer):

    """
        Serializes int32.
    """

    @classmethod
    def get_marker(cls):
        return 108

    def get_value(self):
        return pack('i', self._obj)

    def pretty_value(self, indent=0):
        return "[" + str(self._obj) + "]"


class Int64Serializer(Serializer):

    """
        Serializes int64.
    """

    @classmethod
    def get_marker(cls):
        return 76

    def get_value(self):
        return pack('q', self._obj)

    def pretty_value(self, indent=0):
        return "[" + str(self._obj) + "]"


class IntMatcher(SerializerMatcher):

    """
        Matches int to one of (u)int{8,16,32,64} classes.
    """

    def matches_to(self, obj):
        if isinstance(obj, int):
            if obj >= 0 and obj < 0x80:
                return Uint8Serializer
            elif obj >= -0x80 and obj < 0x80:
                return Int8Serializer
            elif obj >= -0x8000 and obj < 0x8000:
                return Int16Serializer
            elif obj >= -0x80000000 and obj < 0x80000000:
                return Int32Serializer
            else:
                return Int64Serializer


class Float64Serializer(Serializer):
    """
        Serializes float64.
    """

    @classmethod
    def get_marker(cls):
        return 68

    def get_value(self):
        return pack('d', self._obj)

    def pretty_value(self, indent=0):
        return "[" + str(self._obj) + "]"


class FloatMatcher(SerializerMatcher):

    """
        Matches float to float64.
        @todo Match to float32 too.
    """

    def matches_to(self, obj):
        if isinstance(obj, float):
            return Float64Serializer


class StrSerializer(Serializer):

    """
        Serializes strings.
    """

    def __init__(self, obj):
        super(StrSerializer, self).__init__(obj)

        alen = len(self._obj)
        self._len_matcher = IntMatcher().matches_to(alen)(alen)

    @classmethod
    def get_marker(cls):
        return 83

    def get_value(self):
        out = bytearray([self._len_matcher.get_marker()]) + \
            self._len_matcher.get_value()
        out += bytearray([ord(x) for x in self._obj])
        return out

    def pretty_value(self, indent=0):
        return self._len_matcher.pretty_serialize() + "[" + str(self._obj) + "]"


class StrMatcher(SerializerMatcher):

    """
        matches strings.
    """

    def matches_to(self, obj):
        if isinstance(obj, str):
            return StrSerializer


class HPNSerializer(Serializer):

    """
        Serializes HPNs.
    """

    def __init__(self, obj):
        super(HPNSerializer, self).__init__(obj)

        alen = len(str(self._obj))
        self._len_matcher = IntMatcher().matches_to(alen)(alen)

    @classmethod
    def get_marker(cls):
        return 72

    def get_value(self):
        out = bytearray([self._len_matcher.get_marker()]) + \
            self._len_matcher.get_value()
        out += bytearray([ord(x) for x in str(self._obj)])
        return out

    def pretty_value(self, indent=0):
        return self._len_matcher.pretty_serialize() + "[" + str(self._obj) + "]"


class HPNMatcher(SerializerMatcher):

    """
        Matches Decimal to HPNs.
    """

    def matches_to(self, obj):
        if isinstance(obj, Decimal):
            return HPNSerializer


def get_serializer_if_all_are_same(arr):
    """
        Checks that all items in the list belong to same serializer class.
        If true, it is returned.
        @param arr: list()
        @return SerializerMatcher class, or None.
    """

    if len(arr) == 0:
        return None

    iterator = iter(arr)

    LOG.debug("get serializer if all are same")
    first_writer = try_match_serializer(next(iterator))

    for item in iterator:
        next_writer = try_match_serializer(item)
        if first_writer != next_writer:
            LOG.debug("nope")
            return None

    LOG.debug("all are the same!")
    return first_writer


class ArraySerializer(Serializer):

    """
        Serializes arrays.

        Techniques:
        # if length <= 3, this will be unoptimized
        # else this is optimized with at least length
            # if all items belong to same serializer, then also optimized with type.

        @todo For int serializers, match to greatest one possible.
        Currently 99x int8 and 1x int16 will fail to match to one type.
        It might be worth.
    """

    def __init__(self, obj):
        super(ArraySerializer, self).__init__(obj)

        self.__item_serializer = None
        self.__length_serializer = None

        # Never optimize for <= 3 values. Not worth it.
        worth_optimizing = (len(obj) > 3)
        if worth_optimizing:
            serializer = get_serializer_if_all_are_same(obj)
            if serializer is not None:
                self.log.debug(
                    "optimizing by serializer: %s", serializer)
                self.__item_serializer = serializer

            alen = len(self._obj)
            self.__length_serializer = IntMatcher().matches_to(
                alen)(alen)
            self.log.debug(
                "optimizing by length: %d", alen)

    @classmethod
    def get_marker(cls):
        return 91

    def get_value(self):
        out = bytearray()

        if self.__item_serializer is not None:
            out += bytearray([36, self.__item_serializer.get_marker()])

        if self.__length_serializer is not None:
            out += bytearray([35])
            out += self.__length_serializer.serialize()

        for item in self._obj:
            if self.__item_serializer is not None:
                out += self.__item_serializer(item).get_value()
            else:
                out += serialize(item)

        if self.__length_serializer is None:
            out += bytearray([93])

        return out

    def pretty_value(self, indent=0):

        out = ""

        if self.__item_serializer is not None:
            out += "[$][{}]".format(
                chr(self.__item_serializer.get_marker()))

        if self.__length_serializer is not None:
            out += "[#]" + \
                self.__length_serializer.pretty_serialize()

        if len(self._obj) > 0:
            the_indent = self._pretty_indent(indent + 1)

            for item in self._obj:
                out += "\n" + the_indent
                if self.__item_serializer is not None:
                    out += self.__item_serializer(
                        item).pretty_value(indent + 1)
                else:
                    out += pretty_serialize(item, indent + 1)

            out += "\n" + self._pretty_indent(indent)

        out += "[]]"

        return out


class ArrayMatcher(SerializerMatcher):

    """
        Matches list to arrays.
    """

    def matches_to(self, obj):
        if isinstance(obj, list):
            return ArraySerializer


class ObjectSerializer(Serializer):

    """
        Serializes object.

        Techniques:
        # if length <= 3, this will be unoptimized
        # else this is optimized with at least length
            # if all items belong to same serializer, then also optimized with type.

        @todo For int serializers, match to greatest one possible.
        Currently 99x int8 and 1x int16 will fail to match to one type.
        It might be worth.
    """

    def __init__(self, obj):
        super(ObjectSerializer, self).__init__(obj)

        self.__item_serializer = None
        self.__length_serializer = None

        # Never optimize for <= 3 values. Not worth it.
        worth_optimizing = (len(obj) > 3)
        if worth_optimizing:
            serializer = get_serializer_if_all_are_same(obj.values())
            if serializer is not None:
                self.log.debug(
                    "optimizing by serializer: %s", serializer)
                self.__item_serializer = serializer

            alen = len(self._obj)
            self.__length_serializer = IntMatcher().matches_to(
                alen)(alen)
            self.log.debug(
                "optimizing by length: %d", alen)

    @classmethod
    def get_marker(cls):
        return 123

    def get_value(self):
        out = bytearray()

        if self.__item_serializer is not None:
            out += bytearray([36, self.__item_serializer.get_marker()])

        if self.__length_serializer is not None:
            out += bytearray([35])
            out += self.__length_serializer.serialize()

        for key, value in self._obj.items():
            out_key = StrSerializer(key).get_value()
            out_value = None

            if self.__item_serializer is not None:
                out_value = self.__item_serializer(
                    value).get_value()
            else:
                out_value = serialize(value)

            self.log.debug("key: %d\n%s", len(out_key), out_key)
            self.log.debug("get_value: %d\n%s", len(out_value), out_value)

            out += out_key + out_value

        if self.__length_serializer is None:
            out += bytearray([125])

        return out

    def pretty_value(self, indent=0):

        out = ""

        if self.__item_serializer is not None:
            out += "[$][{}]".format(
                chr(self.__item_serializer.get_marker()))

        if self.__length_serializer is not None:
            out += "[#]" + \
                self.__length_serializer.pretty_serialize()

        if len(self._obj) > 0:
            the_indent = self._pretty_indent(indent + 1)

            for key, value in self._obj.items():
                out += "\n" + the_indent
                out += StrSerializer(key).pretty_value()

                if self.__item_serializer is not None:
                    out += self.__item_serializer(
                        value).pretty_value(indent + 1)
                else:
                    out += pretty_serialize(value, indent + 1)

            out += "\n" + self._pretty_indent(indent)

        out += "[}]"

        return out


class ObjectMatcher(SerializerMatcher):

    """
        Matches dicts to objects.
    """

    def matches_to(self, obj):
        if isinstance(obj, dict):
            return ObjectSerializer


# Recognized serializers.
SERIALIZER_MATCHERS = [NullMatcher(), NoopMatcher(), TrueMatcher(), FalseMatcher(
), IntMatcher(), FloatMatcher(), StrMatcher(), HPNMatcher(), ArrayMatcher(), ObjectMatcher()]

# Local logger.
LOG = getLogger('writer')


def try_match_serializer(obj):
    """
        Tries to match a serializer for given object, and returns one.
        @param obj: Object to serializer.
        @return MatcherSerializer subclass, or None.
    """

    LOG.debug("try match serializer for object: %s", obj)
    for matcher in SERIALIZER_MATCHERS:
        serializer = matcher.matches_to(obj)
        if serializer is not None:
            LOG.debug(
                "matched serializer %s from matcher %s", serializer, matcher)
            return serializer

    LOG.debug("none matched")
    return None


def serialize(obj):
    """
        Serializes object to UBJson syntax.
        @param obj: None/NOOP/True/False/int/float/string/Decimal/array/dict.
        @return: bytearray
    """

    serializer = try_match_serializer(obj)
    if serializer is None:
        raise SerializationException("Cannot serialize object: {}".format(obj))

    out = serializer(obj).serialize()
    LOG.debug("serialized to: %d %s", len(out), out.decode('latin-1'))
    return out


def pretty_serialize(obj, indent=0):
    """
        Prettily-serializes object to UBJson syntax.
        @param obj: None/NOOP/True/False/int/float/string/Decimal/array/dict.
        @return: string
    """

    serializer = try_match_serializer(obj)
    if serializer is None:
        raise SerializationException("Cannot pretty-serialize object: {}".format(obj))

    out = serializer(obj).pretty_serialize(indent=indent)
    LOG.debug(
        "pretty-serialized to: %d\n%s", len(out), out)
    return out
