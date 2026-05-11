from meep.rtmidi import open_input

for msg in open_input('mpk'):
    print(msg)
