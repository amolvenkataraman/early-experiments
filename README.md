# early-experiments

<a href="https://haiscale.amolven.com/"><img alt="HAI Scale: code H (fully human), README A1 (mostly automated). Original 2021–22 code; README added in 2026 with AI help." src=".github/assets/hai.svg" width="100%"></a>

> [!IMPORTANT]
> **This repository is archived for preservation.** These are rough 2021–22 experiments, kept to show they existed. They aren't maintained and aren't meant for real use; dependencies are old and code has hardcoded paths.

> **About this repo:** the code is my original work from 2021–2022. The only edits remove a private map location and an old API token. The commit history was rebuilt in 2026 from the files' original dates. This README and the licence were added in 2026 with AI help.

Small computer vision and mapping experiments from 2021-2022. Each folder is a separate
experiment. They are rough: hardcoded paths, debug prints, no tests.

## TSHandDetect

Hand gesture recognition and mouse control from a webcam, using MediaPipe Hands and a small
Keras model.

- `trainer.py` - records right-hand landmarks (21 points x 3 coordinates per frame) while you
  hold a gesture and saves them to a pickle file named after the gesture class (e.g. `4.ct`).
  Press Esc to stop. Edit the output file name for each gesture.
- `model.py` - trains a small dense network on all `*.ct` files and saves `model.h5`.
- `modeltest.py` - classifies hands live: flat palm, thumbs up, thumbs down, one, two.
- `handdtetest.py` - moves the mouse pointer to your index fingertip (screen size is
  hardcoded to 1920x1080).

`0.ct`-`4.ct` are the training recordings (landmark coordinates only, no images) and
`model.h5` is the model trained on them. Only unpickle files you trust.

    pip install opencv-python mediapipe tensorflow scikit-learn pynput
    python modeltest.py      # webcam 0, uses model.h5
    python handdtetest.py
    python trainer.py        # webcam 1
    python model.py

Written against the 2021 `mediapipe.solutions` API; newer MediaPipe releases may need an
older version.

## LocationTest

Browser map viewers for GPS logs, GPX tracks and photo locations (Leaflet + OpenStreetMap).

- `imageloc.py` - reads the EXIF GPS tag of every photo in `ALBUMS` and writes
  `[[lat, lon], ...]` to `gps.json`.
- `photodisplay.html` - shows a `gps.json` file as a heatmap.
- `locationdisplay.html` - draws a GPS log (JSON array of
  `{latitude, longitude, altitude, accuracy, timestamp}`) as a line.
- `logdisplay_v2.html` - full-screen viewer combining all three: photo heatmap, GPX tracks
  and GPS logs.

    pip install gpsphoto exifread pillow
    python imageloc.py       # edit ALBUMS first
    # then open logdisplay_v2.html in a browser and pick your files

No location data is included, only the code. `leaflet-heatmap.js` is the Leaflet heatmap
plugin by Patrick Wied (MIT/Beerware, see its header).

## License

MIT, see LICENSE. `LocationTest/leaflet-heatmap.js` keeps its own license.
