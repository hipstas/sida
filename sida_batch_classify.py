#!/usr/bin/python
import os
import sys
import attk
import numpy as np
from sklearn.externals import joblib
from moviepy.audio.io import AudioFileClip
import timeit


def classify_clip(classifier, clip_pathname):
    mfccs = attk.get_mfccs_and_deltas(clip_pathname)
    results = classifier.predict(mfccs)  ## Predicting new observation
    vowel_results=[]
    vowel_bools = attk.get_vowel_segments(clip_pathname)
    for i in range(len(results)):
        if vowel_bools[i]==True:
            vowel_results.append(results[i])
    return np.mean(vowel_results) ## Vowels only


## Takes exactly three arguments: trained .pkl model, time resolution, and directory pathname
def main(argv):
    try:
        model_path = sys.argv[1]
        resolution_secs = float(sys.argv[2])
        dir_path = sys.argv[3]
    except getopt.GetoptError:
        print "sida_batch_classify.py <pkl model pathname> <directory pathname>"
        sys.exit(2)

    print('>> Model: ' + model_path)
    print('>> Directory: ' + dir_path)

    classifier = joblib.load(model_path)

    model_basename = os.path.basename(model_path).replace('.pkl','')

    media_pathnames = attk.find_media_paths(dir_path)

    for media_pathname in media_pathnames:
        tic=timeit.default_timer()

        print('    >> Classifying '+ media_pathname.split('/')[-1])

        if media_pathname[-4:].lower() == '.wav':
            wav_pathname = media_pathname
            using_temp_wav = False

        else:
            wav_pathname = attk.temp_wav_path(wav_pathname)
            using_temp_wav = True

        snd = AudioFileClip.AudioFileClip(wav_pathname)

        classifier_output = []

        for i in range(int(attk.duration(wav_pathname)/resolution_secs)):
            try:
                snd.subclip(i * resolution_secs , (i * resolution_secs) + resolution_secs).write_audiofile('/tmp/temp_sida_clip.wav')
                classifier_output.append(classify_clip(classifier, '/tmp/temp_sida_clip.wav'))
            except Exception as e:
                classifier_output.append(0.0)
                print(e)

        media_basename = '.'.join(os.path.basename(media_pathname).split('.')[:-1])

        csv_path = os.path.join(dir_path, media_basename + '__' + model_basename+'.csv')

        print(classifier_output)

        for value in classifier_output:
            print(value)

        with open(csv_path, 'w') as fo:
            for value in classifier_output:
                start = round(value * resolution_secs, 4)
                duration = round(resolution_secs, 4)
                fo.write(str(start) + ',' + str(duration) + '\n')

        if using_temp_wav == True:
            os.remove(wav_pathname)

        print("       >> Completed in " + str(round(timeit.default_timer() - tic, 4))) + " seconds"


if __name__ == "__main__":
   main(sys.argv)
