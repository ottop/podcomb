# PodComb

## What is PodComb?
PodComb is an application that combines an image file with an audio file into a video. 

It is written for Linux systems with GTK4. The binary was compiled on Ubuntu 23.04 with PyInstaller, so there may be issues with older systems. In that case, look into manual compilation.

## Screenshots
![Screenshot from 2023-09-07 21-25-33](https://github.com/ottop/podcomb/assets/60475104/51faca1b-8645-48bd-97f4-01648a31d3f0)
![Screenshot from 2023-09-07 21-26-04](https://github.com/ottop/podcomb/assets/60475104/4611b890-22de-4c8e-926d-217abb68b068)

![Screenshot from 2023-09-07 21-25-38](https://github.com/ottop/podcomb/assets/60475104/2f4c9b40-4468-45de-860a-da6cdc2407a3)

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
