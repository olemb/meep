import time
from meep.rtmidi import open_output
from meep.messages import NoteOn, NoteOff

out = open_output('GM')

for i in range(10):
    note = i + 2
    out.send(NoteOn())
    time.sleep(0.3)
    out.send(NoteOff())
    time.sleep(0.1)
