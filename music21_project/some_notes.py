from music21 import *

f = note.Note("F5") # >>f; <music21.note.Note F>
# >> f.name; 'F' >>f.octave; 5
cs = harmony.ChordSymbol('Am')
cs = cs.transpose(1)
print(cs)
print(cs.root().name)
k = key.Key()
k.mode
k.sharps
#f.show()

'''pitch'''
f.pitch # returns another object # <music21.pitch.Pitch F5>
f.pitch.frequency # sub attribute of pitch gives = 698.456462866008
f.pitch.pitchClassString # '5'
# f.octave is int but f.pitch.pitchClassString is string.
#print(f.pitch.frequency)

'''For a Note to occupy musical space, it has to last a certain amount of time. We call that time the Note’s Duration.
A Duration object can represent just about any time span. 
Duration objects are best used when they’re attached to something else, like a Note or a Rest. 
duration types: “whole”, “half”, “quarter”, “eighth”, “16th”, “32nd”, “64th” '''

dottedQuarter = duration.Duration(1.5)
# whole note (quarterLength = 4), half note (quarterlength = 2), quarter note-> 1.5 verdiğimiz için, yoksa 1 dimi? (dörtlük nota çeyreği kadar uzun yani), eight note...
halfDuration = duration.Duration('half')
#halfDuration.quarterLength()  # 2.0 verir.
#dottedQuarter.type() # quarter
#halfDuration.type()  # half

'''The attributes of dots ? , type (tama göre isimleri), and quarterLength (süreleri 4, 2, 1...) are actually special attributes called “properties”'''
'''The Stream object and its subclasses (Score, Part, Measure) are the fundamental containers for music21 objects 
such as Note, Chord, Clef, TimeSignature objects.'''

'''Objects stored in a Stream are generally spaced in time; each stored object has an 
offset usually representing how many quarter notes it lies from the beginning of the Stream. 
For instance in a 4/4 measure of two half notes, the first note will be at offset 0.0, and the second at offset 2.0.
'''