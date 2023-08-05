"""This module implements encoding and decoding of bittorrent's bencoding."""
import io

class DecodeError(Exception):
    """Describe a decoding error"""
    pass

class EncodeError(Exception):
    """Describe an encoding error"""
    pass

def _consume(data, charset, many=False, optional=False):
    found = 0
    while found < len(data):
        if data[found] in charset:
            found += 1
        else:
            break
        if not many:
            break
    if found == 0 and not optional:
        raise DecodeError("Parse error at %s" % (data,))
    return (data[:found], data[found:])

def _decode_int(data):
    _, data = _consume(data, b'i')
    minus, data = _consume(data, b'-', optional=True)
    numbers, data = _consume(data, b'0123456789', many=True)
    _, data = _consume(data, b'e')
    return (int(minus + numbers), data)

def _decode_str(data):
    count, data = _consume(data, b'0123456789', many=True)
    count = int(count)
    _, data = _consume(data, b':')
    if len(data) < count:
        raise DecodeError('Parse error at %s, not enough data to parse string' %
                         (data,))
    return (data[:count], data[count:])

def _decode_list(data):
    _, data = _consume(data, b'l')
    lst = list()
    while True:
        val, data = _decode(data, end=True)
        if val == None:
            break
        lst.append(val)
    return (lst, data)

def _decode_dict(data):
    _, data = _consume(data, b'd')
    dct = dict()
    while True:
        key, data = _decode(data, end=True)
        if key == None:
            break
        val, data = _decode(data)
        dct[key] = val
    return (dct, data)

def _decode(data, end=False):
    if len(data) == 0:
        raise DecodeError('No data to decode')
    if data[0] in b'i':
        return _decode_int(data)
    elif data[0] in b'0123456789':
        return _decode_str(data)
    elif data[0] in b'l':
        return _decode_list(data)
    elif data[0] in b'd':
        return _decode_dict(data)
    elif end and data[0] in b'e':
        return None, data[1:]
    else:
        raise DecodeError('No data to decode')

def decode(data):
    """Decode a bencoded bytes object
        
    :param bytes data: A valid bencoded representation of some object.
    :returns: The decoded object.
    :rtype: bytes, int, dict, list
    :raises: DecodeError
    """
    value, data = _decode(data)
    if len(data) != 0:
        raise DecodeError('Trailing data after decoding')
    return value

def _encode_int(buf, val):
    buf.write(b'i')
    buf.write(str(val).encode())
    buf.write(b'e')

def _encode_bytes(buf, val):
    buf.write(str(len(val)).encode())
    buf.write(b':')
    buf.write(val)

def _encode_list(buf, val):
    buf.write(b'l')
    for item in val:
        _encode(buf, item)
    buf.write(b'e')

def _encode_dict(buf, rawval):
    # Dicts are annoying, because they need to be sorted and can't contain the
    # same key twice. This creates two problems:
    # 1. a key 'hello' and b'hello' would encode to the same key (not allowed)
    # 2. a key 'hello' and b'hello' can't be compared (by the default sorted())
    # To solve this problem we convert the entire dictionary to something that
    # only has bytes() keys and bail out if we can't do that unambiguously.
    val = {}
    for key, value in rawval.items():
        bkey = key
        if type(bkey) == str:
            bkey = bkey.encode()
        if type(bkey) != bytes:
            raise EncodeError("Can't encode dict keys of type %s" % type(key))
        if bkey in val:
            raise EncodeError('Ambiguous key in dictionary, multiple keys '
                              'encode to %s', bkey)
        val[bkey] = value

    buf.write(b'd')
    for key in sorted(val.keys()):
        _encode_bytes(buf, key)
        _encode(buf, val[key])
    buf.write(b'e')

def _encode(buf, val):
    if isinstance(val, str):
        _encode_bytes(buf, val.encode())
    elif isinstance(val, bytes):
        _encode_bytes(buf, val)
    elif isinstance(val, list):
        _encode_list(buf, val)
    elif isinstance(val, dict):
        _encode_dict(buf, val)
    elif isinstance(val, int):
        _encode_int(buf, val)
    else:
        raise EncodeError("Can't encode object of type %s" % type(val))

def encode(val):
    """Encode a value as a bytearray
    
    :param val: The value that is to be encoded. Can be of type ``dict``,
        ``list``, ``int``, ``string``, ``bytes``. Dicts and lists can only
        contain those types.  Note that ``dict`` objects may not contain keys
        with a type other than ``bytes`` or ``string`` and that all keys must
        have a unique ``bytes`` encoding.  The following is not valid::

                {'hello': 1, b'hello': 2}

        because::

                'hello'.encode() == b'hello'

        Besides the aforementioned types, any type that derives from them is
        also supported with the expectation that they behave in a sane way.
        If you supply derived types that don't behave as we expect these
        types to behave the results are undefined.

    :returns: The bencoded representation of ``val``
    :rtype: bytes 
    :raises: EncodeError
    """
    buf = io.BytesIO()
    _encode(buf, val)
    return buf.getvalue()
