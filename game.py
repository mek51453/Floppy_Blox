import pygame
import random
import time
import sys
import json


# Set the background for the menu and main game
menu_background = pygame.image.load("images/menu_background.jpg")
game_background = pygame.image.load("images/game_background.jpg")

# Load images for bird, pipe, monster, and explosion
bird_image = pygame.image.load("images/bird_image.png")
pipe_image = pygame.image.load("images/pipe_image.png")
monster_image = pygame.image.load("images/monster_image.png")
explosion_image = pygame.image.load("images/explosion_image.png")  # Added explosion image

class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40
        self.velocity = 0
        self.rotation = 0  # Variable for rotation

    def move(self):
        self.velocity += 0.3  # Reduce gravity strength
        self.y += self.velocity

        # When jumping, the bird will rotate
        if self.velocity < 0:
            self.rotation = max(self.rotation - 1, -15)  # Slow down rotation for smoother movement
        else:
            self.rotation = min(self.rotation + 1, 15)  # Slow down rotation for smoother movement

    def jump(self):
        self.velocity = -5  # Reduce jump force for softer jumps
        self.rotation = -15  # Start rotating at a smaller angle when jumping

    def draw(self, screen):
        # Rotate the bird image based on the rotation angle
        bird_scaled = pygame.transform.scale(bird_image, (self.width, self.height))
        bird_rotated = pygame.transform.rotate(bird_scaled, self.rotation)
        screen.blit(bird_rotated, (self.x, self.y))

class Pipe:
    def __init__(self, x):
        self.x = x
        self.width = 60
        self.height = random.randint(100, 300)
        self.gap = 200
        self.passed = False

    def move(self):
        self.x -= 5

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), (self.x, 0, self.width, self.height))
        pygame.draw.rect(screen, (0, 0, 0), (self.x, self.height + self.gap, self.width, 744 - (self.height + self.gap)))

class Monster:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40
        self.is_dead = False  # Variable to check if the monster is dead

    def move(self):
        self.x -= 5

    def draw(self, screen):
        if not self.is_dead:
            # Display monster image
            monster_scaled = pygame.transform.scale(monster_image, (self.width, self.height))
            screen.blit(monster_scaled, (self.x, self.y))
        else:
            # Display explosion image when the monster is dead
            explosion_scaled = pygame.transform.scale(explosion_image, (50, 50))
            screen.blit(explosion_scaled, (self.x, self.y))

    def check_collision_with_bullet(self, bullet):
        if self.x < bullet.x + bullet.width and self.x + self.width > bullet.x:
            if self.y < bullet.y + bullet.height and self.y + self.height > bullet.y:
                return True
        return False

class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 10
        self.height = 5
        self.velocity = 10

    def move(self):
        self.x += self.velocity

    def draw(self, screen):
        pygame.draw.rect(screen, (173, 216, 230), (self.x, self.y, self.width, self.height))

def save_scores(scores):
    with open('scores.json', 'w') as f:
        json.dump(scores, f)
    
class Game:
    def __init__(self, player_name, scores):
        self.player_name = player_name  # Added player name input
        self.scores = scores  # Added scores input
        self.width = 1000
        self.height = 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Floppy Bird")
        
        self.bird = Bird(100, self.height // 2)
        self.pipes = []
        self.monsters = []
        self.bullets = []
        self.score = 0
        self.ammo = 10
        self.last_shoot_time = 0
        self.reload_time = 10
        self.reload_start_time = None
        self.ground_x = 0
        self.game_over_flag = False  # Flag to track if the game is over

    def check_collision(self):
        for pipe in self.pipes:
            if self.bird.x + self.bird.width > pipe.x and self.bird.x < pipe.x + pipe.width:
                if self.bird.y < pipe.height or self.bird.y + self.bird.height > pipe.height + pipe.gap:
                    return True
        for monster in self.monsters:
            if not monster.is_dead:  # Do not check for collisions with dead monsters
                if self.bird.x + self.bird.width > monster.x and self.bird.x < monster.x + monster.width:
                    if self.bird.y < monster.y + monster.height and self.bird.y + self.bird.height > monster.y:
                        return True
        if self.bird.y + self.bird.height > self.height - 50:  # Ground check
            return True
        return False

    def reset_game(self):
        self.bird = Bird(100, self.height // 2)
        self.pipes.clear()
        self.monsters.clear()
        self.bullets.clear()
        self.score = 0
        self.ammo = 10
        self.reload_start_time = None
        self.ground_x = 0
        self.game_over_flag = False

    def game_loop(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            self.screen.blit(game_background, (0, 0))  # Use the game background
            self.handle_events()

            if self.game_over_flag:
                self.game_over()  # Show game over screen
                pygame.display.flip()
                clock.tick(60)
                continue  # Skip game loop if game over

            self.bird.move()
            self.bird.draw(self.screen)

            # Spawn pipes
            if len(self.pipes) == 0 or self.pipes[-1].x < self.width - 200:
                self.pipes.append(Pipe(self.width))

            for pipe in self.pipes:
                pipe.move()
                if pipe.x + pipe.width < 0:
                    self.pipes.remove(pipe)
                if pipe.x + pipe.width / 2 < self.bird.x and not pipe.passed:
                    self.score += 1
                    pipe.passed = True
                pipe.draw(self.screen)

            # Spawn monsters
            if len(self.monsters) == 0 or self.monsters[-1].x < self.width - 200:
                self.monsters.append(Monster(self.width, random.randint(100, 500)))

            for monster in self.monsters:
                monster.move()
                if monster.x + monster.width < 0:
                    self.monsters.remove(monster)

                # Check if bullet hits monster
                for bullet in self.bullets:
                    if monster.check_collision_with_bullet(bullet):
                        self.score += 1  # Increase score when monster is hit
                        monster.is_dead = True  # Mark monster as dead
                        self.bullets.remove(bullet)    # Bullet destroyed
                        break

                monster.draw(self.screen)

            # Handle bullets
            for bullet in self.bullets:
                bullet.move()
                if bullet.x > self.width:
                    self.bullets.remove(bullet)
                bullet.draw(self.screen)

            # Draw score and ammo
            score_text = pygame.font.SysFont("Arial", 30).render(f"Score: {self.score}", True, (173, 216, 230))
            self.screen.blit(score_text, (10, 10))

            ammo_text = pygame.font.SysFont("Arial", 30).render(f"Ammo: {self.ammo}", True, (173, 216, 230))
            self.screen.blit(ammo_text, (10, 50))

            if self.check_collision():
                self.game_over_flag = True  # Set game over flag

            if self.reload_start_time:
                if time.time() - self.reload_start_time >= self.reload_time:
                    self.ammo = 5
                    self.reload_start_time = None

            pygame.display.flip()
            clock.tick(60)

    def game_over(self):
        font = pygame.font.SysFont("Arial", 50)
        game_over_text = font.render("GAME OVER", True, (255, 0, 0))
        self.screen.blit(game_over_text, (self.width // 2 - game_over_text.get_width() // 2, self.height // 3))

        # Show the final score in the game over screen
        final_score_text = pygame.font.SysFont("Arial", 30).render(f"Final Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(final_score_text, (self.width // 2 - final_score_text.get_width() // 2, self.height // 3 + 60))

        if self.player_name in self.scores:
            self.scores[self.player_name] = max(self.scores[self.player_name], self.score)

        else:
            self.scores[self.player_name] = self.score

        save_scores(self.scores)  # Save the updated scores

        self.draw_button("Restart", self.width // 2 - 80, self.height // 2, 160, 50)
        self.draw_button("Exit", self.width // 2 - 80, self.height // 2 + 60, 160, 50)

        pygame.display.flip()

    def draw_button(self, text, x, y, width, height):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if x < mouse_x < x + width and y < mouse_y < y + height:
            pygame.draw.rect(self.screen, (200, 0, 0), (x, y, width, height))
        else:
            pygame.draw.rect(self.screen, (0, 255, 0), (x, y, width, height))

        font = pygame.font.SysFont("Arial", 30)
        text_surface = font.render(text, True, (255, 255, 255))
        self.screen.blit(text_surface, (x + (width - text_surface.get_width()) // 2, y + (height - text_surface.get_height()) // 2))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.bird.jump()
                if event.key == pygame.K_e and self.ammo > 0:
                    bullet = Bullet(self.bird.x + self.bird.width, self.bird.y + self.bird.height // 2)
                    self.bullets.append(bullet)
                    self.ammo -= 1
                    if self.ammo == 0:
                        self.reload_start_time = time.time()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if self.width // 2 - 80 < mouse_x < self.width // 2 + 80 and self.height // 2 < mouse_y < self.height // 2 + 50:
                    self.reset_game()
                    self.game_loop()
                if self.width // 2 - 80 < mouse_x < self.width // 2 + 80 and self.height // 2 + 60 < mouse_y < self.height // 2 + 110:
                    pygame.quit()
                    sys.exit()
