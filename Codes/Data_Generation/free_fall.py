'''This file generates a simulation video of free-falling objects.'''
import pygame
import pymunk
import os
import moviepy.video.io.ImageSequenceClip as ImageSequenceClip

# Initialize Pygame and Pymunk
pygame.init()
display = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()
space = pymunk.Space()
FPS = 150

# Create directory for frames for video generation
frames_dir = "frames"
if not os.path.exists(frames_dir):
    os.makedirs(frames_dir)

def convert_coordinates(point): 
    """Convert Pymunk coordinates to Pygame coordinates."""
    return int(point.x), int(800 - point.y)

"""This part can be modified to generate different videos."""

# Set up parameters for the simulation
GRAVITY = (0, -3000)  # Gravity in Pymunk is in the negative y direction
space.gravity = GRAVITY
START_POSITION = (400, 750)  # Starting position of the body
BACKGROUND_COLOR = (255, 255, 255)  # Background color for the simulation
OBJECT_COLOR =   (255, 0, 0)    # Color of the falling object

# GRAVITY = (0, -1000)  # Gravity in Pymunk is in the negative y direction
# space.gravity = GRAVITY
# START_POSITION = (400, 750)  # Starting position of the body
# BACKGROUND_COLOR = (143, 129, 122)  # Background color for the simulation
# OBJECT_COLOR = (146, 97, 35)   # Color of the falling object

# Initialize the Falling Object
body = pymunk.Body()
body.position = START_POSITION
shape = pymunk.Circle(body,60)
# shape = pymunk.Poly.create_box(body, (60, 120))  # Create a square shape instead of a circle
shape.density = 1
space.add(body, shape)

# Initialize the ground
flat_segment_body = pymunk.Body(body_type=pymunk.Body.STATIC)
flat_segment_shape = pymunk.Segment(flat_segment_body, (0, 150), (800, 150), 5)
space.add(flat_segment_body, flat_segment_shape)

def game():
    frame_count = 0
    max_frames = 100  # number of recorded frames
    
    while frame_count < max_frames:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return frame_count
        
        # Fill screen with background color
        display.fill(BACKGROUND_COLOR)
        
        # Draw object
        x, y = convert_coordinates(body.position)
        pygame.draw.circle(display, OBJECT_COLOR, (int(x), int(y)), shape.radius)
        # vertices = [convert_coordinates(body.local_to_world(v)) for v in shape.get_vertices()]
        # pygame.draw.polygon(display, OBJECT_COLOR, vertices)

        # Draw ground       
        pygame.draw.line(display, (0, 0, 0), (0, 650 - 3), (800, 650 - 3), 6)
        pygame.display.update()
        
        # Save frame
        frame_filename = os.path.join(frames_dir, f"frame_{frame_count:04d}.png")
        pygame.image.save(display, frame_filename)
        
        clock.tick(FPS)
        space.step(1/FPS)
        frame_count += 1
        
        # Print progress
        if frame_count % 50 == 0:
            print(f"Recorded {frame_count} frames...")
    
    return frame_count

def create_video(total_frames):
    """Create video from saved frames."""
    print("Creating video from frames...")
    
    # Get list of frame files
    frame_files = [os.path.join(frames_dir, f"frame_{i:04d}.png") for i in range(total_frames)]
    
    # Create video clip
    clip = ImageSequenceClip.ImageSequenceClip(frame_files, fps=50)
    
    # Write video file
    output_filename = "radiusx2.mp4"
    clip.write_videofile(output_filename, codec='libx264')
    
    print(f"Video saved as: {output_filename}")
    
    # Optional: Clean up frame files
    cleanup = input("Delete frame files? (y/n): ").lower().strip()
    if cleanup == 'y':
        for frame_file in frame_files:
            os.remove(frame_file)
        os.rmdir(frames_dir)
        print("Frame files deleted.")

# Run the simulation and record
print("Starting simulation recording...")
total_frames = game()

pygame.quit()

if total_frames > 0:
    create_video(total_frames)
    print("Recording complete!")
else:
    print("Recording was interrupted.")