from meep.rtmidi import open_input

for msg in open_input('MPK'):
    if msg.is_cc(1):
        print('Filter knob:', msg.value)
    elif msg.is_cc():
        print('Other knob:', msg)
    else:
        print('Other message', msg)
