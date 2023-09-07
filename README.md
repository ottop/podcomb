# PodComb

## What is PodComb?
PodComb is an application that combines an image file with an audio file into a video. 

It is written for Linux systems with GTK4. The binary was compiled on Ubuntu 23.04 with PyInstaller, so there may be issues with older systems. In that case, build the application on your system.

## Screenshots
![Screenshot from 2023-09-07 21-25-33](https://github.com/ottop/podcomb/assets/60475104/f481e212-6ff9-4717-9c61-79d41791c081)
![Screenshot from 2023-09-07 21-25-38](https://github.com/ottop/podcomb/assets/60475104/09df861f-a21c-46eb-be02-f8c193e7997e)


## How to install
1. Download the release in the Releases section
2. Open the folder of the release in a terminal
3. Run ```sudo ./install.sh```

## How to build
1. Download the release in the Releases section
2. Install pyinstaller ```pip install pyinstaller```
3. Open the folder of the release in a terminal
4. Run pyinstaller yourself: ```pyinstaller podcomb.spec```
5. Run ```sudo ./install.sh```

## How to uninstall
1. Open the folder of the release in a terminal
2. Run ```sudo ./uninstall.sh```
