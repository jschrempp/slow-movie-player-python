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

usage: slow-movie.py [-h] [-d DELAY] [-f FRAMES_INCREMENT] [-i INITIAL_FRAME] [-n] [-x] [-t] [-m [MP4] | -p [PLAY_DIRECTORY] | -r [RANDOM]]

Plays movies frames much slower than normal play or can play random frames from random movies. Great for small displays mounted on a wall or sitting on a desk.

options:
  -h, --help            show this help message and exit
  -d DELAY, --delay DELAY
                        delay between frames in seconds
  -f FRAMES_INCREMENT, --frames_increment FRAMES_INCREMENT
                        frame increment (frame=1 means play every frame, frame=10 means play every 10 frames)
  -i INITIAL_FRAME, --initial_frame INITIAL_FRAME
                        initial frame to display when playing the first movie in non-random mode
  -n, --no_scale        Do not scale movie frames to fit display
  -x, --debug           Display debug messages
  -t, --test_mode       Test mode: delay between frames: 1 second; frame increment: 10; scale image; random off; play directory off; debug mode on
  -m [MP4], --mp4 [MP4]
                        file name of movie to play
  -p [PLAY_DIRECTORY], --play_directory [PLAY_DIRECTORY]
                        Play every mp4 in the specified directory in order and repeat forever
  -r [RANDOM], --random [RANDOM]
                        Display random frames from random files in a directory

More information and source code at https://github.com/makeralchemy/slow-movie-player-python

```

Note that you can only specify one of the --mp4, --random, and --play_directory options. 
They are mutually exclusive and you will get an error if you try to specify any combination of them.

### Command Line Examples

Play movie.mp4 with one frame every minute

     python slow-movie.py --mp4 movie.mp4 --delay 60

Play every 10th frame of movie.mp4 every second

     python slow-movie.py --mp4 movie.mp4 --delay 1 --frames_increment 10
     
Play every 10th frame of movie.mp4 every second starting at frame 42

     python slow-movie.py --mp4 movie.mp4 --delay 1 --frames_increment 10 --initial_frame 42

Play movie.mp4, one frame every minute, with the debug messages (time to play, current frame, total frames, percent played)

     python slow-movie.py --mp4 movie.mp4 --delay 60 --debug

Once a minute display a random frame from a random .mp4 file found in the folder video1
   
     python slow-movie.py --random video1 --delay 60

Play all movies in sequence over and over from folder video5 with a three second delay between frames

     python slow-movie.py --play_directory video5 --delay 3

Play movie.mp4 in test mode (delay between frames: 1 second; frame increment: 10; scale image; debug mode on)

     python slow-movie.py --mp4 movie.mp4 --test_mode

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

To setup automatic start you need to edit two files "smp.sh" and "smp.desktop".

First edit "smp.sh":
1. Replace the two places that say {your user} with your user name. 
For example, if you setup your Raspberry Pi with the user name "makeralchemy", you would replace {your user} with makeralchemy.
2. Replace the arguments on the python command line what you want the slow movie player to do.
3. Save the file.

4. Make the file executable with the command:

       chmod +x smp.sh

Next edit "smp.desktop":

1. Replace the two places that say {your user} with your user name.
2. Save the file.

4. Put the smp.desktop file on your desktop, using this command and substituting your user name for {your user}. 

       cp /home/{your user}/slow-movie-player-python/smp.desktop /home/{your user}/Desktop/smp.desktop

5. Go to your desktop and you should see an icon called "Slow Movie Start". Double click that icon to verify that you have everything configured properly.

6. If everything works, enable autostart on boot for the Raspberry Pi (raspbian 2023-10-10 64 bit), by copying the "smp.desktop" file to the autostart system folder using the command (subsititute your user name for {your user}): 

       sudo cp /home/{your user}/slow-movie-player-python/smp.desktop  /etc/xdg/autostart
 
On your next reboot, your movie should automatically start playing!

## License
This project is licensed under the MIT license.