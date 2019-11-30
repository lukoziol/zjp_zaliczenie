"""Zadanie kdtree

"""

import os
import time
import math
from collections import deque
import data_generator as dg
import kdtree as kdt
os.environ['SDL_VIDEO_WINDOW_POS'] = "0, 32"
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

# poziom wypisywania logów na 0 - żeby nie spowalniać
# można dać wartości z zakresu 0-5
kdt.KDTree.DEBUG_LEVEL = 0

# sekcja stałych globalnych i ważniejszych zmiennych wyświetlania
TARGET_FPS = 60
WINDOW_WIDTH = 1201
WINDOW_HEIGHT = 1001
X_OFFSET = int(WINDOW_WIDTH / 2) + 1
Y_OFFSET = int(WINDOW_HEIGHT / 2) + 1
X_SCALAR = 8
Y_SCALAR = 8
WINDOW_XRANGE = (WINDOW_WIDTH - X_OFFSET) // X_SCALAR
WINDOW_YRANGE = (WINDOW_HEIGHT - Y_OFFSET) // Y_SCALAR
LOG_SPACER = "------------------------------------------------------------------"
# kolory
CANVAS_FILL_RGB = (10, 12, 8)
FONT_INFO_RGB = (255, 225, 80)
FONT_POINT_RGB = (80, 180, 200)
POINT_NORMAL_RGB = (200, 230, 210)
POINT_TRAVERSED_RGB = (20, 200, 70)
POINT_IN_RANGE_RGB = (200, 70, 20)
AXIS_RGB = (120, 120, 110)
GRID_RGB = (20, 30, 30)
RANGE_RGB = (50, 50, 50)
RANGE_MOUSE_RGB = (100, 100, 100)
BRANCH_RGB = (20, 120, 70)
# tekst
TEXT_VERTICAL_SPACING = 16
TEXT_LEFT_OFFSET = 2
TEXT_RIGHT_OFFSET = 165
WARNING_STRING = "PRZELICZANIE"
# tekst pomocy
HELP_STRINGS = [
    "  switch set - s|S",
    "switch range - r|R",
    "generate set - m|M",
    " toggle zoom - z|Z",
    " cycle depth - d  ",
    "  toggle X|Y - p  "]


def x_to_screen(x_value):
    """Konwersja współrzednych osi X canvas na X ekranu

    :param x_value: wartość X canvas
    :return: wartość X ekranu
    """
    return x_value * X_SCALAR + X_OFFSET


def y_to_screen(y_value):
    """Konwersja współrzednych osi Y canvas na Y ekranu

    :param y_value: wartość Y canvas
    :return: wartość Y ekranu
    """
    return y_value * Y_SCALAR + Y_OFFSET


def point_to_screen(point):
    """Konwersja punktu ze współrzednych canvas na współrzedne ekranu

    :param point: punkt ze współrzednymi canvas
    :return: punkt ze współrzednymi ekranu
    """
    p_screen = None
    if point is not None:
        p_screen = (x_to_screen(point[0]), y_to_screen(point[1]))
    return p_screen


def x_to_canvas(x_value):
    """Konwersja współrzednych osi X ekranu na X canvas

    :param x_value: wartość X ekranu
    :return: wartość X canvas
    """
    return (x_value - X_OFFSET) / X_SCALAR


def y_to_canvas(y_value):
    """Konwersja współrzednych osi Y ekranu na Y canvas

    :param y_value: wartość Y ekranu
    :return: wartość Y canvas
    """
    return (y_value - Y_OFFSET) / -Y_SCALAR


def point_to_canvas(point):
    """Konwersja punktu ze współrzednych ekranu na współrzedne canvas

    :param point: punkt ze współrzednymi ekranu
    :return: punkt ze współrzednymi canvas
    """
    p_canvas = None
    if point is not None:
        p_canvas = (x_to_canvas(point[0]), y_to_canvas(point[1]))
    return p_canvas


def approximate_complexity(n_points):
    """Funkcja pomocznia do aproksymacji złożoności przeszukiwania

    :param n_points: ilość punktów w zbiorze danych
    :return: aproksymowana złożonośc obliczeniowa (rekurencja)
    """
    if n_points == 1:
        return 1
    return 2 + 2 * approximate_complexity(math.ceil(n_points / 4))


class FPSCounter:
    """Klasa pomocznicza do sprawdzania prędkości renderowania

    """

    def __init__(self, target):
        """Inicjalizacja klasy, przygotowanie zmiennych i zerowanie wartości FPS

        :param target: docelowa ilość klatek na sekundę
        """
        self.__target = target
        self.__timestamps = deque([0] * self.__target, maxlen=self.__target)
        self.__fps = 0

    def tick(self, timestamp):
        """Oblicza FPS na podstawie danych z zegara

        :param timestamp: aktualny czas
        """
        self.__timestamps.append(timestamp)
        self.__fps = self.__target / (self.__timestamps[-1] - self.__timestamps[0])

    @property
    def fps(self):
        """Wrapper do odczytu wartości FPS

        :return: zmierzona ilość klatek na sekundę
        """
        return self.__fps


def do_stuff(set_array, range_bounds):
    """Funkcja pomocnicza do tworzenia drzewa na podstawie zadanych parametrów

    :param set_array: zbiór punktów
    :param range_bounds: obszar przeszukiwania
    :return: drzewo kd
    """
    tree = kdt.KDTree(set_array)
    tree.search_range(range_bounds[0], range_bounds[1])
    print(tree)
    return tree


def draw_points(surface, points, point_color, size):
    """Funkcja rysująca punkty

    :param surface: powierzchnia rysowania
    :param points: zbiór punktów do narysowania
    :param point_color: kolor punktów
    :param size: rozmiar pojedynczego punktu
    """
    length = size * 2 + 1
    for point in points:
        pygame.draw.rect(
            surface,
            point_color,
            (int(point[0] - size), int(point[1] - size), length, length))


# komentarz pod spodem likwiduje niepotrzebne warningi z pylinta dotyczące nazw stałych
# pylint: disable=C0103
# program ------------------------------------------------------------
if __name__ == "__main__":
    print(LOG_SPACER)
    # utworzenie generatora danych
    G = dg.Generator()
    # dodanie losowych zbiorów danych
    G.generate_point_set(50, (60, 60))
    G.generate_point_set(100, (60, 60))
    G.generate_point_set(200, (60, 60))
    G.generate_point_set(300, (60, 60))
    G.generate_point_set(500, (60, 60))
    G.generate_point_set(700, (60, 60))
    G.generate_point_set(900, (70, 60))
    G.generate_point_set(1000, (70, 60))
    G.generate_point_set(10000, (70, 50), 100)
    # wybranie ostatniego zbioru (największego)
    G.prev_set()
    # przygotowanie zestawów danych
    vertices = G.point_set
    search_range = G.range
    # operacje na drzewie
    T = do_stuff(vertices, search_range)

    # inicjalizacja grafiki
    print(LOG_SPACER)
    print('Creating main window: [{:d}|{:d}]'.format(WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('KDTree')
    # zmienne rysowania
    screen_image = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    geometry_image = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    big_font = pygame.font.SysFont("consolas", 16, True, False)
    small_font = pygame.font.SysFont("consolas", 9, True, False)
    # zmienne obsługi gui/rysowania/etc
    clock = pygame.time.Clock()
    fps_counter = FPSCounter(TARGET_FPS)
    gui_done_flag = False
    data_update_flag = True
    drawing_depth_limit = 0
    mouse_range_canvas = None
    mouse_range_screen = None
    point_values_flag = False

    # główna pętla zdarzeń
    while not gui_done_flag:
        fps_counter.tick(time.perf_counter())
        # pętla odbierająca akcje użytkownika
        for event in pygame.event.get():
            # wyjście przyciskiem
            if event.type == pygame.QUIT:
                print('Quit')
                gui_done_flag = True
            # wyjście klawiszem 'ESC'
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                print('Quit')
                gui_done_flag = True
            # zmiana wielokąta klawiszem 's'
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                if event.mod & pygame.KMOD_SHIFT:
                    G.prev_set()
                else:
                    G.next_set()
                vertices = G.point_set
                print(LOG_SPACER)
                # wyświetlenie informacji o przeliczaniu
                screen.fill(CANVAS_FILL_RGB)
                screen.blit(
                    big_font.render(WARNING_STRING, True, FONT_INFO_RGB),
                    (X_OFFSET, Y_OFFSET))
                pygame.display.flip()
                T = do_stuff(vertices, search_range)
                data_update_flag = True
            # zmiana zakresu klawiszem 'r'
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                if event.mod & pygame.KMOD_SHIFT:
                    G.prev_range()
                else:
                    G.next_range()
                search_range = G.range
                print(LOG_SPACER)
                T.search_range(search_range[0], search_range[1])
                data_update_flag = True
            # zmiana poziomu rysowania odcięć
            if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                data_update_flag = True
                drawing_depth_limit += 1
            # zmiana wielkości siatki
            if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                if event.mod & pygame.KMOD_SHIFT:
                    X_SCALAR -= 8
                else:
                    X_SCALAR += 8
                if X_SCALAR > 128:
                    X_SCALAR = 8
                if X_SCALAR < 8:
                    X_SCALAR = 128
                Y_SCALAR = X_SCALAR
                WINDOW_XRANGE = (WINDOW_WIDTH - X_OFFSET) // X_SCALAR
                WINDOW_YRANGE = (WINDOW_HEIGHT - Y_OFFSET) // Y_SCALAR
                data_update_flag = True
            # zaznaczanie myszą
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_RIGHT:
                mouse_range_canvas = [point_to_canvas(event.pos)] * 2
                mouse_range_screen = [event.pos] * 2
            if event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_RIGHT:
                mouse_range_canvas[1] = point_to_canvas(event.pos)
                G.add_range(mouse_range_canvas)
                search_range = G.range
                print(LOG_SPACER)
                T.search_range(search_range[0], search_range[1])
                data_update_flag = True
                mouse_range_canvas = None
                mouse_range_screen = None
            if event.type == pygame.MOUSEMOTION and mouse_range_screen is not None:
                mouse_range_screen[1] = event.pos
            # toggle napisów
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                point_values_flag = not point_values_flag
                data_update_flag = True
            # magic key
            if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                if event.mod & pygame.KMOD_SHIFT:
                    G.generate_point_set(10000, (70, 50), 100, True)
                else:
                    G.generate_point_set(40000, (70, 50), 1000, True, empty=20)
                vertices = G.point_set
                search_range = G.range
                print(LOG_SPACER)
                # wyświetlenie informacji o przeliczaniu
                screen.fill(CANVAS_FILL_RGB)
                screen.blit(
                    big_font.render(WARNING_STRING, True, FONT_INFO_RGB),
                    (X_OFFSET, Y_OFFSET))
                pygame.display.flip()
                T = do_stuff(vertices, search_range)
                data_update_flag = True

        if data_update_flag:
            # przygotowanie rysowanych elementów wykonywane tylko przy wykryciu zmiany
            data_update_flag = False

            if 2 ** drawing_depth_limit > T.size:
                drawing_depth_limit = 0

            # czyszczenie powierzchni
            geometry_image.fill(CANVAS_FILL_RGB)
            screen_image.fill(CANVAS_FILL_RGB)

            # konwersja kształtów na współrzędne okna
            set_points = []
            traversed_points = []
            range_points = []
            for vertex in vertices:
                set_points.append(point_to_screen(vertex))
            for vertex in T.range_points:
                range_points.append(point_to_screen(vertex))
            for vertex in T.traversed_points:
                traversed_points.append(point_to_screen(vertex))
            T_screen = []
            for index in range(T.size):
                T_screen.append(point_to_screen(T[index]))

            # rysowanie - nie ma alphy - ostatni narysowany element przysłania poprzednie
            # osie
            pygame.draw.line(geometry_image, AXIS_RGB, (0, Y_OFFSET), (WINDOW_WIDTH, Y_OFFSET), 1)
            pygame.draw.line(geometry_image, AXIS_RGB, (X_OFFSET, 0), (X_OFFSET, WINDOW_HEIGHT), 1)
            # siatka
            if X_SCALAR >= 8:
                for x_line in range(X_SCALAR, WINDOW_WIDTH // 2, X_SCALAR):
                    pygame.draw.line(geometry_image, GRID_RGB,
                                     (X_OFFSET + x_line, 0),
                                     (X_OFFSET + x_line, WINDOW_HEIGHT), 1)
                    pygame.draw.line(geometry_image, GRID_RGB,
                                     (X_OFFSET - x_line, 0),
                                     (X_OFFSET - x_line, WINDOW_HEIGHT), 1)
                for y_line in range(Y_SCALAR, WINDOW_HEIGHT // 2, Y_SCALAR):
                    pygame.draw.line(geometry_image, GRID_RGB,
                                     (0, Y_OFFSET + y_line),
                                     (WINDOW_WIDTH, Y_OFFSET + y_line), 1)
                    pygame.draw.line(geometry_image, GRID_RGB,
                                     (0, Y_OFFSET - y_line),
                                     (WINDOW_WIDTH, Y_OFFSET - y_line), 1)
            # range search
            if T.range[0] is not None:
                pygame.draw.rect(geometry_image, RANGE_RGB, (
                    x_to_screen(T.range[0][0]),
                    y_to_screen(T.range[0][1]),
                    x_to_screen(T.range[1][0]) - x_to_screen(T.range[0][0]),
                    y_to_screen(T.range[1][1]) - y_to_screen(T.range[0][1])), 0)
            # linie odcięć
            level_bound = 1
            depth = 0
            color = BRANCH_RGB
            # print('Calculating range boundaries')
            while level_bound * 2 - 1 <= T.size:
                next_level_bound = level_bound * 2
                # print('Current depth', depth, 'indexes:', current_bound - 1, next_bound - 1)
                if depth % 2 == 0:
                    # print('Divide X range')
                    for index in range(level_bound - 1, next_level_bound - 1):
                        if T[index] is not None:
                            y_min, y_max = T.find_bounds(index, 1, WINDOW_YRANGE)
                            pygame.draw.line(geometry_image, color,
                                             (T_screen[index][0], y_to_screen(y_min)),
                                             (T_screen[index][0], y_to_screen(y_max)), 3)
                else:
                    # print('Divide Y range')
                    for index in range(level_bound - 1, next_level_bound - 1):
                        if T[index] is not None:
                            x_min, x_max = T.find_bounds(index, 0, WINDOW_XRANGE)
                            pygame.draw.line(geometry_image, color,
                                             (x_to_screen(x_min), T_screen[index][1]),
                                             (x_to_screen(x_max), T_screen[index][1]), 3)
                level_bound = next_level_bound
                depth += 1
                color = (int(color[0] * 1.25), int(color[1] * 0.9), int(color[2] * 0.7))
                if color[0] > 255:
                    color = BRANCH_RGB
                if depth > drawing_depth_limit:
                    break
            # punkty
            pt_size = (2, 1)[len(set_points) > 500]
            draw_points(geometry_image, set_points, POINT_NORMAL_RGB, pt_size - 1)
            draw_points(geometry_image, traversed_points, POINT_TRAVERSED_RGB, pt_size)
            draw_points(geometry_image, range_points, POINT_IN_RANGE_RGB, pt_size)

            # cały wypełniany bufor jest odbity w pionie i załadowany do kolejnego bufora
            screen_image.blit(pygame.transform.flip(geometry_image, False, True), (0, 0))
            # na ten obraz nałożone są współrzędne punktów ...
            if point_values_flag:
                if X_SCALAR <= 16:
                    if X_SCALAR >= 8:
                        for index in range(len(vertices)):
                            screen_image.blit(
                                small_font.render(
                                    "{:.0f},{:.0f}".format(vertices[index][0], vertices[index][1]),
                                    True, FONT_POINT_RGB),
                                (set_points[index][0] - 20,
                                 WINDOW_HEIGHT - 14 - set_points[index][1]))
                else:
                    for index in range(len(vertices)):
                        screen_image.blit(
                            small_font.render(
                                "{:.1f},{:.1f}".format(vertices[index][0], vertices[index][1]),
                                True, FONT_POINT_RGB),
                            (set_points[index][0] - 20,
                             WINDOW_HEIGHT - 14 - set_points[index][1]))
            # ... oraz inne napisy informacyjne
            point_count = len(set_points)
            visited_count = len(traversed_points)
            range_count = len(range_points)
            sqr_boundary = 4 * math.ceil(math.sqrt(point_count)) + range_count
            recurrence_boundary = 4 * approximate_complexity(point_count) + range_count
            data_strings = [
                "Set index: {:d}/{:d}".format(G.point_set_index + 1, G.point_set_count),
                "Range index: {:d}/{:d}".format(G.range_index + 1, G.range_count),
                "Points: {:d}/{:d}/{:d}".format(point_count, visited_count, range_count),
                "Complexity: {:d}/{:d}".format(sqr_boundary, recurrence_boundary)
            ]
            for index in range(1, len(data_strings) + 1):
                screen_image.blit(
                    big_font.render(data_strings[index - 1], True, FONT_INFO_RGB),
                    (TEXT_LEFT_OFFSET, TEXT_VERTICAL_SPACING * index))
            # i instrukcja
            for index in range(1, len(HELP_STRINGS) + 1):
                screen_image.blit(
                    big_font.render(HELP_STRINGS[len(HELP_STRINGS) - index], True, FONT_INFO_RGB),
                    (WINDOW_WIDTH - TEXT_RIGHT_OFFSET,
                     WINDOW_HEIGHT - TEXT_VERTICAL_SPACING * index))

        screen.fill(CANVAS_FILL_RGB)
        # wysłanie przygotowanych danych na ekran
        screen.blit(screen_image, (0, 0))
        if mouse_range_screen is not None:
            pygame.draw.rect(screen, RANGE_MOUSE_RGB, (
                mouse_range_screen[0][0],
                mouse_range_screen[0][1],
                mouse_range_screen[1][0] - mouse_range_screen[0][0],
                mouse_range_screen[1][1] - mouse_range_screen[0][1]), 2)
        # wyświetlenie fps
        screen.blit(
            big_font.render("FPS: {:0.2f}".format(fps_counter.fps), True, FONT_INFO_RGB),
            (TEXT_LEFT_OFFSET, TEXT_VERTICAL_SPACING * 0))
        pygame.display.flip()
        clock.tick(TARGET_FPS)

    # zamknięcie programu
    print('Closing GUI')
    pygame.display.quit()
    print('Exit')
