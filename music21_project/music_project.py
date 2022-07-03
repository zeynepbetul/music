import pandas as pd
import music21 as m21
import numpy as np

path = '/Users/zeynepbetulkaya/PycharmProjects/music/music21_project/Stephen Sondheim - A Little Night Music.mxl'
s = m21.converter.parse(path) # s -> <music21.stream.Score 0x10556f160>

def check_single(name):
    if len(name) == 1:
        name = name + "0"
    return name

def encode(note):
    if (note == 'C0'):
        encoded = 0
    if (note == 'Db'):
        encoded = 1
    if (note == 'D0'):
        encoded = 2
    if (note == 'Eb'):
        encoded = 3
    if(note == 'E0'):
        encoded = 4
    if(note == 'F0'):
        encoded = 5
    if (note == 'Gb'):
        encoded = 6
    if (note == 'G0'):
        encoded = 7
    if (note == 'Ab'):
        encoded = 8
    if (note == 'A0'):
        encoded = 9
    if (note == 'Bb'):
        encoded = 10
    if (note == 'B0'):
        encoded = 11
    return encoded

def decode(encoded_number, name, add_new):
    encoded_number = encoded_number + add_new
    if (encoded_number == 0):
        name = 'C0'
    if (encoded_number == 1):
        name = 'Db'
    if (encoded_number == 2):
        name = 'D0'
    if (encoded_number == 3):
        name = 'Eb'
    if(encoded_number == 4):
        name = 'E0'
    if(encoded_number == 5):
        name = 'F0'
    if (encoded_number == 6):
        name = 'Gb'
    if (encoded_number == 7):
        name = 'G0'
    if (encoded_number == 8):
        name = 'Ab'
    if (encoded_number == 9):
        name = 'A0'
    if (encoded_number == 10):
        name = 'Bb'
    if (encoded_number == 11):
        name = 'B0'
    return encoded_number, name

#s.show()
time_sign = 0
measure = 0
key_fifths = 0
key_tonic = ''
key_mode = 0
chord_root = ''
chord_type = ''
note_root = ''
note_octave = 0
note_duration = 0.0
key_tonic = ''
chord_encoded = ''
note_encoded = ''
new_array = []
combined_array = np.zeros((1, 13))

for el in s.recurse():
    if el.classes[0] == 'Note':
        note_root = el.name
        note_root = check_single(note_root)
        note_root = note_root.replace('-', 'b')
        note_encoded = encode(note_root)
        note_octave = el.octave
        note_duration = el.duration.quarterLength * 4.0  # DurationTuple(type='quarter', dots=0, quarterLength=1.0)
        measure = el.activeSite.measureNumber
        new_array = [time_sign, measure, key_fifths, key_tonic, key_mode, chord_root,
                     chord_type, note_root, note_octave, note_duration, key_encoded, chord_encoded, note_encoded]
        combined_array = np.vstack((combined_array, new_array))
    elif el.classes[0] == 'Rest':
        note_root = 'rest'
        note_octave = 0
        note_duration = el.duration.quarterLength * 4.0
        measure = el.activeSite.measureNumber
        new_array = [time_sign, measure, key_fifths, key_tonic, key_mode, chord_root,
                     chord_type, note_root, note_octave, note_duration, key_encoded, chord_encoded, note_encoded]
        combined_array = np.vstack((combined_array, new_array))
    elif el.classes[0] == 'ChordSymbol':
        chord_root = el.root().name
        chord_root = check_single(chord_root)
        chord_root = chord_root.replace('-', 'b')
        chord_encoded = encode(chord_root)
        chord_type = el.chordKind
        measure = el.activeSite.measureNumber
    elif el.classes[0] == 'TimeSignature':
        time_sign = el.ratioString
        measure = el.activeSite.measureNumber
        #print('time: ', time_sign)
    elif el.classes[0] == 'Key':
        key_fifths = el.sharps
        key_tonic = el.tonic
        key_tonic = check_single(key_tonic.name)
        key_tonic = key_tonic.replace('-', 'b')
        key_encoded = encode(key_tonic)
        key_mode = el.mode
        #print('keys:', key_fifths, key_mode)
    print(el.offset, el, el.activeSite, el.classes[0])

combined_array = np.delete(combined_array, 0, axis=0)
print(combined_array)
df = pd.DataFrame(combined_array, columns=['time', 'measure', 'key fifths', 'key tonic',
                                           'key mode', 'chord root', 'chord type', 'note root',
                                           'note octave', 'note duration', 'key encoded', 'chord encoded',
                                           'note encoded'])
df.to_excel('pandas_t_excel.xlsx', sheet_name='new_shet_name', index=False)
