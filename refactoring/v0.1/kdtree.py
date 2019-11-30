
def make_tree(points):
    global size
    global T
    
    xsorted = sorted(points)
    ysorted = sorted(points, key=lambda k: [k[1], k[0]])
    # przygotowanie zmiennych
    size = 1
    while size <= len(xsorted):
        size *= 2
    size -= 1
    print('Size required: {:d}'.format(size))
    T = [None] * size
    # tworzenie drzewa
    make_x_split(0, 0, xsorted, ysorted)


def make_x_split(tree_level, index, xsorted, ysorted):
    # Funkcja budująca kolejne elementy drzewa (rekurencyjna)
    global T
    global size
    
    # aktualny rozmiar poddrzewa
    s = len(xsorted)
    if s == 0:
        return
    # obliczenie punktu podziału dla osi X
    mid = s//2
    mid_point = xsorted[mid]
    # logowanie
    print((' ' * tree_level), 'Level: {:d} index: {:d} size: {:d}'.format(tree_level, index, s))
    print((' ' * tree_level), 'Data: {}'.format(xsorted))
    # zapisanie punktu podziału
    T[index] = mid_point
    if s == 1:
        return
    # logowanie (tlyko jeśli faktycznie dzielimy tablice)
    print((' ' * tree_level), 'Split point at {:d}: {}'.format(mid, mid_point))
    # dzielenie tablic względem aktualnej osi
    x_lo = xsorted[:mid]
    x_hi = xsorted[mid+1:]
    # dzielenie tablic względem drugiej osi
    # korzysta z wbudowanego porównywania tuple
    y_lo = []
    y_hi = []
    for point in ysorted:
        if point < mid_point:
            y_lo.append(point)
        elif point > mid_point:
            y_hi.append(point)
    # aktualizacja głębokości drzewa i indeksu elementów
    tree_level += 1
    index *= 2
    # wykonanie rekurencyjne na nowych podzbiorach danych
    make_y_split(tree_level, index + 1, x_lo, y_lo)
    make_y_split(tree_level, index + 2, x_hi, y_hi)


def make_y_split(tree_level, index, xsorted, ysorted):
    # Funkcja budująca kolejne elementy drzewa (rekurencyjna)
    global T
    global size
    
    # aktualny rozmiar poddrzewa
    s = len(xsorted)
    if s == 0:
        return    
    # obliczenie punktu podziału dla osi Y
    mid = s//2
    mid_point = ysorted[mid]
    # logowanie
    print((' ' * tree_level), 'Level: {:d} index: {:d} size: {:d}'.format(tree_level, index, s))
    print((' ' * tree_level), 'Data: {}'.format(ysorted))
    # zapisanie punktu podziału
    T[index] = mid_point
    if size == 1:
        return
    # logowanie (tlyko jeśli faktycznie dzielimy tablice)
    print((' ' * tree_level), 'Split point at {:d}: {}'.format(mid, mid_point))
    # dzielenie tablic względem aktualnej osi
    y_lo = ysorted[:mid]
    y_hi = ysorted[mid+1:]
    # dzielenie tablic względem drugiej osi
    # korzysta z wbudowanego porównywania tuple
    x_lo = []
    x_hi = []
    for point in xsorted:
        if (point[1], point[0]) < (mid_point[1], mid_point[0]):
            x_lo.append(point)
        elif (point[1], point[0]) > (mid_point[1], mid_point[0]):
            x_hi.append(point)
    # aktualizacja głębokości drzewa i indeksu elementów
    tree_level += 1
    index *= 2
    # wykonanie rekurencyjne na nowych podzbiorach danych
    make_x_split(tree_level, index + 1, x_lo, y_lo)
    make_x_split(tree_level, index + 2, x_hi, y_hi)


def search_x_range(tree_level, index):
    # Rekurencyjne przeszukiwanie zadanego obszaru
    global T
    global size
    global range_points
    global traversed_points
    global search_range
    
    # sprawdzenie, czy znajdujemy się w prawidłowym węźle
    if index >= size:
        return
    point = T[index]
    if point is None:
        return
    # dodanie węzła do zbioru odwiedzonych
    traversed_points.append(point)
    # rozważamy oś X
    if point[0] < search_range[0][0]:
        print((' ' * tree_level), 'Point {} is smaller than {}'.format(point, search_range[0]))
        # jeżeli punkt jest niżej w rozważanym wymiarze - idź w prawo (w większe wartości)
        search_y_range(tree_level+1, index*2+2)
    elif point[0] > search_range[1][0]:
        print((' ' * tree_level), 'Point {} is bigger than {}'.format(point, search_range[1]))
        # jeżeli punkt jest wyżej w rozważanym wymiarze - idź w lewo (w mniejsze wartości)
        search_y_range(tree_level+1, index*2+1)
    else:
        print((' ' * tree_level), 'Point {} X is in {}'.format(point, (search_range[0][0], search_range[1][0])))
        # punkt zawiera się w rozważanym wymiarze, sprawdź czy zawiera się w przedziale
        if search_range[0][0] <= point[0] <= search_range[1][0] and search_range[0][1] <= point[1] <= search_range[1][1]:
            # jesli tak, to dodaj go do zbioru znalezionych punktów
            print((' ' * tree_level), 'Point in range')
            range_points.append(point)
        # i odzwiedź jego oba poddrzewa
        search_y_range(tree_level+1, index*2+1)
        search_y_range(tree_level+1, index*2+2)

def search_y_range(tree_level, index):
    # Rekurencyjne przeszukiwanie zadanego obszaru
    global T
    global size
    global range_points
    global traversed_points
    global search_range
    
    # sprawdzenie, czy znajdujemy się w prawidłowym węźle
    if index >= size:
        return
    point = T[index]
    if point is None:
        return
    # dodanie węzła do zbioru odwiedzonych
    traversed_points.append(point)
    # rozważamy oś Y            
    if point[1] < search_range[0][1]:
        print((' ' * tree_level), 'Point {} is smaller than {}'.format(point, search_range[0]))
        # jeżeli punkt jest niżej w rozważanym wymiarze - idź w prawo (w większe wartości)
        search_x_range(tree_level+1, index*2+2)
    elif point[1] > search_range[1][1]:
        print((' ' * tree_level), 'Point {} is bigger than {}'.format(point, search_range[1]))
        # jeżeli punkt jest wyżej w rozważanym wymiarze - idź w lewo (w mniejsze wartości)
        search_x_range(tree_level+1, index*2+1)
    else:
        print((' ' * tree_level), 'Point {} Y is in {}'.format(point, (search_range[0][1], search_range[1][1])))
        # punkt zawiera się w rozważanym wymiarze, sprawdź czy zawiera się w przedziale
        if search_range[0][0] <= point[0] <= search_range[1][0] and search_range[0][1] <= point[1] <= search_range[1][1]:
            # jesli tak, to dodaj go do zbioru znalezionych punktów
            print((' ' * tree_level), 'Point in range')
            range_points.append(point)
        # i odzwiedź jego oba poddrzewa
        search_x_range(tree_level+1, index*2+1)
        search_x_range(tree_level+1, index*2+2)


def search():
    # Funkcja uruchamiająca wyszukiwanie punktów należących do zadanego przedziału
    global range_points
    global traversed_points
    global search_range
    
    print('Range search in: {}'.format(search_range))
    # przygotowanie zmiennych
    range_points = []
    traversed_points = []
    # uruchomienie wyszukiwania
    search_x_range(0, 0)
    # funkcja zwraca znalezione punkty, można je również odczytać później bezpośrednio z klasy
    return range_points






T = []
size = 0
range_points = None
traversed_points = None
search_range = [None, None]



print('TEST')
points = [(0,0), (1,1), (2,2), (3,3), (4,4), (5,5), (6,6)]
make_tree(points)
print('Drzewo:', T)
search_range = [(2,2), (4,4)]
print('Points in range:', search())
input()
print('--------------------Przykład nr 1--------------------')
points = [(0, 3), (1, 3), (2, 3), (3, 3), (0, 2), (3, 2), (0, 1), (3, 1), (0, 0), (1, 0), (2, 0), (3, 0)]
make_tree(points)
print('Drzewo:', T)
search_range = [(0, 0), (4, 3)]
print('Points in range:', search())
input()
print('--------------------Przykład nr 2--------------------')
search_range = [(1, 0), (2, 4)]
print('Points in range:', search())
input()
print('--------------------Przykład nr 3--------------------')
search_range = [(1, 1), (2, 2)]
print('Points in range:', search())
input()
print('--------------------Przykład nr 4--------------------')
search_range = [(0, 0), (4, 0)]
print('Points in range:', search())
input()
print('--------------------Przykład nr 5--------------------')
search_range = [(1, 1), (1, 1)]
print('Points in range:', search())
input()
print('--------------------Przykład nr 6--------------------')
search_range = [(0, 1), (0, 1)]
print('Points in range:', search())
input()
    
    
