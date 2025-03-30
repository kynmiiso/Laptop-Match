"""
CSC111 Project 2 User Input Form

Form to gather information from user about an ideal laptop and display recommendations
"""
from random import randint
from io import BytesIO
from typing import Optional
import pygame
import math
import requests
import doctest
import python_ta.contracts
from graph_class import load_laptop_graph, add_dummy

pygame.init()

CLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode([1600, 900])
FONT = pygame.font.Font(None, 20)

COLOR_ACTIVE = pygame.color.Color(179, 158, 181)
COLOR_INACTIVE = pygame.color.Color(80, 80, 80)
WHITE = (255, 255, 255)
BG_COLOR = (30, 30, 30)

DUMMY_LAPTOP_ID = -1

QUESTIONS = [
    'What is the minimum price you would pay for a laptop(CAD)? (*)',
    'What is the maximum price you would pay for a laptop (CAD)? (*)',
    'Which processor would you like to have? (Intel/AMD/Apple)',
    'Which processing power would you like to have for the laptop? (Less/Medium/High)',
    'How much RAM (Random Access Memory) would you like to have? (4 GB/8 GB/16 GB/32 GB)',
    'What Operating System would you like to have? (Mac/Windows/Chrome)',
    'How much storage (SSD) would you like to have? (128 GB/256 GB/512 GB/1 TB/2 TB)',
    'Roughly, what display size (in inches) would you like to have? (Integer from 12-17)',
    'How many laptop recommendations would you like? (Integer from 1-20) (*)'
]

VALID_OPTIONS = [
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

DATA_Q = ['min_price', 'max_price', 'processor', 'processing power',
          'ram', 'os', 'storage', 'display(in inch)', 'limit']

BOX_WIDTH = 200
BOX_HEIGHT = 50
BOX_SPACING = 100


class InputBox:
    """Create an Input Box to gather user input. Takes in the x and y positions, w (width), and h (height).
    It also takes questions from the list created and only allows the user to submit their answers if their answers
    are in valid options."""
    active: bool
    rect: pygame.Rect
    color: pygame.color.Color
    text: str
    question: str
    valid_options: Optional[list[str]] = None

    def __init__(self, dim: tuple[int, int, int, int], question: str, valid_opt: Optional[list[str]] = None) -> None:
        self.active = False
        x, y, w, h = dim
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = ''
        self.question = question
        self.valid_options = valid_opt

    def event_handler(self, event: pygame.event) -> None:
        """Handles the events occurring in the main loop of the form display."""

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            if self.active:
                self.color = COLOR_ACTIVE
            else:
                self.color = COLOR_INACTIVE

        if self.active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

    def draw_box(self) -> None:
        """Draws the input box and text."""
        question_surf = FONT.render(self.question, True, WHITE)
        SCREEN.blit(question_surf, (self.rect.x, self.rect.y - 20))

        pygame.draw.rect(SCREEN, self.color, self.rect, 5)
        text_surface = FONT.render(self.text, True, WHITE)
        SCREEN.blit(text_surface, (self.rect.x + 10, self.rect.y + 10))

    def check_validity(self) -> bool:
        """Checks if the input is valid according to the valid options list. Stripped and lowercase inputs also
        allowed. Returns True if input for self.text is valid and False if not valid."""
        if not self.text:
            return False

        if self.valid_options is None:  # for price
            return True

        for lst in self.valid_options:
            # print(f'{self.text.strip().lower()} == {lst.strip().lower()}')
            if isinstance(lst, str) and self.text.strip().lower() == lst.strip().lower():
                return True
        return False


class Button:
    """Class for buttons to submit user's ideal laptop specs or go back to form.  Takes in the x and y positions,
    w (width), and h (height). Also has a specs attribute to store laptop specs from user input."""

    rect: pygame.Rect
    color: pygame.color.Color
    specs: dict
    button_text: str

    def __init__(self, dim: tuple[int, int, int, int], button_text: str) -> None:
        x, y, w, h = dim
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.specs = {}  # will include final data
        self.button_text = button_text

    # def event_handler(self, event, input_boxes: list):
    #     """Handles the events occurring in the main loop when button is pressed."""
    #
    #     if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
    #         for box in input_boxes:
    #             if box[0].text > box[1].text:
    #                 return None
    #             if not box.check_validity():
    #                 return None
    #         for i, box in enumerate(input_boxes):
    #             self.specs[questions[i]] = box.text
    #         return self.specs
    #     return None

    def draw_box(self) -> None:
        """Draws the button and text."""
        pygame.draw.rect(SCREEN, self.color, self.rect)
        text_surface = FONT.render(self.button_text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        SCREEN.blit(text_surface, text_rect)


class DisplayRecommendations:
    """A new screen to display final laptop recommendations."""

    recommendations: dict
    scroll: int
    back_button: Button
    total_height: int

    def __init__(self, recommendations: dict) -> None:
        self.recommendations = recommendations
        self.scroll = 0
        self.back_button = Button((1200, 75 - self.scroll, BOX_WIDTH, BOX_HEIGHT), "Go to Form")
        self.total_height = len(recommendations) * 150

    def display_recs(self, limit: int) -> bool:
        """Draw the recommendations on screen, for a number of laptops within the limit, including
        a larger display of the main laptop with its specs. Also has a scroll functionality for the
        screen. Returns False if the user quit the screen, and returns True to go back to the
        form when back button is pressed."""

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

            primary_laptop = self.recommendations[0]
            primary_rect = pygame.Rect(100, 150 - self.scroll, 600, 400)
            pygame.draw.rect(screen, color_inactive, primary_rect, 2)

            name = font.render(f"Best Recommendation: {primary_laptop['Name']}", True, white)
            screen.blit(name, (150, 200 - self.scroll))

            y_offset = 240

            for spec, value in primary_laptop.items():
                if spec not in {'Name', 'Image'}:
                    spec_text = font.render(f"{spec}: {value}", True, white)
                    screen.blit(spec_text, (150, y_offset - self.scroll))
                    y_offset += 50
                if spec == 'Image':
                    response = requests.get(value)
                    image_data = BytesIO(response.content)
                    img = pygame.image.load(image_data)
                    img = pygame.transform.scale(img, (300, 200))
                    screen.blit(img, (350, 270 - self.scroll))

            self.draw_text(limit)

        return False

    def draw_text(self, limit: int) -> None:
        """Split the text into 2 lines if longer than the box."""
        for i in range(1, limit):
            for _ in self.recommendations[i]:
                row = (int(i) + 1) // 4
                col = (int(i) + 1) % 4

                x = x_start + col * (laptop_width + x_space)
                y = y_start + row * (laptop_height + y_space) - self.scroll
                if item_height < y < screen_height:
                    pygame.draw.rect(screen, color_inactive, (x, y, laptop_width, laptop_height))
                    self.split_line(self.recommendations[i]['Name'], x, y)

        self.back_button.draw_box()
        pygame.display.flip()
        pygame.time.Clock().tick(60)

    def split_line(self, name: str, x: int, y: int) -> None:
        """Splits the text into 2 lines if longer than box."""
        if len(name) <= 40:
            name_ = font.render(name, True, white)
            screen.blit(name_, (x + 20, y + 20))
        else:
            rec_name_first_line = name[:40]
            rec_name_second_line = name[40:]
            name_1 = font.render(f"{rec_name_first_line}", True, white)
            name_2 = font.render(f"{rec_name_second_line}", True, white)
            screen.blit(name_1, (x + 20, y + 20))
            screen.blit(name_2, (x + 20, y + 40))


def generate_random_specs(valid_options: list) -> list:
    """Generate a random combination of laptop specs according to what is required"""
    # RANDOMISE DATA SPEC SAMPLE
    min_price = randint(300, 700)
    max_price = randint(min_price, 1500)
    data_spec_sample = [str(min_price), str(max_price)]

    for lst in valid_options:
        if lst is None:
            continue
        data_spec_sample.append(lst[randint(0, len(lst) - 1)])

    return data_spec_sample


def mod_box(input_boxes: list[InputBox], data_spec_sample: list) -> None:
    """modify input boxes contents to certain text"""
    for i, box in enumerate(input_boxes[0:8]):
        box.text = data_spec_sample[i]


def verify(input_boxes: list[InputBox]) -> tuple[bool, str]:
    """verify box contentes"""
    all_valid = True
    filled = 0
    err_msg = ''
    for i, box in enumerate(input_boxes):
        if box.text == '' and i != 8:  # skip empty boxes
            continue

        try:
            if not box.check_validity():
                all_valid = False
                err_msg = "Please enter a valid input from the options in brackets in all fields!"
            elif float(input_boxes[0].text) > float(input_boxes[1].text):
                all_valid = False
                err_msg = "Budget cannot be more than max price!"
        except ValueError:
            all_valid = False
            err_msg = "Please enter only numbers in the prices fields!"

        filled += 1

    enable_partial_matching = (filled > 2 and all(b.text != '' for b in input_boxes[0:2])
                               and input_boxes[8].text != '')
    # note that price values will be checked in previous try-except

    return (all_valid and enable_partial_matching), err_msg


def get_user_specs(input_boxes: list[InputBox]) -> tuple[dict, list]:
    """Get specs and kind of unfilled input boxes from user input"""
    empty_boxes = []
    user_specs = {}
    for i, box in enumerate(input_boxes):
        if box.text == '':
            empty_boxes.append(DATA_Q[i])
            continue

        if VALID_OPTIONS[i] is None:
            user_specs[i] = float(box.text)
        elif isinstance(VALID_OPTIONS[i], tuple):
            user_specs[i] = float(box.text)
        else:
            user_specs[i] = box.text

    return user_specs, empty_boxes


def submit(all_valid: bool, input_boxes: list[InputBox], dummy_laptop_id: int = -1) -> None:
    """submit all info"""
    if not all_valid:
        return

    if all_valid:
        user_specs, empty_boxes = get_user_specs(input_boxes)
        assert all(i in user_specs for i in [0, 1, 8])
        lim = int(user_specs[8])
        graph, img_links = load_laptop_graph('laptops.csv', 'parameters_data.json')
        # price_tolerence = abs(int(list(user_specs.values())[0]) - int(list(user_specs.values())[1]))
        price_tolerence = (float(user_specs[1]) - float(user_specs[0])) / 2
        add_dummy(graph, user_specs, dummy_laptop_id)

        recs_id_list = graph.recommended_laptops(dummy_laptop_id, lim, price_tolerence, empty_boxes)
        # dummy_laptop_id -= 1  # reduce DUMMY LAPTOP ID every time we send a new laptop in
        recs = graph.id_to_rec(recs_id_list, lim, img_links)
        _ = DisplayRecommendations(recs).display_recs(lim)


def load_boxes(dummy_laptop_id: int = -1) -> None:
    """Loads text input boxes to get user input about specs for laptop. Returns the user's preferred specifications
     for the laptop from the input."""

    pygame.init()
    form_screen = pygame.display.set_mode([1600, 900])
    pygame.display.set_caption("Laptop Recommendation Form")

    input_boxes = []

    # half = math.ceil(len(QUESTIONS) / 2)

    for i in range(math.ceil(len(QUESTIONS) / 2)):
        x = 100
        y = 100 + i * BOX_SPACING
        input_boxes.append(InputBox((x, y, BOX_WIDTH, BOX_HEIGHT), QUESTIONS[i], VALID_OPTIONS[i]))

    for i in range(math.ceil(len(QUESTIONS) / 2), len(QUESTIONS)):
        x = 800
        y = 100 + (i - math.ceil(len(QUESTIONS) / 2)) * BOX_SPACING
        input_boxes.append(InputBox((x, y, BOX_WIDTH, BOX_HEIGHT), QUESTIONS[i], VALID_OPTIONS[i]))

    submit_button = Button((800, 700, BOX_WIDTH, BOX_HEIGHT), "Submit")
    exit_button = Button((1050, 700, BOX_WIDTH, BOX_HEIGHT), "Exit")
    sample_specs = Button((150, 700, BOX_WIDTH, BOX_HEIGHT), "Randomise")

    run = True
    # user_specs = None
    error_message = None
    # show_error = False

    # main loop
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            for box in input_boxes:
                box.event_handler(event)

            if event.type == pygame.MOUSEBUTTONDOWN and exit_button.rect.collidepoint(event.pos):
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN and sample_specs.rect.collidepoint(event.pos):
                # data_spec = ['500', '1000', 'AMD', 'Medium', '8 GB', 'Windows', '256 GB', '13']
                data_spec_sample = generate_random_specs(VALID_OPTIONS)
                mod_box(input_boxes, data_spec_sample)

            if event.type == pygame.MOUSEBUTTONDOWN and submit_button.rect.collidepoint(event.pos):
                all_valid, error_message = verify(input_boxes)
                submit(all_valid, input_boxes, dummy_laptop_id)
                dummy_laptop_id -= 1

            form_screen.fill(BG_COLOR)
            for box in input_boxes:
                box.draw_box()

            submit_button.draw_box()
            exit_button.draw_box()
            sample_specs.draw_box()

            form_screen.blit(FONT.render("Enter a proper value for the required fields marked (*)", True,
                                         (255, 255, 255)), (150, 800))
            form_screen.blit(FONT.render(error_message, True, (255, 0, 0)), (800, 750))

            pygame.display.flip()
            CLOCK.tick(60)

    pygame.quit()


if __name__ == "__main__":

    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode([1600, 900])
    font = pygame.font.Font(None, 20)

    color_active = pygame.color.Color(179, 158, 181)
    color_inactive = pygame.color.Color(80, 80, 80)
    white = (255, 255, 255)
    bg_color = (30, 30, 30)

    dummy_laptop_id = -1

    questions = [
        'What is the minimum price you would pay for a laptop(CAD)? (*)',
        'What is the maximum price you would pay for a laptop (CAD)? (*)',
        'Which processor would you like to have? (Intel/AMD/Apple)',
        'Which processing power would you like to have for the laptop? (Less/Medium/High)',
        'How much RAM (Random Access Memory) would you like to have? (4 GB/8 GB/16 GB/32 GB)',
        'What Operating System would you like to have? (Mac/Windows/Chrome)',
        'How much storage (SSD) would you like to have? (128 GB/256 GB/512 GB/1 TB/2 TB)',
        'Roughly, what display size (in inches) would you like to have? (Integer from 12-17)',
        'How many laptop recommendations would you like? (Integer from 1-20) (*)'
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

    screen_height = 900
    item_height = 150

    laptop_width = 300
    laptop_height = 300
    x_space = 50
    y_space = 50
    x_start = 100
    y_start = 250
    scroll_speed = 30

    # specs = load_boxes()
    load_boxes(-1)

    doctest.testmod()
    python_ta.check_all(config={
        'extra-imports': [
            'random',
            'pygame',
            'graph_class',
            'requests',
            'io',
            'math'  # only for ceiling function lol soz
        ],
        'allowed-io': [],
        'max-line-length': 120
    })

    python_ta.contracts.check_all_contracts("user_input_form.py")
