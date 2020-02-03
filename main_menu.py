import sys

sys.path.insert(0, '../../')

speed = 5

map_one = []

import os
from random import randrange
import pygame
import pygameMenu

# -----------------------------------------------------------------------------
# Constants and global variables
# -----------------------------------------------------------------------------
ABOUT = ['Author: @{0}'.format('Dan095ss'),
         pygameMenu.locals.TEXT_NEWLINE,
         'Email: {0}'.format("daniil095ss@gmail.com")]
COLOR_BACKGROUND = (128, 0, 128)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
SELECT_MAP = ['1']
FPS = 60.0
MENU_BACKGROUND_COLOR = (228, 55, 36)
WINDOW_SIZE = (640, 480)

clock = None
main_menu = None
surface = None

# -----------------------------------------------------------------------------
# Methods
# -----------------------------------------------------------------------------
def change_map(value, level):
    selected, index = value
    print('Selected level: "{0}" ({1}) at index {2}'.format(selected, level, index))
    SELECT_MAP[0] = level


def random_color():
    return randrange(0, 255), randrange(0, 255), randrange(0, 255)


def play_function(level, test=False):
    assert isinstance(level, (tuple, list))
    level = level[0]
    assert isinstance(level, str)

    # Define globals
    global main_menu
    global clock

    if level == '1':
        os.system('python game.py')
        sys.exit()
    # elif level == '2':
    #     os.system('python game.py')
    #     sys.exit()
    # elif level == '3':
    #     os.system('python game.py')
    else:
        raise Exception('Unknown map selected {0}'.format(level))


    bg_color = random_color()
    f_width = f.get_size()[0]

    main_menu.disable()
    main_menu.reset(1)

    while True:

        # Clock tick
        clock.tick(60)

        # Application events
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                exit()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE and main_menu.is_disabled():
                    main_menu.enable()

                    # Quit this function, then skip to loop of main-menu on line 317
                    return

        # Pass events to main_menu
        main_menu.mainloop(events)

        # Continue playing
        surface.fill(bg_color)
        surface.blit(f, ((WINDOW_SIZE[0] - f_width) / 2, WINDOW_SIZE[1] / 2))
        pygame.display.flip()

        # If test returns
        if test:
            break


def main_background():
    global surface
    surface.fill(COLOR_BACKGROUND)


def main(test=False):
    global clock
    global main_menu
    global surface

    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    surface = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption('Piano Tiles - Project')
    clock = pygame.time.Clock()

    pygame.mixer.music.load("data/intro.mp3")  # a.mp3
    pygame.mixer.music.play(-1)

    play_menu = pygameMenu.Menu(surface,
                                bgfun=main_background,
                                color_selected=COLOR_WHITE,
                                font=pygameMenu.font.FONT_BEBAS,
                                font_color=COLOR_BLACK,
                                font_size=30,
                                menu_alpha=100,
                                menu_color=MENU_BACKGROUND_COLOR,
                                menu_height=int(WINDOW_SIZE[1] * 0.7),
                                menu_width=int(WINDOW_SIZE[0] * 0.7),
                                onclose=pygameMenu.events.DISABLE_CLOSE,
                                option_shadow=False,
                                title='Play menu',
                                window_height=WINDOW_SIZE[1],
                                window_width=WINDOW_SIZE[0]
                                )
    play_menu.add_option('Start',  # When pressing return -> play(SELECT_MAP[0], font)
                         play_function,
                         SELECT_MAP,
                         pygame.font.Font(pygameMenu.font.FONT_FRANCHISE, 30))
    play_menu.add_selector('Select level',
                           [('1', '1')],
                           onchange=change_map,
                           selector_id='select_level')
    play_menu.add_option('Return to main menu', pygameMenu.events.BACK)

    # About menu
    about_menu = pygameMenu.TextMenu(surface,
                                     bgfun=main_background,
                                     color_selected=COLOR_WHITE,
                                     font=pygameMenu.font.FONT_BEBAS,
                                     font_color=COLOR_BLACK,
                                     font_size_title=30,
                                     # font_title=pygameMenu.font.FONT_8BIT,
                                     menu_color=MENU_BACKGROUND_COLOR,
                                     menu_color_title=COLOR_WHITE,
                                     menu_height=int(WINDOW_SIZE[1] * 0.6),
                                     menu_width=int(WINDOW_SIZE[0] * 0.6),
                                     onclose=pygameMenu.events.DISABLE_CLOSE,
                                     option_shadow=False,
                                     text_color=COLOR_BLACK,
                                     text_fontsize=20,
                                     title='About',
                                     window_height=WINDOW_SIZE[1],
                                     window_width=WINDOW_SIZE[0]
                                     )
    for m in ABOUT:
        about_menu.add_line(m)
    about_menu.add_line(pygameMenu.locals.TEXT_NEWLINE)
    about_menu.add_option('Return to menu', pygameMenu.events.BACK)

    # Main menu
    main_menu = pygameMenu.Menu(surface,
                                bgfun=main_background,
                                color_selected=COLOR_WHITE,
                                font=pygameMenu.font.FONT_BEBAS,
                                font_color=COLOR_BLACK,
                                font_size=30,
                                menu_alpha=100,
                                menu_color=MENU_BACKGROUND_COLOR,
                                menu_height=int(WINDOW_SIZE[1] * 0.6),
                                menu_width=int(WINDOW_SIZE[0] * 0.6),
                                onclose=pygameMenu.events.DISABLE_CLOSE,
                                option_shadow=False,
                                title='Main menu',
                                window_height=WINDOW_SIZE[1],
                                window_width=WINDOW_SIZE[0]
                                )

    main_menu.add_option('Play', play_menu)
    main_menu.add_option('About', about_menu)
    main_menu.add_option('Quit', pygameMenu.events.EXIT)

    # Configure main menu
    main_menu.set_fps(FPS)

    while True:

        # Tick
        clock.tick(FPS)

        # Paint background
        main_background()

        # Application events
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

        # Main menu
        main_menu.mainloop(events, disable_loop=test)

        # Flip surface
        pygame.display.flip()

        # At first loop returns
        if test:
            break


if __name__ == '__main__':
    main()