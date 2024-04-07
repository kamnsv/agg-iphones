![](https://img.shields.io/badge/python-3.11-blue)

# Idea

- on your Linux PC, raises the `FTP server`
- on iOS, we set the `FTP client`
- copy all media from iphones to the computer

> the copied files must have HIEC

- use the current script to aggregate and convert photos and videos.

> I used the application [FTP Manager](https://apps.apple.com/ru/app/ftpmanager-ftp-sftp-client/id525959186)

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
