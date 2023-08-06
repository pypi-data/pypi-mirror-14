'''
Created on 23 lis 2015

@author: tsieprawski
'''

from decimal import Decimal
from logging import getLogger
from struct import unpack

from ubjsonstream import NOOP


class DeserializationException(Exception):
    """
        Exception raised when reading badly formatted data.
    """


class Child(object):
    """
        Child is an abstract class for processing single bytes.
        Children can be put in parent-child hierarchy (thus the name)
        in stack to easily separate responsibilities.

        The topmost "child" is always the Deserializer class.
    """

    def __init__(self, parent):
        """
            @param parent: Parent.
        """

        # Parent of this child.
        self.parent = parent

        # Logger.
        self.log = getLogger(self.__class__.__name__)

    def feed(self, pos, character):  # pragma: no cover
        """
            Feeds the child with a single character.
            @param pos: Position of the character in original input array.
            @param character: One-char string.
        """

        pass

    def _request_control(self):
        """
            Gives control to this child in the reader.
            Now every incoming character will be processed in this child.
        """

        self.log.debug("request control")
        self.give_control_to(self)

    def give_control_to(self, child):
        """
            Gives control to specified child in the reader.
            Now every incoming character will be processed in specified child.
            @param child: The child.
        """

        self.log.debug("give control to: %s", child)
        self.parent.give_control_to(child)

    def on_produced(self, product):
        """
            Event incoming from self's children upon producing an object
            from parsed input.
            @param product: Produced object.
        """

        self.parent.on_produced(product)

    def on_got_control(self):
        """
            Event incoming upon getting control.
        """

        pass

    def __str__(self):
        return self.__class__.__name__


class GetMarker(Child):
    """
        The child that expects a get_marker and then passes control to
        specified child class.
    """

    def __init__(self, parent):
        super(GetMarker, self).__init__(parent)
        self.__markers = {}

    def register_marker(self, get_marker, child_class):
        """
            Registers a possible get_marker for processing.
            @param get_marker: Marker, byte 0-255.
            @param child_class: Child class to be constructed and passed control
            upon receiving this get_marker.
        """

        self.log.debug(
            "register get_marker: %d => %s", get_marker, child_class)
        self.__markers[get_marker] = child_class

    def register_markers(self, markers):
        """
            Registers many markers at once.
            @param markers: dict get_marker => child_class.
        """

        for get_marker, klass in markers.items():
            self.register_marker(get_marker, klass)

    def feed(self, pos, character):
        """
            @raise DeserializationException: When unregistered character is received.
        """

        self.log.debug("got get_marker: %d", character)

        if character not in self.__markers:
            raise DeserializationException(
                "illegal get_marker at {}: {}".format(pos, character))

        child_klass = self.__markers[character]
        self.parent.on_got_marker(child_klass)


class ProduceNext(Child):
    """
        Meta-child that processes a get_marker and its related input.
        Effectively this works like that:
        * pass control to child GetMarker,
        * pass control to newly created child from GetMarker,
        * return produced object to parent.
    """

    def __init__(self, parent, markers):
        """
            @param markers: dict get_marker => child class.
        """

        super(ProduceNext, self).__init__(parent)
        self.__markers = markers

    def on_got_control(self):

        self.log.debug("produce next")

        child = GetMarker(self)
        child.register_markers(self.__markers)
        self.give_control_to(child)

    def on_got_marker(self, child_klass):
        """
            Event incoming from GetMarker instance upon getting
            a supported get_marker.
        """

        self.log.debug("got get_marker: %s", child_klass)

        child = child_klass(self)
        self.give_control_to(child)


class ProduceNull(Child):
    """
        Produces None (=null) and returns control up.
    """

    def on_got_control(self):
        self.log.debug("produce")
        self.parent.on_produced(None)


class ProduceNoop(Child):
    """
        Produces NOOP and returns control up.
    """

    def on_got_control(self):
        self.log.debug("produce")
        self.parent.on_produced(NOOP)


class ProduceTrue(Child):
    """
        Produces True and returns control up.
    """

    def on_got_control(self):
        self.log.debug("produce")
        self.parent.on_produced(True)


class ProduceFalse(Child):
    """
        Produces False and returns control up.
    """

    def on_got_control(self):
        self.log.debug("produce")
        self.parent.on_produced(False)


class ProduceFirstOfStruct(Child):
    """
        Awaits some bytes, constructs a struct from given format
        and returns its first item.
    """

    def __init__(self, parent, aformat, length):
        """
            @param aformat: Format recognized by unpack() method.
            @param length: Number of bytes to read.
        """

        super(ProduceFirstOfStruct, self).__init__(parent)
        self.__format = aformat
        self.__length = length
        self.__bytes = bytearray()

    def on_got_control(self):
        self.log.debug(
            "want %d bytes for format: %s", self.__length, self.__format)

    def feed(self, pos, character):
        self.__bytes.append(character)
        if len(self.__bytes) != self.__length:
            return

        self.log.debug("produce with format: %s", self.__format)
        self.log.debug("        with bytes: %s", self.__bytes)

        obj = unpack(self.__format, self.__bytes)[0]
        self.log.debug("%s", obj)

        self.on_produced(obj)


class ProduceChar(Child):
    """
        Produces a character from next byte and returns control up.
    """

    def on_got_control(self):
        self.log.debug("want the char")

    def feed(self, pos, character):
        ret = chr(character)
        self.log.debug("%s", ret)
        self.on_produced(ret)


class GetStringLength(Child):
    """
        This reads string's length and processes incoming string.
        Effectively this reads any int get_marker and passes control to ProduceString instance,
        which will produce the final string.
    """

    def __init__(self, parent):
        super(GetStringLength, self).__init__(parent)

    def on_got_control(self):
        self.log.debug("want length")
        self.give_control_to(ProduceNext(self, INT_MARKERS))

    def on_produced(self, obj):
        self.log.debug("length will be: %d", obj)
        self.give_control_to(ProduceString(self.parent, obj))


class ProduceString(Child):
    """
        Produces a string and returns control up.
    """

    def __init__(self, parent, length):
        """
            @param length: Expected length.
        """

        super(ProduceString, self).__init__(parent)
        self.__length = length
        self.__bytes = bytearray()

    def on_got_control(self):
        self.log.debug("want %d bytes for string", self.__length)
        if self.__length == 0:
            self.__got_whole()

    def __got_whole(self):

        ret = "".join([chr(x) for x in self.__bytes])
        self.log.debug("%s", ret)
        self.on_produced(ret)

    def feed(self, pos, character):
        self.__bytes.append(character)
        if len(self.__bytes) == self.__length:
            self.__got_whole()


class GetHPNLength(Child):
    """
        This reads HPN's length and processes incoming HPN.
        Effectively this reads any int get_marker and passes control to ProduceHPN instance,
        which will produce the final HPN.
    """

    def __init__(self, parent):
        super(GetHPNLength, self).__init__(parent)

    def on_got_control(self):
        self.log.debug("want length")
        self.give_control_to(ProduceNext(self, INT_MARKERS))

    def on_produced(self, obj):
        self.log.debug("length will be: %d", obj)
        self.give_control_to(ProduceHPN(self.parent, obj))


class ProduceHPN(Child):
    """
        Produces a Decimal from incoming HPN and returns control up.

        @note: We support a case when empty HPN arrives (this is 0-length) - we return "0" HPN.
    """

    def __init__(self, parent, length):
        super(ProduceHPN, self).__init__(parent)
        self.__length = length
        self.__bytes = bytearray()

    def on_got_control(self):
        self.log.debug("want %d bytes for string", self.__length)
        if self.__length == 0:
            self.__got_whole()

    def __got_whole(self):

        if len(self.__bytes) == 0:
            ret = Decimal("0")
        else:
            ret = Decimal("".join([chr(x) for x in self.__bytes]))

        self.log.debug("%s", ret)
        self.on_produced(ret)

    def feed(self, pos, character):
        self.__bytes.append(character)
        if len(self.__bytes) == self.__length:
            self.__got_whole()


class ProduceArrayBase(Child):
    """
        Base for any array producer.
    """

    def __init__(self, parent):
        super(ProduceArrayBase, self).__init__(parent)
        self._arr = []

    def on_got_marker(self, child_klass):
        """
            Event from implementing classes with child class of next array's item.
            This gives control to newly created child instance.
            When the child is produced, it will be added to the array.
        """

        child = child_klass(self)
        self.give_control_to(child)

    def on_produced(self, child):

        self.log.debug("item %d: %s", len(self._arr), child)
        self._arr.append(child)

    def _finish(self):
        self.log.debug("produced array with %d items", len(self._arr))
        self.parent.on_produced(self._arr)


class ProduceArrayUnoptimized(ProduceArrayBase):
    """
        Produces an unoptimized array.
        Unoptimized array has no predefined item type nor length.
        All items until "]" get_marker are added to the array as-they-are.
    """

    def on_got_control(self):

        self.log.debug("want next item")
        child = GetMarker(self)
        child.register_markers(STANDARD_MARKERS)
        child.register_marker(93, ProduceArrayEnd)
        self.give_control_to(child)

    def on_got_marker(self, child_klass):

        if child_klass == ProduceArrayEnd:
            self._finish()
            return

        super(ProduceArrayUnoptimized, self).on_got_marker(child_klass)

    def on_produced(self, child):

        super(ProduceArrayUnoptimized, self).on_produced(child)
        self._request_control()


class ProduceArrayOptimizedWithCount(ProduceArrayBase):
    """
        Produces array with expected length.
        Array will contain next length items as-they-are.
    """

    def __init__(self, parent, count):
        super(ProduceArrayOptimizedWithCount, self).__init__(parent)
        self.__count = count

    def on_got_control(self):

        if self.__count == 0:
            self._finish()
            return

        self.log.debug("want next item")
        child = GetMarker(self)
        child.register_markers(STANDARD_MARKERS)
        self.give_control_to(child)

    def on_produced(self, child):

        super(ProduceArrayOptimizedWithCount, self).on_produced(child)
        if len(self._arr) == self.__count:
            self._finish()
            return

        self.log.debug("want %d more", self.__count - len(self._arr))
        self._request_control()


class ProduceArrayOptimizedWithTypeCount(ProduceArrayBase):
    """
        Produces array with expected both type and length.
        This means:
        - there will be read length items,
        - because of knowing a type, they will be read without markers.

        For no-get_value markers (true/false/null/noop) this immedietely produces the array upon
        getting control. Otherwise it waits for items' values.
    """

    def __init__(self, parent, atype, count):
        super(ProduceArrayOptimizedWithTypeCount, self).__init__(parent)
        self.__type = atype
        self.__count = count

    def on_got_control(self):

        if self.__count == 0:
            self._finish()
            return

        self.__want_next_item()

    def __want_next_item(self):
        self.log.debug("want next item")
        self.on_got_marker(self.__type)

    def on_produced(self, child):

        super(ProduceArrayOptimizedWithTypeCount, self).on_produced(child)
        if len(self._arr) == self.__count:
            self._finish()
            return

        self.log.debug("want %d more", self.__count - len(self._arr))
        self.__want_next_item()


class ProduceArrayCount(Child):
    """
        Reads length of an array and passes it to the array.
        Depending on whether we knew the type before, the control will be passed
        to either optimized-with-type-and-count child, or to optimized-with-count only.
    """

    def __init__(self, parent, atype=None):
        super(ProduceArrayCount, self).__init__(parent)
        self.__type = atype

    def on_got_control(self):
        self.log.debug("want count")
        self.give_control_to(ProduceNext(self, INT_MARKERS))

    def on_produced(self, obj):
        self.log.debug("count will be: %d", obj)

        if self.__type is not None:
            self.give_control_to(
                ProduceArrayOptimizedWithTypeCount(self.parent, self.__type, obj))
        else:
            self.give_control_to(
                ProduceArrayOptimizedWithCount(self.parent, obj))


class ProduceArrayOptimizedWithType(Child):
    """
        Reads the only expected length get_marker and passes control to
        ProduceArrayCount.
    """

    def __init__(self, parent, atype):
        super(ProduceArrayOptimizedWithType, self).__init__(parent)
        self.__type = atype

    def on_got_control(self):

        self.log.debug("produce next")

        child = GetMarker(self)
        child.register_marker(35, ProduceArrayCount)
        self.give_control_to(child)

    # pylint: disable=unused-argument
    def on_got_marker(self, child_klass):
        """
            Event incoming when got type marker.
        """

        self.log.debug("will get count")
        self.give_control_to(ProduceArrayCount(self.parent, self.__type))


class ProduceArrayEnd(Child):
    """
        Sentinel class to indicate that the unoptimized array is ended.
    """


class ProduceObjectEnd(Child):
    """
        Sentinel class to indicate that the unoptimized object is ended.
    """


class ProduceArrayType(Child):
    """
        Reads a get_marker that will be the array's items' type.
        After reading the get_marker the control will be passed to
        ProduceArrayOptimizedWithType, that expects array length.
    """

    def on_got_control(self):

        self.log.debug("get type get_marker")

        child = GetMarker(self)
        child.register_markers(STANDARD_MARKERS)
        self.give_control_to(child)

    def on_got_marker(self, child_klass):
        """
            @todo
        """

        self.log.debug("type is: %s", child_klass)
        self.give_control_to(
            ProduceArrayOptimizedWithType(self.parent, child_klass))


class ProduceArray(Child):
    """
        Child that gets control after receiving array get_marker.
        Depending upon next get_marker, the processing will go:
        - type get_marker => will read optimized with type and count array,
        - count get_marker => will read optimized with count array,
        - anything else => will read unoptimized array.

        Especially end array get_marker will immedietaly produce an empty array.
    """

    def on_got_control(self):

        self.log.debug("want next get_marker")

        child = GetMarker(self)
        child.register_markers(STANDARD_MARKERS)
        child.register_marker(36, ProduceArrayType)
        child.register_marker(35, ProduceArrayCount)
        child.register_marker(93, ProduceArrayEnd)

        self.give_control_to(child)

    def on_got_marker(self, child_klass):
        """
            Event incoming upon receiving first get_marker.
        """

        if child_klass == ProduceArrayEnd:
            self.log.debug("empty array")
            self.on_produced([])
            return

        if child_klass == ProduceArrayType:
            self.log.debug("will get type")
            self.give_control_to(ProduceArrayType(self.parent))
            return

        if child_klass == ProduceArrayCount:
            self.log.debug("will get count")
            self.give_control_to(ProduceArrayCount(self.parent))
            return

        self.log.debug("unoptimized array")
        child = ProduceArrayUnoptimized(self.parent)
        self.give_control_to(child)
        child.on_got_marker(child_klass)


class ProduceObjectKey(Child):
    """
        Produces an key (string) and passes it to the object.
    """

    def on_produced(self, child):
        self.log.debug("key: %s", child)
        self.parent.on_got_key(child)


class ProduceObjectValue(Child):
    """
        Reads a get_value of object key and produces a key-get_value pair in object.
    """

    def __init__(self, parent, key):
        super(ProduceObjectValue, self).__init__(parent)
        self.__key = key

    def on_produced(self, child):
        self.log.debug("get_value: %s", child)
        self.parent.on_pair(self.__key, child)


class ProduceObjectBase(Child):
    """
        Base for any object producer.
    """

    def __init__(self, parent):
        super(ProduceObjectBase, self).__init__(parent)
        self._dct = {}

    def on_got_marker(self, child_klass):
        """
            Event from implementing classes with child class of next objects's key.
            This gives control to newly created child instance.
            When the key-get_value pair is produced, it will be added to the object.
        """

        self.log.debug("got key get_marker: %s", child_klass)
        self.give_control_to(
            child_klass(GetStringLength(ProduceObjectKey(self))))

    def on_got_key(self, key):  # pragma: no cover
        """
            Event incoming upon receiving a key.
        """

    def on_pair(self, key, get_value):
        """
            Event incoming upon receiving a key-get_value pair.
        """

        self.log.debug("item %d %s: %s", len(self._dct), key, get_value)
        self._dct[key] = get_value

    def _finish(self):
        self.log.debug("produced object with %d items", len(self._dct))
        self.parent.on_produced(self._dct)


class ProduceObjectUnoptimized(ProduceObjectBase):
    """
        Produces an unoptimized object.
        Unoptimized object has no predefined item type nor length.
        All items until "}" get_marker are added to the array as-they-are.
    """

    def on_got_control(self):
        self.log.debug("want next key")

        child = GetMarker(self)
        child.register_markers(INT_MARKERS)
        child.register_marker(125, ProduceObjectEnd)
        self.give_control_to(child)

    def on_got_marker(self, child_klass):

        if child_klass == ProduceObjectEnd:
            self._finish()
            return

        super(ProduceObjectUnoptimized, self).on_got_marker(child_klass)

    def on_got_key(self, key):
        self.log.debug("want get_value for key: %s", key)
        self.give_control_to(
            ProduceNext(ProduceObjectValue(self, key), STANDARD_MARKERS))

    def on_pair(self, key, get_value):

        super(ProduceObjectUnoptimized, self).on_pair(key, get_value)
        self._request_control()


class ProduceObjectOptimizedWithCount(ProduceObjectBase):
    """
        Produces object with expected length.
        Object will contain next length key-get_value pairs as-they-are.
    """

    def __init__(self, parent, count):
        super(ProduceObjectOptimizedWithCount, self).__init__(parent)
        self.__count = count

    def on_got_control(self):
        if self.__count == 0:
            self._finish()
            return

        self.log.debug("want next key")
        master = GetMarker(self)
        master.register_markers(INT_MARKERS)
        self.give_control_to(master)

    def on_got_key(self, key):
        self.log.debug("want get_value for key: %s", key)
        self.give_control_to(
            ProduceNext(ProduceObjectValue(self, key), STANDARD_MARKERS))

    def on_pair(self, key, get_value):

        super(ProduceObjectOptimizedWithCount, self).on_pair(key, get_value)
        if len(self._dct) == self.__count:
            self._finish()
            return

        self.log.debug("want %d more", self.__count - len(self._dct))
        self._request_control()


class ProduceObjectOptimizedWithTypeCount(ProduceObjectBase):
    """
        Produces object with expected both type and length.
        This means:
        - there will be read length key-get_value pairs,
        - because of knowing a type, values will be read without markers.
    """

    def __init__(self, parent, atype, count):
        super(ProduceObjectOptimizedWithTypeCount, self).__init__(parent)
        self.__type = atype
        self.__count = count

    def on_got_control(self):

        if self.__count == 0:
            self._finish()
            return

        self.__want_next_item()

    def __want_next_item(self):
        self.log.debug("want next key")
        child = GetMarker(self)
        child.register_markers(INT_MARKERS)
        self.give_control_to(child)

    def on_got_key(self, key):
        self.log.debug("want get_value for key: %s", key)
        child = self.__type(ProduceObjectValue(self, key))
        self.give_control_to(child)

    def on_pair(self, key, get_value):

        super(ProduceObjectOptimizedWithTypeCount, self).on_pair(
            key, get_value)
        if len(self._dct) == self.__count:
            self._finish()
            return

        self.log.debug("want %d more", self.__count - len(self._dct))
        self._request_control()


class ProduceObjectCount(Child):
    """
        Reads length of an object and passes it to the object.
        Depending on whether we knew the type before, the control will be passed
        to either optimized-with-type-and-count child, or to optimized-with-count only.
    """

    def __init__(self, parent, atype=None):
        super(ProduceObjectCount, self).__init__(parent)
        self.__type = atype

    def on_got_control(self):
        self.log.debug("want count")
        self.give_control_to(ProduceNext(self, INT_MARKERS))

    def on_produced(self, obj):
        self.log.debug("count will be: %d", obj)

        if self.__type is not None:
            self.give_control_to(
                ProduceObjectOptimizedWithTypeCount(self.parent, self.__type, obj))
        else:
            self.give_control_to(
                ProduceObjectOptimizedWithCount(self.parent, obj))


class ProduceObjectOptimizedWithType(Child):
    """
        Reads the only expected length get_marker and passes control to
        ProduceObjectCount.
    """

    def __init__(self, parent, atype):
        super(ProduceObjectOptimizedWithType, self).__init__(parent)
        self.__type = atype

    def on_got_control(self):

        self.log.debug("produce next")

        child = GetMarker(self)
        child.register_marker(35, ProduceObjectCount)
        self.give_control_to(child)

    # pylint: disable=unused-argument
    def on_got_marker(self, child_klass):
        """
            Event incoming when got type marker.
        """
        self.log.debug("will get count")
        self.give_control_to(ProduceObjectCount(self.parent, self.__type))


class ProduceObjectType(Child):
    """
        Reads a get_marker that will be the object's values' type.
        After reading the get_marker the control will be passed to
        ProduceObjectOptimizedWithType, that expects object length.
    """

    def on_got_control(self):

        self.log.debug("get type get_marker")

        child = GetMarker(self)
        child.register_markers(STANDARD_MARKERS)
        self.give_control_to(child)

    def on_got_marker(self, child_klass):
        """
            @todo
        """

        self.log.debug("type is: %s", child_klass)
        self.give_control_to(
            ProduceObjectOptimizedWithType(self.parent, child_klass))


class ProduceObject(Child):
    """
        Child that gets control after receiving object get_marker.
        Depending upon next get_marker, the processing will go:
        - type get_marker => will read optimized with type and count object,
        - count get_marker => will read optimized with count object,
        - anything else => will read unoptimized object.

        Especially end object get_marker will immedietaly produce an empty object.
    """

    def on_got_control(self):

        self.log.debug("want next get_marker")

        child = GetMarker(self)
        child.register_markers(INT_MARKERS)
        child.register_marker(36, ProduceObjectType)
        child.register_marker(35, ProduceObjectCount)
        child.register_marker(125, ProduceObjectEnd)

        self.give_control_to(child)

    def on_got_marker(self, child_klass):
        """
            Event incoming upon receiving first get_marker.
        """

        if child_klass == ProduceObjectEnd:
            self.log.debug("empty object")
            self.on_produced({})
            return

        if child_klass == ProduceObjectType:
            self.log.debug("will get type")
            self.give_control_to(ProduceObjectType(self.parent))
            return

        if child_klass == ProduceObjectCount:
            self.log.debug("will get count")
            self.give_control_to(ProduceObjectCount(self.parent))
            return

        self.log.debug("unoptimized object")
        child = ProduceObjectUnoptimized(self.parent)
        self.give_control_to(child)
        child.on_got_marker(child_klass)


def produce_uint8(parent):
    """
        Produces uint8.
    """
    return ProduceFirstOfStruct(parent, 'B', 1)


def produce_int8(parent):
    """
        Produces int8.
    """
    return ProduceFirstOfStruct(parent, 'b', 1)


def produce_int16(parent):
    """
        Produces int16.
    """
    return ProduceFirstOfStruct(parent, 'h', 2)


def produce_int32(parent):
    """
        Produces int32.
    """
    return ProduceFirstOfStruct(parent, 'i', 4)


def produce_int64(parent):
    """
        Produces int64.
    """
    return ProduceFirstOfStruct(parent, 'q', 8)


def produce_float32(parent):
    """
        Produces float32.
    """
    return ProduceFirstOfStruct(parent, 'f', 4)


def produce_float64(parent):
    """
        Produces float64.
    """
    return ProduceFirstOfStruct(parent, 'd', 8)

# Known get_marker-childclass bindings that produce integer values.
INT_MARKERS = {
    85: produce_uint8,
    105: produce_int8,
    73: produce_int16,
    108: produce_int32,
    76: produce_int64
}

# Known get_marker-childclass bindings that produce any "standard" get_marker,
# this is non-special ones (like type/count/array/object end).
STANDARD_MARKERS = {
    90: ProduceNull,
    78: ProduceNoop,
    84: ProduceTrue,
    70: ProduceFalse,
    100: produce_float32,
    68: produce_float64,
    67: ProduceChar,
    83: GetStringLength,
    72: GetHPNLength,
    91: ProduceArray,
    123: ProduceObject
}
STANDARD_MARKERS.update(INT_MARKERS)


class ChildGovernor(Child):
    """
        "Governor" of control over children.
        Governor tells which child will be feed with new characters.
    """

    def __init__(self, reader):
        super(ChildGovernor, self).__init__(reader)
        self.controller = None

        self.__should_reset = True

    def __reset(self):
        self.give_control_to(ProduceNext(self, STANDARD_MARKERS))

    def feed(self, pos, character):
        """
            Feeds the child with a single character.
            @param pos: Position of the character in original input array.
            @param character: One-char string.
        """

        if self.__should_reset:
            self.__reset()
            self.__should_reset = False

        self.log.debug("feed %d: %d", pos, character)
        self.controller.feed(pos, character)

    def give_control_to(self, child):
        """
            Gives control to specified child.
        """
        self.log.debug("giving control to: %s", child)
        self.controller = child

        child.on_got_control()

    def on_produced(self, product):
        """
            Event from children upon producing a object.
            This passes the object to the reader.
        """
        self.log.debug("produced: %s", product)
        self.parent.on_produced(product)

        self.__should_reset = True


class Deserializer(object):
    """
        Asynchronous deserializer for UBJson streams.
    """

    def __init__(self, listener):
        """
            @param listener: Method that receives objects:
                def listener(obj): pass
        """

        self.__listener = listener
        self.log = getLogger('reader')

        self.governor = ChildGovernor(self)

    def receive(self, data):
        """
            Use this to pass bytearray data to the reader.
        """

        self.log.debug("receive %d: %s", len(data), data)
        pos = 0
        for character in data:

            self.log.debug("consume %d %d", pos, character)
            self.governor.feed(pos, character)
            pos = pos + 1

    def on_produced(self, obj):
        """
            Event incoming from child governor about received objects.
            This will pass the objects to the listener.
        """
        self.log.debug("return to listener: %s", obj)
        self.__listener(obj)
