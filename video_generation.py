import pygame
import pymunk
import os
import moviepy.video.io.ImageSequenceClip as ImageSequenceClip

# Initialize Pygame and Pymunk
pygame.init()
display = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()
space = pymunk.Space()
FPS = 50

# Create directory for frames for video generation
frames_dir = "frames"
if not os.path.exists(frames_dir):
    os.makedirs(frames_dir)

def convert_coordinates(point): 
    """Convert Pymunk coordinates to Pygame coordinates."""
    return int(point.x), int(800 - point.y)

'''This part can be modified to generate different videos.'''
# Setting up parameters for the simulation
GRAVITY = (0, -1000)  # Gravity in Pymunk is in the negative y direction
space.gravity = GRAVITY
START_POSITION = (10, 330)  # Starting position of the body

# Initialize the Ball Object: Body and shape
body = pymunk.Body()
body.position = START_POSITION
shape = pymunk.Circle(body, 30)
shape.density = 1
space.add(body, shape)

# Initialize the slope: Static bodies and shapes
segment_body = pymunk.Body(body_type=pymunk.Body.STATIC)
segment_shape = pymunk.Segment(segment_body, (0, START_POSITION[1]- shape.radius), (800, 0), 5)
space.add(segment_body, segment_shape)

# Flat segment
flat_segment_body = pymunk.Body(body_type=pymunk.Body.STATIC)
flat_segment_shape = pymunk.Segment(flat_segment_body, (0, 150), (800, 150), 5)
space.add(flat_segment_body, flat_segment_shape)

def game():
    frame_count = 0
    max_frames = 500  # Record for ~10 seconds at 50 FPS
    
    while frame_count < max_frames:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return frame_count
        
        # Clear screen
        display.fill((255, 255, 255))
        
        # Draw circle
        x, y = convert_coordinates(body.position)
        pygame.draw.circle(display, (255, 0, 0), (int(x), int(y)), shape.radius)
        
        # Draw segments        
        pygame.draw.line(display, (0, 0, 0), (0, 500 - 3), (400, 650 - 3), 6)
        pygame.draw.line(display, (0, 0, 0), (400, 650 - 3), (800, 650 - 3), 6)
        
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
    clip = ImageSequenceClip.ImageSequenceClip(frame_files, fps=FPS)
    
    # Write video file
    output_filename = "pymunk_simulation.mp4"
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