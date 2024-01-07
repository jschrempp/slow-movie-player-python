# Python Slow Movie Player

## Overview
*slow-movie-player.py* is a Python program used to play movies at a greatly reduced speed. 
Movies can be played at specified frame per unit of time (e.g., one frame per second, one frame per minute, etc.).
When played at these rates a typical movie can take days or months to display.
When used with a small 7" or 10" display this makes for an interesting desk display.

This program wasd inspired by Tom Whitwell's slow movie player (https://github.com/TomWhitwell/SlowMovie) that used a Raspberry Pi and an e-Ink display.
This version is a rewrite that is designed to display on a standard HDMI display.

## Usage Instructions

*slow-movie.py* can be executed from the command line, inside a shell script, or automatically started at boot (instructions below).

Before running the program, make sure to be in the slow-movie-player-python directory and have activated the virtual environment:

    cd ~/slow-movie-player-python
    source venv/bin/activate

### Command Line Usage:
```
python3 slow-movie.py -h

usage: slow-movie.py [-h] [-d DELAY] [-f FRAMES_INCREMENT] [-i INITIAL_FRAME] [-n] [-r [RANDOM]] [-x] [-t]
                     [filename]

Plays movies frames much slower than normal play or can play random frames from random movies. Great for small
displays mounted on a wall or sitting on a desk.

positional arguments:
  filename              file name of movie to play

options:
  -h, --help            show this help message and exit
  -d DELAY, --delay DELAY
                        delay between frames in seconds
  -f FRAMES_INCREMENT, --frames_increment FRAMES_INCREMENT
                        frame increment (frame=1 means play every frame, frame=10 means play every 10 frames)
  -i INITIAL_FRAME, --initial_frame INITIAL_FRAME
                        initial frame to display when playing in non-random mode
  -n, --no_scale        Do not scale movie frames to fit display
  -r [RANDOM], --random [RANDOM]
                        Display random frames from random files in a directory
  -x, --debug           Display debug messages
  -t, --test_mode       Test mode: delay between frames: 1 second; frame increment: 10; scale image; random off;
                        debug mode on

More information and source code at https://github.com/makeralchemy/slow-movie-player-python

```

### Command Line Examples

Play movie.mp4 with one frame every minute

     python slow-movie.py movie.mp4 --delay 60

Play every 10th frame of movie.mp4 every second

     python slow-movie.py movie.mp4 --delay 1 --frames_increment 10
     
Play every 10th frame of movie.mp4 every second starting at frame 42

     python slow-movie.py movie.mp4 --delay 1 --frames_increment 10 --initial_frame 42

Play movie.mp4, one frame every minute, with the debug messages (time to play, current frame, total frames, percent played)

     python slow-movie.py movie.mp4 --delay 60 --debug

Once a minute display a random frame from a random .mp4 file found in the folder video1
   
     python slow-movie.py --delay 60 --random video1

Play movie.mp4 in test mode (delay between frames: 1 second; frame increment: 10; scale image; debug mode on)

     python slow-movie.py movie.mp4 --test_mode

### Stopping the Movie

When running, the slow movie player takes over the display. 
To stop the movie, press ESC on the keyboard.

## Installation Instructions

These instructions assume you have installed the latest version of Raspberry Pi OS.
WiFi should be enabled.
If you are going to run the slow movie player on a small display without a keyboard and a mouse, you should enable SSH and VNC so you can make changes.

Before installing the libraries, you should run the standard updates:

     sudo apt-get update
     sudo apt-get upgrade

Make sure you are in your home directory:

     cd ~
     
Install the slow movie player code:

     git clone https://github.com/makeralchemy/slow-movie-player-python.git

Go to the directory of where the code is now stored:

     cd slow-movie-player-python
     
Create the virtual environment:

     python -m venv venv
     
Activate the virtual environment:

     source venv/bin/activate
     
Install the required packages:

     pip install -r requirements.txt

Test to make sure everything is working:

     python slow-movie.py Test-2s.mp4 --debug --delay 1

## Setting Up Automatic Start

TBW

## License
This project is licensed under the MIT license.