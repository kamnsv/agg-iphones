![](https://img.shields.io/badge/python-3.11-blue)

# Purpose

- It will find all the materials from the folder provided by `SRC DIR` and copy them by shooting date to the folder `DIR DIST`
- Ranking by year and month
- The file name includes the `DIR DIST` subdirectory
- Replaces the file if the new one is heavier
- HEIC decodes to jpg

# Dependencies

```
sudo apt install software-properties-common
sudo add-apt-repository ppa:strukturag/libde265
sudo add-apt-repository ppa:strukturag/libheif
sudo apt update
sudo apt install libheif-examples ffmpeg
sudo pip install -r requirements.txt
```

# Use

```
python aggiphone.py /src/media /dst/common
```
