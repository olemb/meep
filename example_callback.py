import meep
from meep.rtmidi import open_input

def callback(msg, deltatime):
    print(msg, deltatime)

inp = open_input('microkey')
inp.set_callback(callback)

input('enter to quit> ')
