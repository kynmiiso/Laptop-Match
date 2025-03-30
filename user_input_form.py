"""
CSC111 Project 2 User Input Form

Form to gather information from user about an ideal laptop and display recommendations
"""
from random import randint

import pygame
from main import load_laptop_graph, add_dummy
import requests
from io import BytesIO
import doctest
import python_ta
import python_ta.contracts as contracts

from main import Graph, load_laptop_graph

pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode([1600, 900])
font = pygame.font.Font(None, 20)

color_active = pygame.color.Color(179, 158, 181)
color_inactive = pygame.color.Color(80, 80, 80)
white = (255, 255, 255)
bg_color = (30, 30, 30)

questions = [
    'What is the minimum price you would pay for a laptop(CAD)?',
    'What is the maximum price you would pay for a laptop (CAD)?',
    'Which processor would you like to have? (Intel/AMD/Apple)',
    'Which processing power would you like to have for the laptop? (Less/Medium/High)',
    'How much RAM (Random Access Memory) would you like to have? (4 GB/8 GB/16 GB/32 GB)',
    'What Operating System would you like to have? (Mac/Windows/Chrome)',
    'How much storage (SSD) would you like to have? (128 GB/256 GB/512 GB/1 TB/2 TB)',
    'Roughly, what display size (in inches) would you like to have? (Integer from 12-17)',
    'How many laptop recommendations would you like? (Integer from 1-20)'
]

valid_options = [
    None,
    None,  # can be any price
    ['Intel', 'AMD', 'Apple'],
    ['Less', 'Medium', 'High'],
    ['4 GB', '8 GB', '16 GB', '32 GB'],
    ['Mac', 'Windows', 'Chrome'],
    ['128 GB', '256 GB', '512 GB', '1 TB', '2 TB'],
    [str(n) for n in range(12, 18)],
    [str(i) for i in range(1, 21)]
]

box_width = 200
box_height = 50
box_spacing = 100


class InputBox:
    """Create an Input Box to gather user input."""
    def __init__(self, x, y, w, h, question, valid_opt):
        self.active = False
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color_inactive
        self.text = ''
        self.question = question
        self.valid_options = valid_opt

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

        for lst in self.valid_options:
            print(f'{self.text.strip().lower()} == {lst.strip().lower()}')
            if isinstance(lst, str) and self.text.strip().lower() == lst.strip().lower():
                return True
        return False


class Button:
    """ Class for buttons to submit or go back to form."""

    def __init__(self, x, y, w, h, button_text):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color_inactive
        self.specs = {}  # will include final data
        self.button_text = button_text

    def event_handler(self, event, input_boxes: list):
        """Handles the events occurring in the main loop"""

        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            for box in input_boxes:
                if box[0].text > box[1].text:
                    return None
                if not box.check_validity():
                    return None
            for i, box in enumerate(input_boxes):
                self.specs[questions[i]] = box.text
            return self.specs
        return None

    def draw_box(self):
        """Draws the input box and text"""
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = font.render(self.button_text, True, white)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)


class DisplayRecommendations:
    """New screen to display final laptop recs.
    """
    def __init__(self, recommendations):
        self.recommendations = recommendations
        self.scroll = 0
        self.back_button = Button(1200, 75 - self.scroll, box_width, box_height, "Go to Form")
        self.total_height = len(recommendations) * 150

    def display_recs(self, limit: int):
        """Draw the recommendations on screen, for a number of laptops within the limit, including
        a larger display of the main laptop with its specs."""

        screen_height = 900
        item_height = 150

        laptop_width = 300
        laptop_height = 300
        x_space = 50
        y_space = 50
        x_start = 100
        y_start = 250
        scroll_speed = 30

        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN and self.back_button.rect.collidepoint(event.pos):
                    return True  # to go back to form

                elif event.type == pygame.MOUSEWHEEL:
                    self.scroll -= event.y * scroll_speed
                    self.scroll = max(0, min(self.scroll, self.total_height - screen_height))

            screen.fill(bg_color)
            title_font = pygame.font.Font(None, 30)
            title_surf = title_font.render("Recommended Laptops", True, white)
            screen.blit(title_surf, (650, 50 - self.scroll))

            if not self.recommendations:
                no_recs = font.render("No laptop recommendations found. Please try again!", True, white)
                screen.blit(no_recs, (600, 30))
                pygame.display.flip()
                continue

            primary_laptop = self.recommendations[0]
            primary_rect = pygame.Rect(100, 150 - self.scroll, 600, 400)
            pygame.draw.rect(screen, color_inactive, primary_rect, 2)

            name = font.render(f"Best Recommendation: {primary_laptop['Name']}", True, white)
            screen.blit(name, (150, 200 - self.scroll))

            y_offset = 240

            for spec, value in primary_laptop.items():
                if spec != 'Name' and spec != 'Image':
                    spec_text = font.render(f"{spec}: {value}", True, white)
                    screen.blit(spec_text, (150, y_offset - self.scroll))
                    y_offset += 50
                if spec == 'Image':
                    response = requests.get(value)
                    image_data = BytesIO(response.content)
                    img = pygame.image.load(image_data)
                    img = pygame.transform.scale(img, (300, 200))
                    screen.blit(img, (350, 270 - self.scroll))

            for i in range(1, limit):
                for _ in self.recommendations[i]:
                    row = (int(i) + 1) // 4
                    col = (int(i) + 1) % 4

                    x = x_start + col * (laptop_width + x_space)
                    y = y_start + row * (laptop_height + y_space) - self.scroll
                    if item_height < y < screen_height:
                        pygame.draw.rect(screen, color_inactive, (x, y, laptop_width, laptop_height))
                        if len(self.recommendations[i]['Name']) <= 40:
                            name = font.render(f"{self.recommendations[i]['Name']}", True, white)
                            screen.blit(name, (x + 20, y + 20))
                        else:
                            rec_name_first_line = self.recommendations[i]['Name'][:40]
                            rec_name_second_line = self.recommendations[i]['Name'][40:]
                            name_1 = font.render(f"{rec_name_first_line}", True, white)
                            name_2 = font.render(f"{rec_name_second_line}", True, white)
                            screen.blit(name_1, (x + 20, y + 20))
                            screen.blit(name_2, (x + 20, y + 40))

            self.back_button.draw_box()

            pygame.display.flip()
            pygame.time.Clock().tick(60)

        return False


def load_boxes():
    """Loads text input boxes to get user input about specs for laptop.
    """

    pygame.init()
    form_screen = pygame.display.set_mode([1600, 900])
    pygame.display.set_caption("Laptop Recommendation Form")

    input_boxes = []

    half = len(questions) // 2
    if len(questions) % 2 != 0:
        half += 1

    for i in range(half):
        x = 100
        y = 100 + i * box_spacing
        input_boxes.append(InputBox(x, y, box_width, box_height, questions[i], valid_options[i]))

    for i in range(half, len(questions)):
        x = 800
        y = 100 + (i - half) * box_spacing
        input_boxes.append(InputBox(x, y, box_width, box_height, questions[i], valid_options[i]))

    submit_button = Button(800, 700, box_width, box_height, "Submit")
    exit_button = Button(1050, 700, box_width, box_height, "Exit")

    # todo: addition
    sample_specs = Button(500, 700, box_width, box_height, "Sample")

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

            if event.type == pygame.MOUSEBUTTONDOWN and exit_button.rect.collidepoint(event.pos):
                run = False

            # todo: addition
            if event.type == pygame.MOUSEBUTTONDOWN and sample_specs.rect.collidepoint(event.pos):
                # data_spec = ['500', '1000', 'AMD', 'Medium', '8 GB', 'Windows', '256 GB', '13']

                # RANDOMISE DATA SPEC SAMPLE
                min_price = randint(300, 700)
                max_price = randint(min_price, 1500)
                data_spec_sample = [str(min_price), str(max_price)]

                for lst in valid_options:
                    if lst is None:
                        continue
                    data_spec_sample.append(lst[randint(0, len(lst) - 1)])

                # print(data_spec_sample)
                for i, box in enumerate(input_boxes[0:8]):
                    box.text = data_spec_sample[i]

            if event.type == pygame.MOUSEBUTTONDOWN and submit_button.rect.collidepoint(event.pos):
                all_valid = True
                for box in input_boxes:
                    try:
                        if not box.check_validity():
                            all_valid = False
                            error_message = "Please enter a valid input from the options in brackets in all fields!"
                        elif float(input_boxes[0].text) > float(input_boxes[1].text):
                            all_valid = False
                            error_message = "Budget cannot be more than max price!"
                    except ValueError:
                        all_valid = False
                        error_message = "Please enter only numbers in the prices fields!"

                if all_valid:
                    user_specs = {}
                    for i, box in enumerate(input_boxes):
                        if valid_options[i] is None:
                            user_specs[i] = float(box.text)
                        elif isinstance(valid_options[i], tuple):
                            user_specs[i] = float(box.text)
                        else:
                            user_specs[i] = box.text
                    if user_specs:

                        lim_key = list(user_specs)[8]
                        lim = int(user_specs[lim_key])
                        graph, img_links = load_laptop_graph('laptops.csv')
                        price_tolerence = abs(int(list(user_specs.values())[0]) - int(list(user_specs.values())[1]))
                        dummy_laptop_id = -1
                        add_dummy(graph, user_specs)
                        recs_id_list = graph.recommended_laptops(dummy_laptop_id, lim, price_tolerence)
                        recs = graph.id_to_rec(recs_id_list, lim, img_links)
                        go_back = DisplayRecommendations(recs).display_recs(lim)
                        if not go_back:
                            continue

                        run = True
                else:
                    show_error = True

            form_screen.fill(bg_color)
            for box in input_boxes:
                box.draw_box()
            submit_button.draw_box()
            exit_button.draw_box()

            # todo: addition
            sample_specs.draw_box()

            if error_message and show_error:
                error_surf = font.render(error_message, True, (255, 0, 0))  # Red for errors
                form_screen.blit(error_surf, (800, 750))

            pygame.display.flip()
            clock.tick(60)

    pygame.quit()
    return user_specs


if __name__ == "__main__":
    g = load_laptop_graph("laptops.csv")[0]

    # op = g.recommended_laptops(-1, limit, diff)  # TODO: GET LIMIT SOMEHOW FUSDUFISUFH
    # # TODO: forward to output screen
    #
    # print(op)
    # # output_function(op, g)

    # g = load_laptop_graph("laptops.csv")

    specs = load_boxes()

    doctest.testmod()
    python_ta.check_all(config={
        'extra-imports': [],
        'allowed-io': [],
        'max-line-length': 120
    })

    contracts.check_all_contracts("user_input_form.py")
