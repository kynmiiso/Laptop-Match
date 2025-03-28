"""
CSC111 Project 2 User Input Form

Form to gather information from user about an ideal laptop, in order to inject as a vertex in the graph for comparison
"""

import pygame
import sys

pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode([1600, 900])
font = pygame.font.Font(None, 20)

color_active = pygame.color.Color(179, 158, 181)
color_inactive = pygame.color.Color(80, 80, 80)
white = (255, 255, 255)
bg_color = (30, 30, 30)

questions = [
    'What is your ideal price for a laptop (CAD)?',
    'Does processor brand matter to you, and if so which would you like to have? (Intel/AMD/Apple/No)',
    'Which processing power would you like to have for the laptop? (Less/Medium/High)',
    'How much RAM(Random Access Memory) would you like to have? (4 GB/8 GB/16 GB/32 GB)',
    'What Operating System would you like to have? (Mac/Windows)',
    'How much storage(SSD) would you like to have? (128 GB/256 GB/512 GB/1 TB/2 TB)'
    'What display size would you like to have? ()'
]

box_width = 200
box_height = 50
box_spacing = 100


class InputBox:
    """Create an Input Box to gather user input."""
    def __init__(self, x, y, w, h, question):
        self.active = False
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color_inactive
        self.text = ''
        self.question = question

    def event_handler(self, event):
        """Handles the events occurring in the main loop"""

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            if self.active:
                self.color = color_active
            else:
                self.color = color_inactive

        if self.active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

    def draw_box(self):
        """Draws the input box and text"""
        question_surf = font.render(self.question, True, white)
        screen.blit(question_surf, (self.rect.x, self.rect.y - 20))

        pygame.draw.rect(screen, self.color, self.rect, 5)
        text_surface = font.render(self.text, True, white)
        screen.blit(text_surface, (self.rect.x + 10, self.rect.y + 10))


class SubmitButton:
    """ Class for submit button
    """

    def __init__(self, x, y, w, h, button_text):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color_inactive
        self.specs = []  # will include final data
        self.button_text = button_text

    def event_handler(self, event, input_boxes: list):
        """Handles the events occurring in the main loop"""

        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            specs = {}
            for i, box in enumerate(input_boxes):
                specs[questions[i]] = box.text
            return specs
        return None

    def draw_box(self):
        """Draws the input box and text"""
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = font.render("Submit", True, white)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)


def load_boxes():
    """Loads text input boxes to get user input about specs for laptop.
    """
    input_boxes = []

    for i, question in enumerate(questions):
        x = 100
        y = 100 + i * box_spacing
        input_boxes.append(InputBox(x, y, box_width, box_height, question))

    submit_button = SubmitButton(800, 700, box_width, box_height, "Submit")

    run = True
    user_specs = None
    # main loop
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            for box in input_boxes:
                if event.type == pygame.MOUSEBUTTONDOWN or box.active:
                    # INFO: Verifies whether it is to select a text box (box inactive) or is currently an active box
                    box.event_handler(event)

            specs = submit_button.event_handler(event, input_boxes)
            if specs:
                user_specs = specs
                run = False

        screen.fill(bg_color)

        for box in input_boxes:
            box.draw_box()

        submit_button.draw_box()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    return user_specs


if __name__ == "__main__":
    specs = load_boxes()
    for ques, ans in specs.items():
        print(f"{ques}: {ans}")
