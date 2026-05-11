"""
Basically a clone of http://typedrummer.com/
"""
import os
import sys
import time
import string
import readline
import threading
from meep.rtmidi import open_output
from meep import NoteOn, NoteOff


#drum_notes = {
#    'a': 36,
#    'b': 47,
#    'c': 50,
#}

drum_notes = {}

for note, char in enumerate(string.ascii_lowercase, start=35):
    drum_notes[char] = note


class Drummer:
    def __init__(self, port, pattern=''):
        self.port = port
        self.pattern = pattern
        self.sleep_time = 0.20

        self._thread = threading.Thread(target=self._mainloop)
        self._thread.daemon = True
        self._thread.start()

    def _mainloop(self):
        while True:
            for char in self.pattern:
                note = drum_notes.get(char)
                if note is not None:
                    self.port.send(NoteOn(note, ch=10))
                    self.port.send(NoteOff(note, ch=10))

                time.sleep(self.sleep_time)


gmsynth = open_output('GM')

drummer = Drummer(gmsynth, pattern='b ')
while True:
    pattern = input().rstrip('\n')
    drummer.pattern = pattern
