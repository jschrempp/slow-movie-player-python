import cv2
import pygame
import time

BLACK_RGB = (0, 0, 0)


# Configuration settings
MP4_FILE = "DOCTOR_WHO_2_STATE_OF_DECAY.mp4" 
DELAY_BETWEEN_FRAMES = 1
FRAMES_INCREMENT = 10
SCALE_IMAGE = True
DEBUG = False

def extract_frame(video_filename, frame_number, output_filename):
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
        print("Error: Invalid frame number.")
        return

    # Set the frame number to the desired frame
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

    # Read the frame
    ret, frame = cap.read()

    # Check if the frame was read successfully
    if not ret:
        print("Error: Failed to read frame.")
        return

    # Save the frame to the specified output file
    cv2.imwrite(output_filename, frame)

    frame_aspect_ratio = frame.shape[1] / frame.shape[0]
    if DEBUG:
        print(f"frame height={frame.shape[0]} width={frame.shape[1]} aspect ratio={frame_aspect_ratio}")

    # Release the video file
    cap.release()

    if DEBUG:
        print(f"Frame {frame_number} extracted and saved to {output_filename}.")

    return total_frames

# Example usage:

# total_frames = extract_frame(MP4_FILE, 5000, "output_frame.jpg")

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

# Loop forever - when the movie ends, start it again. Pressing ESC will stop
while True:
    # Initialize the loop variables
    total_frames = 1   # set up for just the first time through the movie playing loop
    frame = 1
    
    movie_played += 1
    print(f"Playing {MP4_FILE}. Iteration {movie_played}.")

    # Loop to extract and display the frames
    while frame <= total_frames:

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

        # Extract the frame
        total_frames = extract_frame(MP4_FILE, frame, "output_frame.jpg")
        percent_played = int((frame / total_frames) * 100)
        print(f"Playback {movie_played} displaying frame {frame} of {total_frames}. {percent_played}% played.")

        # Display the frame
        image = pygame.image.load('output_frame.jpg')

        if SCALE_IMAGE:

            # Calculate the aspect ratio of the image and the screen
            image_aspect_ratio = image.get_width() / image.get_height()
            screen_aspect_ratio = screen_width / screen_height
            if frame == 1:  # only print this once
                print(f"Screen aspect ratio: {screen_aspect_ratio}, Image aspect ratio: {image_aspect_ratio}")

            # Determine the scaling factor
            if image_aspect_ratio > screen_aspect_ratio:
                # Fit by width
                if frame == 1:  # only print this once
                    print("Scaling using fit by width")
                scale_factor = screen_width / image.get_width()
            else:
                # Fit by height
                if frame == 1:  # only print this once
                    print("Scaling using fit by height")
                scale_factor = screen_height / image.get_height()

            # Scale the image to fit the screen

            scaled_width = int(image.get_width()) * scale_factor
            scaled_height = int(image.get_height()) * scale_factor

            if DEBUG:
                print(f"Image width: {image.get_width()} height: {image.get_height()}")

            scaled_image = pygame.transform.scale(image, (scaled_width, scaled_height))

            if DEBUG:
                print(f"Scaled_image width: {scaled_width} height: {scaled_height}")

            # Determine where to place the scaled image so it's centered on the screen
            centered_width_position = int((screen_width - scaled_width)/2)
            
            # With the image centered, make the sides black
            screen.fill(BLACK_RGB)

            # Blit the scaled image onto the screen surface
            screen.blit(scaled_image, (centered_width_position, 0))

        else:
            # for debugging
            screen.fill((255, 0, 0))

            screen.blit(image, (0,0))

        pygame.display.flip()

        frame += FRAMES_INCREMENT

        # wait before displaying the next frame
        time.sleep(DELAY_BETWEEN_FRAMES)

    # If the user pressed ESC exit the forever loop to stop the program
    if stop:
        break

pygame.quit()
