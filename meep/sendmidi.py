"""
Ports and utilities for Geert Bevin's SendMIDI and ReceiveMIDI programs.
"""
import os
import re
import subprocess
from .messages import get_class, SystemExclusive


def dashname(camelname):
    """Convert CamelName to dash-name."""
    return re.sub(r'([a-z])([A-Z])', r'\1-\2', camelname).lower()


def camelname(dashname):
    """Convert dash-name to CamelName."""
    return ''.join(part.capitalize() for part in dashname.split('-'))


templates = {
    'NoteOff': 'channel {ch} note-off {note} {velocity}',
    'NoteOn': 'channel {ch} note-on {note} {velocity}',
    'PolyPressure': 'channel {ch} poly-pressure {note} {value}',
    'ControlChange': 'channel {ch} control-change {number} {value}',
    'ProgramChange': 'channel {ch} program-change {number}',
    'ChannelPressure': 'channel {ch} channel-pressure {value}',
    'PitchBend': 'channel {ch} pitch-bend {value}',
    'TimeCode': 'time-code {frame_type} {frame_value}',
    'SongPosition': 'song-position {beats}',
    'SongSelect': 'song-select {number}',
    'TuneRequest': 'tune-request',
    'MidiClock': 'midi-clock',
    'Start': 'start',
    'Continue': 'continue',
    'Stop': 'stop',
    'ActiveSensing': 'active-sensing',
    'Reset': 'reset',
}

_dashnames = [dashname(name) for name in templates]


def _from_syx_line(line):
    # Example: "system-exclusive hex 01 02 03 dec"

    data = [byte for byte in line.split() if len(byte) == 2]
    return SystemExclusive(bytes(int(byte, 16) for byte in data))


def from_line(line):
    if 'system-exclusive' in line:
        return _from_syx_line(line)
    else:
        for name in _dashnames:
            if name in line:
                cls = get_class(camelname(name))
                args = [int(arg) for arg in re.findall('(\d+)', line)]
                if 'channel' in line:
                    # Move channel to last position.
                    args = args[1:] + [args[0]]
                return cls(*args)
        else:
            raise ValueError(f'unknown message: {line.strip()!r}')


def as_line(msg):
    if msg.type == 'SystemExclusive':
        data = ' '.join(f'{byte:02x}' for byte in msg.data)
        return f'system-exclusive hex {data} dec'
    else:
        return templates[msg.__class__.__name__].format(**vars(msg))


def list_inputs():
    return [n.rstrip() for n in os.popen('receivemidi list').readlines()]


def list_outputs():
    return [n.rstrip() for n in os.popen('sendmidi list').readlines()]


def open_input(name):
    return Input(name)


def open_output(name):
    return Output(name)


def create_input(name):
    return Input(name, create=True)


def create_output(name):
    return Output(name, create=True)


class Input:
    def __init__(self, name, create=False):
        if create:
            devtype = 'virt'
        else:
            devtype = 'dev'

        args = ['receivemidi', devtype, name, 'nn']
        self._proc = subprocess.Popen(args,
                                      stdout=subprocess.PIPE)

    def __iter__(self):
        while True:
            line = self._proc.stdout.readline()
            yield from_line(line.decode('ascii'))


class Output:
    def __init__(self, name, create=False):
        if create:
            devtype = 'virt'
        else:
            devtype = 'dev'

        args = ['sendmidi', devtype, name, '--']
        self._proc = subprocess.Popen(args,
                                      stdin=subprocess.PIPE)

    def send(self, msg):
        line = as_line(msg) + '\n'
        self._proc.stdin.write(line.encode('ascii'))
        self._proc.stdin.flush()


__all__ = ['list_inputs', 'list_outputs',
           'open_input', 'open_output',
           'create_input', 'create_output']
