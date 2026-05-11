from .messages import *


encoders = {
    'NoteOff': lambda msg: (0x80|msg.ch-1, msg.note, msg.velocity),
    'NoteOn': lambda msg: (0x90|msg.ch-1, msg.note, msg.velocity),
    'PolyPressure': lambda msg: (0xa0|msg.ch-1, msg.note, msg.value),
    'ControlChange': lambda msg: (0xb0|msg.ch-1, msg.number, msg.value),
    'ProgramChange': lambda msg: (0xc0|msg.ch-1, msg.number),
    'ChannelPressure': lambda msg: (0xd0|msg.ch-1, msg.value),
    'PitchBend' :lambda msg: (0xe0|msg.ch-1, msg.value & 0x7f, msg.value >> 7),
    'SystemExclusive': lambda msg: (0xf0,) + tuple(msg.data) + (0xf7,),
    'TimeCode': lambda msg: (0xf1, msg.frame_type << 4 | msg.frame_value),
    'SongPosition': lambda msg: (0xf2, msg.beats & 0x7f, msg.beats >> 7),
    'SongSelect': lambda msg: (0xf3, msg.number),
    'TuneRequest': lambda msg: (0xf6,),
    'MidiClock': lambda msg: (0xf8,),
    'Start': lambda msg: (0xfa,),
    'Continue': lambda msg: (0xfb,),
    'Stop': lambda msg: (0xfc,),
    'ActiveSensing': lambda msg: (0xfe,),
    'Reset': lambda msg: (0xff,),
}


def as_bytes(msg):
    return encoders[msg.__class__.__name__](msg)


decoders = {
    0x80: lambda bytes: NoteOff(bytes[1], bytes[2], (bytes[0] & 15) + 1),
    0x90: lambda bytes: NoteOn(bytes[1], bytes[2], (bytes[0] & 15) + 1),
    0xa0: lambda bytes: PolyPressure(bytes[1], bytes[2], (bytes[0] & 15) + 1),
    0xb0: lambda bytes: ControlChange(bytes[1], bytes[2], (bytes[0] & 15) + 1),
    0xc0: lambda bytes: ProgramChange(bytes[1], (bytes[0] & 15) + 1),
    0xd0: lambda bytes: ChannelPressure(bytes[1], (bytes[0] & 15) + 1),
    0xe0: lambda bytes: PitchBend((bytes[1] | bytes[2] << 7), (bytes[0] & 15) + 1),
    0xf0: lambda bytes: SystemExclusive(bytes(bytes[1:-1])),
    0xf1: lambda bytes: TimeCode(bytes[1] >> 4, bytes[1] & 0xf),
    0xf2: lambda bytes: SongPosition((bytes[1] | bytes[2] << 7)),
    0xf3: lambda bytes: SongSelect(bytes[1]),
    0xf6: lambda bytes: TuneRequest(),
    0xf8: lambda bytes: MidiClock(),
    0xfa: lambda bytes: Start(),
    0xfb: lambda bytes: Continue(),
    0xfc: lambda bytes: Stop(),
    0xfe: lambda bytes: ActiveSensing(),
    0xff: lambda bytes: Reset(),
}


def from_bytes(midi_bytes):
    status = midi_bytes[0]
    if status < 0xf0:
        # Strip away channel.
        status &= 0xf0

    return decoders[status](midi_bytes)
