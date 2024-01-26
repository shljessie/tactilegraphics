import music21 as m21
from midiutil import MIDIFile
import yfinance as yf
from datetime import datetime
from sklearn.preprocessing import MinMaxScaler
df = yf.download(tickers='BTC-USD', period = 'max', interval = '1d')
df['days'] = np.arange(len(df))

# time data (in beats)
music_duration = 120 #seconds
tempo = 85 #bpm
scaler = MinMaxScaler((0,music_duration*(tempo/60)))
beats = scaler.fit_transform(df['days'].values.reshape(-1,1)).reshape(-1)

# compress value
values = df.Close.values
# map values optional
# scaler = MinMaxScaler((0,1))
# values = scaler.fit_transform(values.reshape(-1,1))

# octave range
octave_range = m21.scale.MajorScale('c').getPitches('c3','b4',direction='ascending')
octave_range_midi = [x.midi for x in octave_range]

# map values to midi note numbers
scaler = MinMaxScaler((0,len(octave_range)-1))
pitch = scaler.fit_transform(values.reshape(-1,1)).round().reshape(-1)
pitch = [octave_range_midi[int(x)] for x in pitch]

# map values to velocity
scaler = MinMaxScaler((30,127))
velocity = scaler.fit_transform(values.reshape(-1,1)).round().reshape(-1)
velocity = [int(x) for x in velocity]

track = 0
time = 0
channel = 0
duration = 1   # In beats
tempo = 85      # In BPM
MyMIDI = MIDIFile(1) 
MyMIDI.addTempo(track,time,tempo)
for i in range(len(df)):
    MyMIDI.addNote(track, channel, pitch[i], beats[i], duration,
                  velocity[i])
with open("bitcoin_c_major.mid", "wb") as output_file:
    MyMIDI.writeFile(output_file)