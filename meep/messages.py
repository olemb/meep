from numbers import Integral
from dataclasses import dataclass


_max_values = {
    ('PitchBend', 'value'): 16383,
    ('SongPosition', 'beats'): 16383,
    ('TimeCode', 'frame_type'): 7,
    ('TimeCode', 'frame_value'): 15,
}

class MidiMsg:
    @property
    def type(self):
        return self.__class__.__name__

    def is_cc(self, number=None):
        if not isinstance(self, ControlChange):
            return False
        elif number is None:
            return True
        else:
            return self.number == number

    def __post_init__(self):
        class_name = self.__class__.__name__
        # Type and value checks.
        for name, value in vars(self).items():
            if not isinstance(value, Integral):
                raise TypeError(f'{name} must be integer')
            elif name == 'ch':
                if not 1 <= value <= 16:
                    raise ValueError('ch must be in range 1..16')
            else:
                max_value = _max_values.get((class_name, name), 127)
                if not 0 <= value <= max_value:
                    raise ValueError(f'{name} must be in range 0..{max_value}')


@dataclass(frozen=True, eq=True)
class NoteOff(MidiMsg):
    note: Integral = 0
    velocity: Integral = 64
    ch: Integral = 1


@dataclass(frozen=True, eq=True)
class NoteOn(MidiMsg):
    note: Integral = 0
    velocity: Integral = 64
    ch: Integral = 1


@dataclass(frozen=True, eq=True)
class PolyPressure(MidiMsg):
    note: Integral = 0
    value: Integral = 0
    ch: Integral = 1


@dataclass(frozen=True, eq=True)
class ControlChange(MidiMsg):
    number: Integral = 0
    value: Integral = 0
    ch: Integral = 1


@dataclass(frozen=True, eq=True)
class ProgramChange(MidiMsg):
    number: Integral = 0
    ch: Integral = 1


@dataclass(frozen=True, eq=True)
class ChannelPressure(MidiMsg):
    value: Integral = 0
    ch: Integral = 1


@dataclass(frozen=True, eq=True)
class PitchBend(MidiMsg):
    value: Integral = 8192
    ch: Integral = 1
    mid = 8192
    max = 16383


@dataclass(frozen=True, eq=True)
class SystemExclusive(MidiMsg):
    data: bytes = b''

    def __post_init__(self):
        vars(self)['data'] = bytes(self.data)
        for byte in self.data:
            if not 0 <= byte <= 127:
                raise ValueError('syx data byte must be in range 0..127')


@dataclass(frozen=True, eq=True)
class TimeCode(MidiMsg):
    frame_type: Integral = 0
    frame_value: Integral = 0


@dataclass(frozen=True, eq=True)
class SongPosition(MidiMsg):
    beats: Integral = 0
    max = 16383


@dataclass(frozen=True, eq=True)
class SongSelect(MidiMsg):
    number: Integral = 0


@dataclass(frozen=True, eq=True)
class TuneRequest(MidiMsg):


@dataclass(frozen=True, eq=True)
class MidiClock(MidiMsg):


@dataclass(frozen=True, eq=True)
class Start(MidiMsg):


@dataclass(frozen=True, eq=True)
class Continue(MidiMsg):


@dataclass(frozen=True, eq=True)
class Stop(MidiMsg):


@dataclass(frozen=True, eq=True)
class ActiveSensing(MidiMsg):


@dataclass(frozen=True, eq=True)
class Reset(MidiMsg):


classes = [
    NoteOff,
    NoteOn,
    PolyPressure,
    ControlChange,
    ProgramChange,
    ChannelPressure,
    PitchBend,
    SystemExclusive,
    TimeCode,
    SongPosition,
    SongSelect,
    TuneRequest,
    MidiClock,
    Start,
    Continue,
    Stop,
    ActiveSensing,
    Reset,
]


def get_class(name):
    # TODO: add a lookup table.
    for cls in classes:
        if cls.__name__ == name:
            return cls
    else:
        raise ValueError(f'unknown MIDI message {name!r}')


__all__ = [_.__name__ for _ in classes]
