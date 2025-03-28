"""
CSC111 Project 2 User Input Form

Form to gather information from user about an ideal laptop, in order to inject as a vertex in the graph for comparison
"""

import pygame

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
    'How much RAM (Random Access Memory) would you like to have? (4 GB/8 GB/16 GB/32 GB)',
    'What Operating System would you like to have? (Mac/Windows)',
    'How much storage (SSD) would you like to have? (128 GB/256 GB/512 GB/1 TB/2 TB)',
    'What display size (in inches) would you like to have? (12/13/14/15/16/17)',
    'What average value for customer ratings would be ideal for the laptop? (Any number from 3.0 to 5.0)'
]

valid_options = [
    None,  # can be any price
    ['Intel', 'AMD', 'Apple', 'No'],
    ['Less', 'Medium', 'High'],
    ['4 GB', '8 GB', '16 GB', '32 GB'],
    ['Mac', 'Windows'],
    ['128 GB', '256 GB', '512 GB', '1 TB', '2 TB'],
    ['12', '13', '14', '15', '16', '17'],  # remove the 35-inch laptop in dataset since it's not real
    (3.0, 5.0)  # any number from range 3.0 to 5.0 (there are no ratings below that in dataset)
    # (except there's 1 with 1.6 fsr, fix later)
]

box_width = 200
box_height = 50
box_spacing = 100


class InputBox:
    """Create an Input Box to gather user input."""
    def __init__(self, x, y, w, h, question, valid_options):
        self.active = False
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color_inactive
        self.text = ''
        self.question = question
        self.valid_options = valid_options

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

    def check_validity(self):
        """Check if the input is valid according to the valid options"""
        if not self.text:
            return False

        if self.valid_options is None:  # for price
            return True

        if isinstance(self.valid_options, tuple):  # for rating
            value = float(self.text)
            return self.valid_options[0] <= value <= self.valid_options[1]

        return self.text in self.valid_options


class SubmitButton:
    """ Class for submit button
    """

    def __init__(self, x, y, w, h, button_text):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color_inactive
        self.specs = {}  # will include final data
        self.button_text = button_text

    def event_handler(self, event, input_boxes: list):
        """Handles the events occurring in the main loop"""

        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            for box in input_boxes:
                if not box.check_validity():
                    return None
            for i, box in enumerate(input_boxes):
                self.specs[questions[i]] = box.text
            return self.specs
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
    pygame.init()
    form_screen = pygame.display.set_mode([1600, 900])
    pygame.display.set_caption("Laptop Recommendation Form")

    input_boxes = []

    for i, question in enumerate(questions):
        x = 100
        y = 100 + i * box_spacing
        input_boxes.append(InputBox(x, y, box_width, box_height, question, valid_options[i]))

    submit_button = SubmitButton(800, 700, box_width, box_height, "Submit")

    run = True
    user_specs = None
    error_message = None
    show_error = False

    # main loop
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            for box in input_boxes:
                if event.type == pygame.MOUSEBUTTONDOWN or box.active:
                    # INFO: Verifies whether it is to select a text box (box inactive) or is currently an active box
                    box.event_handler(event)
                    show_error = False

            if event.type == pygame.MOUSEBUTTONDOWN and submit_button.rect.collidepoint(event.pos):
                all_valid = True
                for box in input_boxes:
                    if not box.check_validity():
                        all_valid = False
                        error_message = "Please enter a valid input from the options in brackets."

                if all_valid:
                    user_specs = {}
                    for i, box in enumerate(input_boxes):
                        if valid_options[i] is None:
                            user_specs[questions[i]] = float(box.text)
                        elif isinstance(valid_options[i], tuple):
                            user_specs[questions[i]] = float(box.text)
                        else:
                            user_specs[questions[i]] = box.text
                    run = False
                else:
                    show_error = True

        form_screen.fill(bg_color)
        for box in input_boxes:
            box.draw_box()
        submit_button.draw_box()

        if error_message and show_error:
            error_surf = font.render(error_message, True, (255, 0, 0))  # Red for errors
            form_screen.blit(error_surf, (800, 750))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    return user_specs


if __name__ == "__main__":
    specs = load_boxes()
    if specs is not None:
        for ques, ans in specs.items():
            print(f"{ques}: {ans}")
    else:
        print("Form was closed without submission.")
