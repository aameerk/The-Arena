# Author - Hameel Babu Rasheed
# This is a ui module that is gonna be used to replace most of the ui I already made for my game
# It should be better than what I have now but I still expect to see some issues here and there
import pygame


class Timer:
    """The Timer class, used to time things in-game."""

    def __init__(self):
        self.start = int(pygame.time.get_ticks())
        self.seconds = 0

    def timing(self, mode=0):
        # Set mode = 0 to return the time in seconds,set mode = 1 to return the time in milliseconds.
        if mode == 0:
            self.seconds = int((pygame.time.get_ticks() - self.start) / 1000)  # How many seconds passed
        elif mode == 1:
            self.seconds = (pygame.time.get_ticks() - self.start) / 1000  # How many milliseconds passed
        return self.seconds

    def reset(self):
        self.start = int(pygame.time.get_ticks())

    def dothing(self, time):
        seconds = self.timing()
        if seconds >= time:
            print("Doing thing")  # debug
            return True


class UiText:
    """The class for text used by UI with some convenient functions"""
    def __init__(self, font_size=33):
        self.main_font = pygame.font.Font("data/fonts/runescape_uf.ttf", font_size)
        self.main_font_outline = pygame.font.Font("data/fonts/runescape_uf.ttf", font_size + 1)
        self.main_font_colour = (21, 57, 114)   # The default font colour (Blue-ish)
        self.main_font_colour2 = (23, 18, 96)   # Secondary font colour (Darker than the main font)
        self.text_speed = 0  # The speed for text to be scrolling (upto 3)
        self.text_buffer = ''   # The current buffer for the text
        self.text_timer = Timer()
        self.scrolling_flag = True
        self.current_char = 0

    def get_next_character(self, text=''):
        if len(text)  > self.current_char:
            self.text_buffer += text[self.current_char]
            self.current_char += 1

    def draw_text(self, pos, text='', outline=False, surface=pygame.Surface((0, 0))):
        height = surface.get_height()
        width = surface.get_width()
        words = [word.split(' ') for word in text.splitlines()]
        space = self.main_font.size(' ')[0]  # The size of whitespace
        space_outline = self.main_font_outline.size(' ')[0]
        x, y = pos
        x_outline = x + 1
        y_outline = y + 1
        for line in words:
            for word in line:
                rendered_word = self.main_font.render(word, True, self.main_font_colour)
                word_width, word_height = rendered_word.get_size()
                if outline:
                    rendered_word_outline = self.main_font_outline.render(word, True, self.main_font_colour2)
                    word_width2, word_height2 = rendered_word_outline.get_size()
                if x + word_width >= width - 50:
                    x = pos[0]
                    x_outline = pos[0]
                    y += word_height
                    if outline:
                        y_outline += word_height2
                if outline:
                    surface.blit(rendered_word_outline, (x, y))
                surface.blit(rendered_word, (x, y))
                x += word_width + space
                if outline:
                    x_outline += word_width2 + space_outline
            x = pos[0]
            x_outline = pos[0]
            y += word_height
            if outline:
                y_outline += word_height2

    def draw_scrolling_text(self, pos, text='', outline=False, surface=pygame.Surface((0, 0)), text_speed=0):
        if text_speed <= 0:
            self.scrolling_flag = False
        elif text_speed == 1:
            time = 0.3
        elif text_speed == 2:
            time = 0.03
        else:
            time = 0.01
        if text_speed > 0 and self.scrolling_flag:
            if self.text_timer.timing(1) >= time:
                self.get_next_character(text)
                self.text_timer.reset()
        if self.text_buffer == text:
            self.scrolling_flag = False
        if self.scrolling_flag:
            self.draw_text(pos, self.text_buffer, outline, surface)
        else:
            self.draw_text(pos, text, outline, surface)

    def fade_in(self, surface=pygame.Surface((0, 0)), delay=0.01):
        if surface.get_alpha() < 255:
            if self.text_timer.timing(1) > delay:
                surface.set_alpha(surface.get_alpha() + 5)
                self.text_timer.reset()

    def fade_out(self, surface=pygame.Surface((0, 0)), delay=0.01):
        if surface.get_alpha() > 0:
            if self.text_timer.timing(1) > delay:
                surface.set_alpha(surface.get_alpha() - 5)
                self.text_timer.reset()


    def reset_buffer(self):
        self.scrolling_flag = True
        self.current_char = 0
        self.text_buffer = ''


class TextBox:
    """The textbox class, used to draw textboxes and anything related to dialogue."""

    def __init__(self, txtcolor=(21, 57, 114), convo_flag=False):
        self.bg = pygame.image.load("data/backgrounds/rpgtxt.png").convert_alpha()  # Ui background
        self.bg_loaded = pygame.transform.scale(self.bg, (1280, 300)).convert_alpha()
        self.txtbox_surf = pygame.Surface((1260, 300))
        self.txtbox_surf.set_alpha(255)
        self.txtbox_surf.set_colorkey((0, 0, 0))
        self.txtcolor2 = (23, 18, 96)
        self.cursor = pygame.image.load("data/sprites/Cursor.png").convert_alpha()
        self.ch_cursorpos = 0  # Position of cursor for choice selection
        self.dialogue_progress = 0  # Current 'Progress' of the dialogue
        self.txtbox_height = 300
        self.popup_flag = False  # Flag for popup animation
        self.popup_done = False  # Check if the popup animation is done or not
        self.convo_flag = convo_flag  # if it is a conversation(aka story part) the popup animation won't repeat
        self.ui_text = UiText()
        self.ui_text_small = UiText(25)
        self.ui_text_small.main_font_colour = (255, 21, 45)

    def reset(self):
        self.popup_flag = False
        self.popup_done = False
        self.dialogue_progress = 0
        self.ui_text.reset_buffer()
        
    def popup(self):  # popup animation for the text box
        if not self.popup_flag:
            self.txtbox_height = 0
        self.popup_flag = True
        if self.popup_flag and self.txtbox_height < 300:
            self.txtbox_height += 50
        if self.txtbox_height >= 300:
            self.popup_done = True

    def progress_dialogue(self, dialogue):
        if self.ui_text.scrolling_flag:
            self.ui_text.scrolling_flag = False
        else:
            if self.dialogue_progress < len(dialogue) - 1:
                self.dialogue_progress += 1
                self.ui_text.reset_buffer()
                return False
            else:
                return True

    def draw_textbox(self, dialogue, surface=pygame.Surface((0, 0)), pos=(0, 0)):
        if self.txtbox_height < 300:
            self.txtbox_surf.fill((0, 0, 0, 255))
            self.txtbox_surf.blit(pygame.transform.scale(self.bg, (1280, self.txtbox_height)), (0, 0))
        if not self.popup_done:
            self.popup()
        if self.popup_done:
            self.txtbox_surf.blit(self.bg_loaded, (0, 0))
            if dialogue[self.dialogue_progress][0] != "":   # Textbox dialogue head
                speaker = pygame.image.load(dialogue[self.dialogue_progress][0]).convert_alpha()
                self.txtbox_surf.blit(speaker, (110, 70))
                self.ui_text_small.draw_text((150, 220), dialogue[self.dialogue_progress][1], False, self.txtbox_surf)    # Name of speaker
                pic_off = 0  # Offset for image when the text is drawn
            else:
                pic_off = 100

            self.ui_text.draw_scrolling_text((250 - pic_off, 60), dialogue[self.dialogue_progress][2], False, self.txtbox_surf, 3)
            self.ui_text_small.draw_text((300, 220), "Press RCTRL to continue...", False, self.txtbox_surf)

        surface.blit(self.txtbox_surf, pos)
