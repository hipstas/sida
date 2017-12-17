form Test command line calls
	sentence wav_file
endform

wav_name$ = replace$(wav_file$, ".wav", "", 0);
wav_name$ = replace$(wav_name$, ".mp3", "", 0);

Read from file: wav_file$
selectObject: "Sound 'wav_name$'"
To Formant (burg): 0.0, 5.0, 5500.0, 0.025, 50.0
selectObject: "Formant 'wav_name$'"

dur = Get total duration

print starttime,endtime,F1,F2,F3,F4'newline$'
i = 0.5
while i < dur - 0.5
	j = i+0.005
	print 'i','j',
	mean = Get mean: 1, i, j, "Hertz"
	print 'mean',
	mean = Get mean: 2, i, j, "Hertz"
	print 'mean',
	mean = Get mean: 3, i, j, "Hertz"
	print 'mean',
	mean = Get mean: 4, i, j, "Hertz"
	print 'mean''newline$'
	i = i + 0.005
endwhile
