from meep.rtmidi import open_input, open_output
from meep import ProgramChange

gmsynth = open_output('GM')

for msg in open_input('MPK'):
    if msg.is_cc(1):
        # Select sounds with knob 1.
        gmsynth.send(ProgramChange(msg.value))
    elif msg.is_cc():
        pass
    else:
        gmsynth.send(msg)
