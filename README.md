Meep - MIDI Messages for Python

Meep (working title) is an attempt to write a new MIDI library using
what I've learned from developing Mido. I've written it entirely for
my own use. It is not not compatible with Mido.  and is very minimal
in functionality. There is no support for MIDI files, only messages
(the key feature) and very simple ports.

I will add features as they are needed.

Sending and receiving messages:

```python
import time
import meep
from meep import NoteOn

msg1 = NoteOn(60, velocity=22, ch=1))
msg2 = NoteOff(60, ch=1))

# There's no default backend for now.
# You don't need to give the full name of the port.
out = meep.rtmidi.open_output('minilogue')

out.send(msg1)
out.send(msg2)

# Let's use the other backend here (requires ReceiveMIDI).
inp = meep.sendmidi.open_input('microkey')
for msg in inp:
    out.send(msg)
```

All MIDI 1.0 message types are suppported:

```Python
NoteOff(note=0, velocity=64, ch=1)
NoteOn(note=0, velocity=64, ch=1)
PolyPressure(note=0, value=0, ch=1)
ControlChange(number=0, value=0, ch=1)
ProgramChange(number=0, ch=1)
ChannelPressure(value=0, ch=1)
PitchBend(value=8192, ch=1)
SystemExclusive(data=b'')
TimeCode(frame_type=0, frame_value=0)
SongPosition(beats=0)
SongSelect(number=0)
TuneRequest()
MidiClock()
Start()
Continue()
Stop()
ActiveSensing()
Reset()

# Created with:
import meep
for cls in meep.messages.classes:
    # Create a new object.
    print(repr(cls()))
```


Differences from Mido:

* Messages are implemented as one @dataclass per messsage type. (See
  `meep/messages.py`.) This is much simpler and cleaner than doing it
  all in one `Message` class.

* Messages are always immutable (like frozen in Mido terms). The always
  should have been. It makes no sense to change the value of a message.
  It's always better to make a copy.

* Messages have very few methods. Converting to and from the standard
  binary (tuple of ints) is done with `meep.from_bytes()` and
  `meep.as_bytes()`.

* There is very little inheritance and most of the code is purely
  functional.

* Channels are numbered 1-16.

* There are no MIDI files or sysex files.

* Messages don't have a `time` attribute. While it is useful, it
  doesn't really belong there. (I'm torn on the `time` attribute. I
  think it's quite useful in Mido, though it can get a bit confusing.)

* Names of messages and parameters are taked from the SendMIDI and
  ReceiveMIDI tools. (This may change in the future.)

* Ports can be opened without giving the full
  name. For example `open_input('korg')` will open
  'KORG microkey air 0:0'. I would like to bring this feature into Mido.

* Ports are very limited. I want to see how I actually use port before
  I commit to any more API details.

* The channel parameter is last to keep it out of the way. This makes
  it possible to write `NoteOn(12)` and get the expected note 12 instead
  of channel 12.

Ole Martin Bjørndalen
