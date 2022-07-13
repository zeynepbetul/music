import pandas as pd
import music21 as m21
import numpy as np
import os


def check_single(name):
    if len(name) == 1:
        name = name + "0"
    return name


def check_chord_type(chord_string, code):
    isMinor = chord_string.find('minor')
    isDiminished = chord_string.find('diminished')
    if (isMinor != -1 or isDiminished != -1):
        code = code + 12
    return code


def encode(note):
    if (note == 'C0' or note == 'B#'):
        encoded = 0
    elif (note == 'Db' or note == 'C#'):
        encoded = 1
    elif (note == 'D0'):
        encoded = 2
    elif (note == 'Eb' or note == 'D#'):
        encoded = 3
    elif (note == 'E0' or note == 'Fb'):
        encoded = 4
    elif (note == 'F0' or note == 'E#'):
        encoded = 5
    elif (note == 'Gb' or note == 'F#'):
        encoded = 6
    elif (note == 'G0'):
        encoded = 7
    elif (note == 'Ab' or note == 'G#'):
        encoded = 8
    elif (note == 'A0'):
        encoded = 9
    elif (note == 'Bb' or note == 'A#'):
        encoded = 10
    elif (note == 'B0' or note == 'Cb'):
        encoded = 11
    else:
        encoded = 111
    return encoded

path_of_the_directory= '/Users/zeynepbetulkaya/PycharmProjects/music/music21_project/Wikifonia'
for filename in os.listdir(path_of_the_directory):
    f = False
    path = os.path.join(path_of_the_directory, filename)
    ex = os.path.splitext(path)[1]
    if ex != '.mxl':
        continue
    try:
        s = m21.converter.parse(path)  # s -> <music21.stream.Score 0x10556f160>
    except Exception as e:
        print(e)
        continue

    # s.show('text')
    # s.show()
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
    chord_encoded = ''
    note_encoded = ''

    new_array = []
    combined_array = np.zeros((1, 13))
    new_chord_array = []
    chord_array = np.zeros((1, 3))

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
        elif el.classes[0] == 'Measure':
            if chord_array[0, 0] == 0:
                chord_array = np.delete(chord_array, 0, axis=0)
            chord_root = ''
            chord_type = ''
            chord_encoded = ''
            new_chord_array = [chord_root, chord_type, chord_encoded]  # have only one chord per measure
            chord_array = np.vstack((chord_array, new_chord_array))
        elif el.classes[0] == 'Rest':
            note_root = 'rest'
            note_octave = 0
            note_duration = el.duration.quarterLength * 4.0
            measure = el.activeSite.measureNumber
            note_encoded = 12
            new_array = [time_sign, measure, key_fifths, key_tonic, key_mode, chord_root,
                         chord_type, note_root, note_octave, note_duration, key_encoded, chord_encoded, note_encoded]
            combined_array = np.vstack((combined_array, new_array))
        elif el.classes[0] == 'ChordSymbol':
            if chord_root == '':
                chord_root = el.root().name
                chord_root = check_single(chord_root)
                chord_root = chord_root.replace('-', 'b')
                chord_encoded = encode(chord_root)
                chord_type = el.chordKind
                chord_encoded = check_chord_type(chord_type, chord_encoded)
                chord_array[el.activeSite.measureNumber - 1, 0] = chord_root
                chord_array[el.activeSite.measureNumber - 1, 1] = chord_type
                chord_array[el.activeSite.measureNumber - 1, 2] = chord_encoded
        elif el.classes[0] == 'TimeSignature':
            time_sign = el.ratioString
        elif el.classes[0] == 'Key':
            key_mode = el.mode
            if key_mode != 'minor':
                f = True
                break
            key_fifths = el.sharps
            key_tonic = el.tonic
            key_tonic = check_single(key_tonic.name)
            key_tonic = key_tonic.replace('-', 'b')
            key_encoded = encode(key_tonic)

    if f:
        continue

    combined_array = np.delete(combined_array, 0, axis=0)
    for iteration, item in enumerate(combined_array[:, 1]):  # Update all measure according to measure's chord
        if chord_array[int(item) - 1, 0] != '':
            combined_array[iteration, 5] = chord_array[int(item) - 1, 0]  # chord root
            combined_array[iteration, 6] = chord_array[int(item) - 1, 1]  # chord type
            combined_array[iteration, 11] = chord_array[int(item) - 1, 2]  # chord encoded
        else:
            if iteration != 0:
                combined_array[iteration, 5] = chord_array[int(item) - 2, 0]  # chord root
                combined_array[iteration, 6] = chord_array[int(item) - 2, 1]  # chord type
                combined_array[iteration, 11] = chord_array[int(item) - 2, 2]  # chord encoded

    df = pd.DataFrame(combined_array, columns=['time', 'measure', 'key fifths', 'key tonic',
                                               'key mode', 'chord root', 'chord type', 'note root',
                                               'note octave', 'note duration', 'key encoded', 'chord encoded',
                                               'note encoded'])

    df['chord root'] = df['chord root'].replace('', '[]')
    df['chord type'] = df['chord type'].replace('', '[]')

    index = df[df['chord type'] == '[]'].index
    df['chord encoded'][index] = 24
    without_ex = os.path.splitext(path)[0]
    basename = os.path.basename(without_ex)
    df.to_excel(f'{basename}.xlsx', sheet_name=f'{basename}', index=False)



