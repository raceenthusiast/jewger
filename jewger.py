import pygame
import random
import sys
from moviepy import VideoFileClip

# Initialize Pygame and its mixer
pygame.init()
pygame.mixer.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SIZE = 50
RUNNER_SIZE = 40
RUNNER_SPEED = 5

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jewger")

# sounds
collision_sound = pygame.mixer.Sound('collision.mp3')
victory_sound = pygame.mixer.Sound('victory.mp3')

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        # Load and scale player image
        self.image = pygame.image.load("player.png")
        self.image = pygame.transform.scale(self.image, (PLAYER_SIZE, PLAYER_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def move(self, dx, dy):
        new_x = self.x + dx
        new_y = self.y + dy
        
        # Keep player within screen bounds
        if 0 <= new_x <= SCREEN_WIDTH - PLAYER_SIZE:
            self.x = new_x
            self.rect.x = new_x
        if 0 <= new_y <= SCREEN_HEIGHT - PLAYER_SIZE:
            self.y = new_y
            self.rect.y = new_y

class Runner:
    def __init__(self, y):
        self.x = -RUNNER_SIZE
        self.y = y
        self.speed = RUNNER_SPEED
        # Load and scale runner image
        self.image = pygame.image.load("runner.png")
        self.image = pygame.transform.scale(self.image, (RUNNER_SIZE, RUNNER_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def move(self):
        self.x += self.speed
        self.rect.x = self.x
        if self.x > SCREEN_WIDTH:
            self.x = -RUNNER_SIZE
            self.rect.x = self.x

def play_victory_video():
    # Load video with audio using moviepy
    video = VideoFileClip('victory.mp4')
    pygame.mixer.music.set_volume(0.3)  # Reduce to 30% volume
    victory_sound.play()
    
    # Get video properties
    frame_width = int(video.w)
    frame_height = int(video.h)
    fps = video.fps
    frame_duration = 1/fps
    
    # Scale video to fit screen while leaving room for text
    scale = min(SCREEN_WIDTH / frame_width, (SCREEN_HEIGHT - 100) / frame_height)
    new_width = int(frame_width * scale)
    new_height = int(frame_height * scale)
    
    # Calculate position to center the video
    x_offset = (SCREEN_WIDTH - new_width) // 2
    y_offset = ((SCREEN_HEIGHT - 100) - new_height) // 2

    # Create font for victory message
    font = pygame.font.Font(None, 48)
    text = font.render("Oy Vey So Dangerous I'm Shaking But You Won!", True, GREEN)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
    
    playing = True
    duration = video.duration
    start_time = pygame.time.get_ticks() / 1000  # Convert to seconds
    last_frame_time = start_time
    
    clock = pygame.time.Clock()
    
    while playing:
        current_time = pygame.time.get_ticks() / 1000 - start_time
        
        if current_time >= duration:
            playing = False
            continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    playing = False
                    pygame.quit()
                    sys.exit()
                else:
                    # Any other key press will skip the video
                    playing = False
                    continue

        # Get current frame
        try:
            frame = video.get_frame(current_time)
            
            # Convert frame to pygame surface
            frame = pygame.image.frombuffer(frame.tobytes(), (frame_width, frame_height), "RGB")
            frame = pygame.transform.scale(frame, (new_width, new_height))
            
            # Clear screen
            screen.fill(BLACK)
            
            # Draw frame centered
            screen.blit(frame, (x_offset, y_offset))
            
            # Draw victory message
            screen.blit(text, text_rect)
            
            pygame.display.flip()
            
            # Control playback speed
            clock.tick(fps)
            
        except Exception as e:
            print(f"Error getting frame: {e}")
            playing = False

    # Clean up video but don't stop the music
    video.close()

def play_background_music():
    pygame.mixer.music.load('jogger.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(1.0)  # Return to full volume

def game_loop():
    clock = pygame.time.Clock()
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - PLAYER_SIZE - 10)
    
    # Create runners in different lanes
    runners = []
    num_lanes = 4
    lane_height = (SCREEN_HEIGHT - 100) // num_lanes
    for i in range(num_lanes):
        y = 100 + i * lane_height
        # Create multiple runners per lane with different starting positions
        for j in range(3):
            runner = Runner(y)
            runner.x = random.randint(0, SCREEN_WIDTH)
            runner.rect.x = runner.x
            runners.append(runner)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False

        # Handle player movement
        keys = pygame.key.get_pressed()
        dx = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * 5
        dy = (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * 5
        player.move(dx, dy)

        # Move runners
        for runner in runners:
            runner.move()

        # Check collisions
        for runner in runners:
            if player.rect.colliderect(runner.rect):
                collision_sound.play()
                player.y = SCREEN_HEIGHT - PLAYER_SIZE - 10
                player.rect.y = player.y

        # Check win condition
        if player.y < 50:  # Reached the top
            return True

        # Draw everything
        screen.fill(WHITE)
        
        # Draw finish line
        pygame.draw.rect(screen, GREEN, (0, 0, SCREEN_WIDTH, 50))
        
        # Draw lanes
        for i in range(num_lanes):
            y = 100 + i * lane_height
            pygame.draw.line(screen, BLUE, (0, y), (SCREEN_WIDTH, y), 2)

        # Draw runners
        for runner in runners:
            screen.blit(runner.image, runner.rect)

        # Draw player
        screen.blit(player.image, player.rect)

        pygame.display.flip()
        clock.tick(60)

    return False

def main():
    running = True
    
    while running:
        # Start background music if it's not playing
        if not pygame.mixer.music.get_busy():
            play_background_music()
        
        # Run game loop
        won = game_loop()
        
        if won:
            # Play the victory video (music continues)
            play_victory_video()
        else:
            running = False

    # Clean up
    pygame.mixer.music.stop()
    pygame.quit()

if __name__ == "__main__":
    main()
