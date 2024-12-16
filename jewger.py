import pygame
import random
import os

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

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Marathon Crosser")

# Load and start background music
pygame.mixer.music.load('jogger.mp3')
pygame.mixer.music.play(-1)  # -1 means loop indefinitely

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

def main():
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
    won = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

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
                player.y = SCREEN_HEIGHT - PLAYER_SIZE - 10
                player.rect.y = player.y

        # Check win condition
        if player.y < 50:  # Reached the top
            won = True
            running = False

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

    if won:
        # Stop the music when game is won
        pygame.mixer.music.stop()
        
        font = pygame.font.Font(None, 74)
        text = font.render('You Won!', True, GREEN)
        screen.blit(text, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2))
        pygame.display.flip()
        pygame.time.wait(2000)

    # Clean up
    pygame.mixer.music.stop()
    pygame.quit()

if __name__ == "__main__":
    main()

