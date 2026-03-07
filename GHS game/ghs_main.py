"""
GHS Game

The pygame library is required to run this programme.
To install pygame, use either:
1. pip install pygame
2. conda install pygame

Rules:
1. Click on the correct GHS symbols for each chemical.
2. For chemicals with no GHS symbols, click on 'No GHS Symbol'.
3. For chemicals with multiple GHS symbols, the correct GHS symbol will have
   a green box if you click on it. Wrong symbols have a red box.
4. Each correct answer increases your score by 1.
5. There is no animation for changing of questions. Look carefully.
6. Game ends after 3 incorrect answers.
"""

import pygame
import sys
import time
import random
import json


"""Game Constants"""

WIDTH, HEIGHT = 1000, 700
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 60, 60)
GREEN = (60, 200, 60)
GRAY = (200, 200, 200)

"""GHS Image File Mapping"""

GHS_IMAGES = {
    "Explosive": "ghs_images/explosive.png",
    "Flammable": "ghs_images/flammable.png",
    "Oxidizer": "ghs_images/oxidizer.png",
    "Environmental Hazard": "ghs_images/environment.png",
    "Corrosive": "ghs_images/corrosive.png",
    "Toxic": "ghs_images/toxic.png",
    "Health Hazard": "ghs_images/health.png",
    "Irritant": "ghs_images/irritant.png"
}




class GHSSymbol:
    """
    Represents a clickable GHS pictogram
    """

    def __init__(self, name, position):
        self.name = name
        self.image = pygame.image.load(GHS_IMAGES[name]).convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, (120, 120))
        self.rect = self.image.get_rect(topleft=position)

        self.highlight_color = None
        self.highlight_until = None

    def draw(self, screen):
        if self.highlight_color:
            pygame.draw.rect(
                screen,
                self.highlight_color,
                self.rect.inflate(10, 10),
                4
            )
        screen.blit(self.image, self.rect)

    def highlight(self, color, duration=None):
        self.highlight_color = color
        self.highlight_until = None if duration is None else time.time() + duration

    def clear_highlight(self):
        self.highlight_color = None
        self.highlight_until = None

    def update(self):
        if self.highlight_until is not None and time.time() > self.highlight_until:
            self.clear_highlight()





class ChemistryGame:
    """
    Main game code
    """

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("GHS Chemistry Game")

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 28)
        self.large_font = pygame.font.SysFont(None, 36)
        self.game_over_font = pygame.font.SysFont(None, 72)

        self.chemicals = self.load_chemical_data("chemicals.json")

        self.symbols = self.create_symbols()

        self.no_ghs_button = pygame.Rect(0, 0, 220, 45)
        self.no_ghs_button.center = (WIDTH // 2, HEIGHT // 2 + 180)

        self.restart_button = pygame.Rect(0, 0, 200, 50)
        self.restart_button.center = (WIDTH // 2, HEIGHT // 2 + 140)

        self.reset_game()

    def load_chemical_data(self, filename):
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)

    def reset_game(self):
        self.score = 0
        self.wrong_questions = 0
        self.game_over = False
        self.game_over_time = None
        self.load_new_chemical()

    def load_new_chemical(self):
        self.chemical = random.choice(self.chemicals)
        self.correct_symbols = set(self.chemical["ghs"])
        self.selected_correct = set()
        self.wrong_clicks = 0

        for symbol in self.symbols:
            symbol.clear_highlight()

    def create_symbols(self):
        symbols = []

        icon_size = 120
        spacing_x = 40
        spacing_y = 40

        names = list(GHS_IMAGES.keys())
        total = len(names)

        # Layout: max 4 symbols per row
        cols = min(4, total)
        rows = (total + cols - 1) // cols

        grid_width = cols * icon_size + (cols - 1) * spacing_x
        grid_height = rows * icon_size + (rows - 1) * spacing_y

        start_x = (WIDTH - grid_width) // 2
        start_y = (HEIGHT - grid_height) // 2 - 40  # slight upward offset for text

        for i, name in enumerate(names):
            row = i // cols
            col = i % cols

            x = start_x + col * (icon_size + spacing_x)
            y = start_y + row * (icon_size + spacing_y)

            symbols.append(GHSSymbol(name, (x, y)))

        return symbols


    def handle_click(self, position):
        if self.game_over:
            if self.restart_button.collidepoint(position):
                self.reset_game()
            return

        # Handle "No GHS Symbol" button
        if self.no_ghs_button.collidepoint(position):
            if len(self.correct_symbols) == 0:
                self.score += 1
                self.load_new_chemical()
            else:
                self.register_wrong()
            return

        for symbol in self.symbols:
            if symbol.rect.collidepoint(position):
                self.process_symbol_click(symbol)

    def process_symbol_click(self, symbol):
        if symbol.name in self.correct_symbols:
            if symbol.name not in self.selected_correct:
                symbol.highlight(GREEN)
                self.selected_correct.add(symbol.name)

                if self.selected_correct == self.correct_symbols:
                    self.score += 1
                    self.load_new_chemical()
        else:
            symbol.highlight(RED, duration=1)
            self.selected_correct.clear()
            self.register_wrong()

            for s in self.symbols:
                if s.highlight_color == GREEN:
                    s.clear_highlight()

    def register_wrong(self):
        self.wrong_clicks += 1

        if self.wrong_clicks >= 2:
            self.wrong_questions += 1
            if self.wrong_questions >= 2:
                self.game_over = True
                self.game_over_time = time.time()
            else:
                self.load_new_chemical()

    def draw_ui(self):
        instruction = self.large_font.render(
            "Click on the GHS symbols for the following chemical:",
            True, BLACK
        )
        self.screen.blit(
            instruction,
            instruction.get_rect(center=(WIDTH // 2, 40))
        )

        chem_text = self.large_font.render(
            f"{self.chemical['name']} ({self.chemical['formula']})",
            True, BLACK
        )
        self.screen.blit(
            chem_text,
            chem_text.get_rect(center=(WIDTH // 2, 90))
        )

        score_text = self.font.render(f"Points: {self.score}", True, BLACK)
        self.screen.blit(score_text, score_text.get_rect(midleft=(20, HEIGHT - 30)))

        pygame.draw.rect(self.screen, GRAY, self.no_ghs_button, border_radius=6)
        pygame.draw.rect(self.screen, BLACK, self.no_ghs_button, 2, border_radius=6)

        no_ghs_text = self.font.render("No GHS Symbol", True, BLACK)
        self.screen.blit(
            no_ghs_text,
            no_ghs_text.get_rect(center=self.no_ghs_button.center)
        )

    def draw_game_over(self):
        game_over_text = self.game_over_font.render("GAME OVER", True, BLACK)
        self.screen.blit(
            game_over_text,
            game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 80))
        )

        final_score = self.large_font.render(
            f"Final Score: {self.score}", True, BLACK
        )
        self.screen.blit(
            final_score,
            final_score.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        )

        pygame.draw.rect(self.screen, GREEN, self.restart_button, border_radius=6)
        pygame.draw.rect(self.screen, BLACK, self.restart_button, 2, border_radius=6)

        restart_text = self.font.render("Restart", True, BLACK)
        self.screen.blit(
            restart_text,
            restart_text.get_rect(center=self.restart_button.center)
        )

    def update(self):
        for symbol in self.symbols:
            symbol.update()

    def draw(self):
        self.screen.fill(WHITE)

        if self.game_over:
            self.draw_game_over()
        else:
            self.draw_ui()
            for symbol in self.symbols:
                symbol.draw(self.screen)

        pygame.display.flip()

    def run(self):
        running = True

        while running:
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)

            if self.game_over and time.time() - self.game_over_time >= 10:
                running = False

            self.update()
            self.draw()

        pygame.quit()



"""Starting the programme"""

if __name__ == "__main__":
    ChemistryGame().run()