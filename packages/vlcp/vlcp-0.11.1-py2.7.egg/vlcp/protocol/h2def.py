'''
Created on 2016/1/18

:author: hubo
'''
from namedstruct import *
from namedstruct.namedstruct import PrimitiveParser, BadFormatError
import struct

# Why on earth would someone use a 24-bit integer...

class Uint24PrimitiveParser(object):
    def __init__(self, endian = '>'):
        self.struct = struct.Struct(endian + 'I')
        self.emptydata = b'\x00\x00\x00'
        self.empty = 0
    def parse(self, buffer, inlineparent = None):
        if len(buffer) < 3:
            return None
        try:
            if self._le:
                return (self.struct.unpack(buffer[:3] + b'\x00')[0], self.struct.size)
            else:
                return (b'\x00' + self.struct.unpack(buffer[:3])[0], self.struct.size)                
            return (self.struct.unpack(buffer[:3])[0], self.struct.size)
        except struct.error as exc:
            raise BadFormatError(exc)
    def new(self, inlineparent = None):
        return self.empty
    def create(self, data, inlineparent = None):
        try:
            if self._le:
                return self.struct.unpack(data + b'\x00')[0]
            else:
                return self.struct.unpack(b'\x00' + data)[0]
        except struct.error as exc:
            raise BadFormatError(exc)
    def sizeof(self, prim):
        return 3
    def paddingsize(self, prim):
        return 3
    def tobytes(self, prim):
        if self._le:
            return self.struct.pack(prim)[:3]
        else:
            return self.struct.pack(prim)[1:]


class uint24_prim(prim):
    def __init__(self, readablename = 'uint24', endian = '>'):
        prim.__init__(self, '3s', readablename, endian, True)
    def _compile(self):
        return Uint24PrimitiveParser(self._endian)

uint24 = uint24_prim()

frame_type = enum('frame_type', globals(), uint8,
                  DATA = 0x0,
                  HEADERS = 0x1,
                  PRIORITY = 0x2,
                  RST_STREAM = 0x3,
                  SETTINGS = 0x4,
                  PUSH_PROMISE = 0x5,
                  PING = 0x6,
                  GOAWAY = 0x7,
                  WINDOW_UPDATE = 0x8,
                  CONTINUATION = 0x9
                  )

def _frame_packsize(f):
    f.length = f._realsize() - 9

common_flags = enum('common_flags', globals(), uint8, True,
                    END_STREAM = 0x1,
                    PADDED = 0x8
                    )

frame = nstruct((uint24, 'length'),
                (frame_type, 'type'),
                (uint8, 'flags'),
                (bitfield(uint32,
                          (1,'R'),
                          (31, 'stream_id')),),
                size = lambda x: x.length + 9,
                padding = 1,
                name = 'frame',
                prepack = _frame_packsize,
                classifier = lambda x: x.type
                )

END_STREAM = 0x1

frame_data_flags = common_flags.extend(None, 'frame_data_flags')

def _frame_data_padding_prepack(x):
    if hasattr(x, 'padding'):
        x.padlength = len(x.padding)
        x.flags = x.flags | PADDED
    else:
        if hasattr(x, 'padlength'):
            del x.padlength
        x.flags = x.flags & ~PADDED

_frame_data_data = nstruct((raw, 'data'),
                           size = lambda x: x.length - getattr(x, 'padlength', 0),
                           name = '_frame_data_data',
                           padding = 1,
                           lastextra = True
                           )

_frame_data_padding = nstruct(optional(raw, 'padding', lambda x: x.flags & PADDED),
                              size = lambda x: getattr(x, 'padlength', 0),
                              name = '_frame_data_padding',
                              padding = 1,
                              lastextra = True,
                              prepack = _frame_data_padding_prepack
                              )

frame_data = nstruct((optional(uint8, 'padlength', lambda x: x.flags & PADDED),),
                     (_frame_data_data,),
                     (_frame_data_padding,),
                     base = frame,
                     init = packvalue(DATA, 'type'),
                     criteria = lambda x: x.type == DATA,
                     classifyby = (DATA,),
                     lastextra = False,
                     name = 'frame_data',
                     extend = {'flags': frame_data_flags}
                     )

_priority_stream = bitfield(uint32,
                            (1, 'E'),
                            (31, 'stream_dependency'),
                            name = '_priority_stream'
                            )

frame_headers = nstruct((optional(uint8, 'padlength', lambda x: x.flags & PADDED),),
                        (optional(_priority_stream, ''))
                        (_priority_stream,),
                        
                        )
