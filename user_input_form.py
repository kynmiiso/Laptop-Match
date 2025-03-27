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
    'Does processor brand matter to you? (yes/no)',
    'Which processor brand would you like? (Intel, AMD, Apple)',  # if yes to prev ques
    'Which processing power would you like to have for the laptop? (Less/Medium/High)',
    'How much RAM(Random Access Memory) would you like to have? ()'
]

box_width = 200
box_height = 50
box_spacing = 50


class InputBox:
    """Create an Input Box to gather user input"""

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

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode

    def draw_box(self):
        """Draws the input box and text"""
        question_surf = font.render(self.question, True, white)
        screen.blit(question_surf, (self.rect.x, self.rect.y))
        pygame.draw.rect(screen, self.color, self.rect, 5)
        text_surface = font.render(self.text, True, white)
        screen.blit(text_surface, (self.rect.x + 10, self.rect.y + 10))


def load_boxes():
    """Loads text input boxes to get user input about specs for laptop.
    """
    input_boxes = []

    for i, question in enumerate(questions):
        x = 100
        y = 100 + i * box_spacing
        input_boxes.append(InputBox(x, y, box_width, box_height, question))

    run = True
    # main loop
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            for box in input_boxes:
                if event.type == pygame.MOUSEBUTTONDOWN or box.active:
                    # INFO: Verifies whether it is to select a text box (box inactive) or is currently an active box
                    box.event_handler(event)

        screen.fill(bg_color)

        for box in input_boxes:
            box.draw_box()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    load_boxes()
