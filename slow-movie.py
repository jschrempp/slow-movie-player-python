import argparse
import cv2
import os
import pygame
import sys
import time
import random

BLACK_RGB = (0, 0, 0)
RED_RGB   = (255, 0, 0)

def calculate_time_to_play(number_of_frames, time_between_frames, frames_per_iteration):
    seconds = (number_of_frames * time_between_frames) / frames_per_iteration
    minutes = seconds / 60
    hours   = minutes / 60
    days    = hours   / 24
    
    # Return the time units that will be easiest for the user to understand
    if days > 1:
        return days, "days"
    elif hours > 1:
        return hours, "hours"
    elif minutes > 1:
        return minutes, "minutes"
    else:
        return seconds, "seconds"


def extract_frame(video_filename, frame_number):
    # Open the video file
    cap = cv2.VideoCapture(video_filename)

    # Check if the video file was opened successfully
    if not cap.isOpened():
        print("Error: Could not open video file.")
        return

    # Get the total number of frames in the video
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Check if the specified frame number is valid
    if frame_number < 0 or frame_number >= total_frames:
        print("Error: Invalid frame number: {frame_number:,}. Total frames:{total_frames:,}")
        return

    # Set the frame number to the desired frame
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

    # Read the frame
    ret, frame_original = cap.read()

    # Check if the frame was read successfully
    if not ret:
        print("Error: Failed to read frame.")
        return
    
    frame_RGB = cv2.cvtColor(frame_original, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
    frame_string = frame_RGB.tostring()
    frame_size = (frame_RGB.shape[1], frame_RGB.shape[0])  # Width, Height
    
    # Release the video file
    cap.release()

    if debug:
        frame_aspect_ratio = frame_RGB.shape[1] / frame_RGB.shape[0]
        print(f"frame height={frame_RGB.shape[0]} width={frame_RGB.shape[1]} aspect ratio={frame_aspect_ratio}")
        # Save the frame for debugging
        output_filename = f"debugframe.jpg"
        cv2.imwrite(output_filename, frame_original)
        print(f"Frame {frame_number} extracted and saved to {output_filename}.")

    return total_frames, frame_string, frame_size

# Example usage:

# total_frames = extract_frame(MP4_FILE, 5000)


def add_text_to_image(image, left_text, right_text, font_size=20, text_color=(255, 255, 255)):    
    # Create a font
    # font = pygame.font.Font(None, font_size)
    font = pygame.font.SysFont('arial', font_size)
    
    # Render the text
    image_rect = image.get_rect()
    
    text_surface_left = font.render(left_text, True, text_color)
    text_rect_left = text_surface_left.get_rect()
    text_rect_left.bottomleft = image_rect.bottomleft
    
    text_surface_right = font.render(right_text, True, text_color)
    text_rect_right = text_surface_right.get_rect()
    text_rect_right.bottomright = image_rect.bottomright
    
    # Blit the text onto the image
    image.blit(text_surface_left, text_rect_left)
    image.blit(text_surface_right, text_rect_right)


# main execution starts here

# get the configuration from the command line parameters

parser = argparse.ArgumentParser()
parser.add_argument("filename", help="file name of movie to play",default=None,nargs='?')
parser.add_argument("-d", "--delay", type=int, default=1
    ,help="delay between frames in seconds")
parser.add_argument("-f", "--frames_increment", type=int, default=1
    ,help='frame increment (frame=1 means play every frame, frame=10 means play every 10 frames)')
parser.add_argument("-n", "--no_scale", action="store_false"
    ,help="Do not scale movie frames to fit display") 
parser.add_argument("-r", "--random", action="store_true"
    ,help="Display random frames from random files")
parser.add_argument("-x", "--debug", action="store_true"
    ,help="Display debug messages")
parser.add_argument("-t", "--test_mode", action="store_true"
    ,help="Test mode: delay between frames: 1 second; frame increment: 10; scale image; random off; debug mode on")
args = parser.parse_args()

mp4_file = args.filename
delay_between_frames = args.delay
frames_increment = args.frames_increment
scale_image = args.no_scale
use_random_frame_file = args.random
debug = args.debug
test_mode = args.test_mode

# If test mode was specified, override the parameters to the test mode settings
if test_mode:
    delay_between_frames = 1
    frames_increment = 10
    scale_image = True 
    use_random_frame_file = False
    debug = True 

if debug:
    print(f"mp4_file={mp4_file}")
    print(f"delay_between_frames={delay_between_frames}")
    print(f"frames_increment={frames_increment}")
    print(f"scale_image={scale_image}")
    print(f"random_frame_file={use_random_frame_file}")
    print(f"debug={debug}")

# if not random, then file name is required
if not use_random_frame_file:
    if mp4_file is None:
        print("Error: file name is required")
        sys.exit()

    # Exit if the file to play can't be found
    if not(os.path.exists(mp4_file)):
        print(f"{mp4_file} can not be found!")
        sys.exit()

# Initialize PyGame
print("Initializing PyGame...")
pygame.init()

# Set up the display
print("Setting up the display...")
display_info = pygame.display.Info()

screen = pygame.display.set_mode((display_info.current_w, display_info.current_h), pygame.FULLSCREEN)
screen_width = display_info.current_w
screen_height = display_info.current_h
print(f'Screen width: {screen_width} height: {screen_height}')

# Count the number of times the movie has been played
movie_played = 0

# Loop forever - when the movie ends, start it again. Pressing ESC will stop the movie player
while True:
    # Initialize the loop variables
    total_frames = 1   # set up for just the first time through the movie playing loop
    frame_number = 0
    
    movie_played += 1
    if not use_random_frame_file:
        print(f"Playing {mp4_file}. Iteration {movie_played}.")

    # Loop to extract and display the frames
    while frame_number < total_frames:
    # when in random mode total_frames is reset within the while loop


        # Check to see if the user wants to quit
        stop = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    stop = True

        # If the user pressed ESC, exit the frame playing loop and stop the program
        if stop:
            break

        # Choose a file if needed
        if use_random_frame_file:
            # Get a random file from the current directory
            files = os.listdir()
            # remove non mp4 files
            files = [f for f in files if f.endswith(".mp4")]
            mp4_file = random.choice(files)

        # Extract the frame
        total_frames, frame_string, frame_size  = extract_frame(mp4_file, frame_number)
       
        # Print the playing time once
        if frame_number == 0:
            duration, duration_units = calculate_time_to_play(total_frames, delay_between_frames, frames_increment)
            playing_time = f"{duration:,.2f} {duration_units}"
            print(f"Time to play: {playing_time}")

        # Construct the status message
        percent_played = int((frame_number / total_frames) * 100)
        frame_message = f"Playback {movie_played:,} Frame {frame_number:,} of {total_frames:,} ({percent_played}%)"
        print(mp4_file, frame_message)


        # display the frame 
        image = pygame.image.fromstring(frame_string,frame_size,'RGB',False)
        
        if scale_image:
            # Calculate the aspect ratio of the image and the screen
            image_aspect_ratio = image.get_width() / image.get_height()
            screen_aspect_ratio = screen_width / screen_height
            if frame_number == 0:  # only print this once
                print(f"Screen aspect ratio: {screen_aspect_ratio}, Image aspect ratio: {image_aspect_ratio}")

            # Determine the scaling factor
            if image_aspect_ratio > screen_aspect_ratio:
                # Fit by width
                if frame_number == 0:  # only print this once
                    print("Scaling using fit by width")
                scale_factor = screen_width / image.get_width()
            else:
                # Fit by height
                if frame_number == 0:  # only print this once
                    print("Scaling using fit by height")
                scale_factor = screen_height / image.get_height()

            # Scale the image to fit the screen
            scaled_width = int(image.get_width()) * scale_factor
            scaled_height = int(image.get_height()) * scale_factor
            scaled_image = pygame.transform.scale(image, (scaled_width, scaled_height))

            if debug:
                print(f"Image width: {image.get_width()} height: {image.get_height()}")
                print(f"Scaled_image width: {scaled_width} height: {scaled_height}")
                if not use_random_frame_file:
                    file_info = f"{mp4_file} ({playing_time})"
                else:
                    file_info = f"{mp4_file}"
                add_text_to_image(scaled_image, file_info, frame_message)

            # Determine where to place the scaled image so it's centered on the screen
            centered_width_position = int((screen_width - scaled_width)/2)
            
            # With the image centered, make the sides black
            screen.fill(BLACK_RGB)

            # Blit the scaled image onto the screen surface
            screen.blit(scaled_image, (centered_width_position, 0))
        
        # scaled_image = False
        else:
            # fill screen to red for debugging
            screen.fill(RED_RGB)

            # Blit the scaled image onto the screen surface
            screen.blit(image, (0,0))

        pygame.display.flip()

        frame_number += frames_increment

        # wait before displaying the next frame
        time.sleep(delay_between_frames)

    # If the user pressed ESC exit the forever loop to stop the program
    if stop:
        break

pygame.quit()
