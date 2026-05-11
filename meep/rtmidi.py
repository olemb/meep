"""
pip install python-rtmidi
"""
import time
import rtmidi
from .bytes import as_bytes, from_bytes


def _find_port(rt, name):
    names = rt.get_ports()
    try:
        return names.index(name)
    except ValueError:
        pass

    for index, fullname in enumerate(names):
        if name.lower() in fullname.lower():
            return index
    else:
        raise ValueError(f'unknown device {name!r}')


def list_inputs():
    return rtmidi.MidiIn().get_ports()


def list_outputs():
    return rtmidi.MidiOut().get_ports()


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
        self.rt = rtmidi.MidiIn()
        if create:
            self.rt.open_virtual_port(name)
        else:
            self.rt.open_port(_find_port(self.rt, name))

    def __iter__(self):
        while True:
            msg = self.rt.get_message()
            if msg is None:
                time.sleep(0.001)
            else:
                yield from_bytes(msg[0])


class Output:
    def __init__(self, name, create=False):
        self.rt = rtmidi.MidiOut()
        if create:
            self.rt.open_virtual_port(name)
        else:
            self.rt.open_port(_find_port(self.rt, name))

    def send(self, msg):
        self.rt.send_message(as_bytes(msg))


__all__ = ['list_inputs', 'list_outputs',
           'open_input', 'open_output',
           'create_input', 'create_output']
