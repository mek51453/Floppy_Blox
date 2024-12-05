import pygame
import sys
from game import Game
import json  # Used for managing score files

def main_menu():
    pygame.init()

    WIDTH, HEIGHT = 1000, 800
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flopy Blox - Main Menu")

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)  # Red color
    DARK_RED = (200, 0, 0)
    GREY = (150, 150, 150)

    font = pygame.font.SysFont("Arial", 30)
    big_font = pygame.font.SysFont("Arial", 50)

    input_active = False  # To check if the input box is selected
    player_name = ""  # Store the player's name
    input_box_color = GREY  # Color of the input box
    message = ""  # Store status messages (e.g., "Save Successful")
    message_timer = 0  # Controls the duration of the status message
    show_rank = False  # For showing the ranking screen

    score_file = "scores.json"  # File to store scores

    # Load background image
    try:
        menu_background = pygame.image.load("images/menu_background.jpg")
        menu_background = pygame.transform.scale(menu_background, (WIDTH, HEIGHT))
    except pygame.error as e:
        print(f"Error loading background image: {e}")
        pygame.quit()
        sys.exit()

    # Load Tip image (e.g., "tip_image.png")
    try:
        tip_image = pygame.image.load("images/tip_image.png")  # Adjust to match your image file name
        tip_image = pygame.transform.scale(tip_image, (700, 700))  # Resize the image
    except pygame.error as e:
        print(f"Error loading tip image: {e}")
        tip_image = None  # If the image cannot be loaded, it won't be displayed

    # Variable for controlling the visibility of the Tip
    tip_visible = False  # Whether to show or hide the Tip

    # Load and manage the score file
    def load_scores():
        try:
            with open(score_file, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_scores(scores):
        with open(score_file, "w") as file:
            json.dump(scores, file)

    scores = load_scores()  # Load scores from the file

    def draw_button(screen, text, x, y, width, height, color, hover_color):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if x < mouse_x < x + width and y < mouse_y < y + height:
            pygame.draw.rect(screen, hover_color, (x, y, width, height))
        else:
            pygame.draw.rect(screen, color, (x, y, width, height))

        text_surface = font.render(text, True, WHITE)
        screen.blit(text_surface, (x + (width - text_surface.get_width()) // 2, y + (height - text_surface.get_height()) // 2))

    running = True
    while running:
        screen.blit(menu_background, (0, 0))  # Draw the background image

        # If showing the ranking
        if show_rank:
            title_text = big_font.render("Rankings", True, BLACK)
            screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))
            
            # Display ranking from the file
            rank_y = HEIGHT // 3
            sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
            for idx, (name, score) in enumerate(sorted_scores):
                rank_text = font.render(f"{idx + 1}. {name}: {score}", True, BLACK)
                screen.blit(rank_text, (WIDTH // 2 - rank_text.get_width() // 2, rank_y))
                rank_y += 40

            draw_button(screen, "Back", WIDTH // 2 - 80, HEIGHT - 100, 160, 50, GREEN, DARK_RED)

        else:
            # Draw buttons
            draw_button(screen, "Play", WIDTH // 2 - 80, HEIGHT // 2, 160, 50, GREEN, DARK_RED)
            draw_button(screen, "Exit", WIDTH // 2 - 80, HEIGHT // 2 + 60, 160, 50, GREEN, DARK_RED)
            draw_button(screen, "Rank", WIDTH // 2 - 80, HEIGHT // 2 + 120, 160, 50, GREEN, DARK_RED)

            draw_button(screen, "Tip", WIDTH - 120, 20, 100, 40, GREEN, DARK_RED)

            # Show Tip image if tip_visible is True
            if tip_visible and tip_image:
                tip_x = (WIDTH - tip_image.get_width()) // 2
                tip_y = (HEIGHT - tip_image.get_height()) // 2
                screen.blit(tip_image, (tip_x, tip_y))

            # If Tip is not visible
            if not tip_visible:
                # Input box for player name
                pygame.draw.rect(screen, input_box_color, (WIDTH // 2 - 200, HEIGHT // 2 - 80, 300, 40), 2)
                name_text = player_name if input_active or player_name else "Name"
                name_surface = font.render(name_text, True, WHITE)
                screen.blit(name_surface, (WIDTH // 2 - 190, HEIGHT // 2 - 75))

                # OK button
                draw_button(screen, "OK", WIDTH // 2 + 120, HEIGHT // 2 - 80, 60, 40, GREEN, DARK_RED)

                # Show status message
                if message:
                    message_color = GREEN if message != "Please enter your name before play" else RED
                    message_surface = font.render(message, True, message_color)
                    screen.blit(message_surface, (WIDTH // 2 - message_surface.get_width() // 2, HEIGHT // 2 - 140))
                    message_timer -= 1
                    if message_timer <= 0:
                        message = ""

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Click on the name input box
                if WIDTH // 2 - 200 < mouse_x < WIDTH // 2 + 100 and HEIGHT // 2 - 80 < mouse_y < HEIGHT // 2 - 40:
                    input_active = True
                    input_box_color = GREEN
                else:
                    input_active = False
                    input_box_color = GREY

                # OK button
                if WIDTH // 2 + 120 < mouse_x < WIDTH // 2 + 180 and HEIGHT // 2 - 80 < mouse_y < HEIGHT // 2 - 40:
                    if player_name:  # If the player has entered a name
                        message = "Save Success"
                        message_timer = 60  # Set the message duration to 60 frames
                        input_box_color = GREY  # Change input box color
                        # Save player data
                        if player_name in scores:
                            scores[player_name] = max(scores[player_name], 0)  # Check old score
                        else:
                            scores[player_name] = 0  # Set score to 0 for new players
                        save_scores(scores)
                    else:  # If the name is not entered
                        message = "Please enter your name before play"
                        message_timer = 60  # Set the message duration to 60 frames

                # Play button
                if WIDTH // 2 - 80 < mouse_x < WIDTH // 2 + 80 and HEIGHT // 2 < mouse_y < HEIGHT // 2 + 50:
                    if not player_name:
                        message = "Please enter your name before play"
                        message_timer = 60
                    else:
                        game = Game(player_name, scores)  # Start the game with the player's name
                        game.game_loop()

                # Rank button
                if WIDTH // 2 - 80 < mouse_x < WIDTH // 2 + 80 and HEIGHT // 2 + 120 < mouse_y < HEIGHT // 2 + 170:
                    show_rank = True

                # Check if the Tip button is clicked to toggle the visibility of the Tip image
                if WIDTH - 120 < mouse_x < WIDTH - 20 and 20 < mouse_y < 60:
                    tip_visible = not tip_visible  # Toggle the Tip visibility

                # Exit button
                if WIDTH // 2 - 80 < mouse_x < WIDTH // 2 + 80 and HEIGHT // 2 + 60 < mouse_y < HEIGHT // 2 + 110:
                    pygame.quit()
                    sys.exit()

                # Back button (in the ranking screen)
                if show_rank and WIDTH // 2 - 80 < mouse_x < WIDTH // 2 + 80 and HEIGHT - 100 < mouse_y < HEIGHT - 50:
                    show_rank = False

            if event.type == pygame.KEYDOWN and input_active:
                if event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                else:
                    player_name += event.unicode

    pygame.quit()

if __name__ == "__main__":
    main_menu()
