
# SIDA setup steps

Create VPS on Digital Ocean, or install Docker on your server of choice.


Run Audio ML Lab container for server:

```
docker rm -f audio_ml_lab
docker pull hipstas/audio-ml-lab-server
docker run -it --name audio_ml_lab -p 8887:8887 -v /sharedfolder/:/sharedfolder/ hipstas/audio-ml-lab-server
```



Model training is based on two types of collections: media sets and label sets.

- Media set: ZIP file(s) containing MP3s, WAVs, and/or MP4 videos
    - Sample datasets by speaker: http://xtra.arloproject.com/datasets/audio/AAPB_Hand_Labeled/

- Label set: CSV file(s), 5 columns:

```
"Media file basename","Start","Duration","Label","Labeled by"
spe_1995_0423_clinton,40.0,1.0,"Bill Clinton","Stephen Reid McLaughlin"
spe_1995_1127_clinton,237.0,1.0,"Bill Clinton","Stephen Reid McLaughlin"
```

Hand-labeled audio collections can be helpful, but it is necessary to do some data cleaning by choosing 1-second clips at random.

We can combine multiple ad hoc collections of labeled audio to train models, downsampling as needed to get the right balance.

Adjustable hyperparameters for feature extraction: window size and number of MFCCs.
    - Good default value for window: 4096 end_samples
    -
