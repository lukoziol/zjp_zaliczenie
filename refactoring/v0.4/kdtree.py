"""Moduł zawierający obsługę drzew KD."""


class KDTree:
    """Klasa reprezentująca drzewo KD.

    Pozwala budować i wyszukiwać punkty w drzewie.
    """

    # Domyślny poziom debugu - można zmieniac w trakcie używania klasy
    DEBUG_LEVEL = 4

    @staticmethod
    def __logger(level, indent, text):
        """Funkcja usprawniająca logowanie
        Pozwala na wygodniejsze wyświetlanie informacji
        oraz na dynamiczną zmianę poziomu logowania

        :param level: poziom informacji do zalogowania - pozwala na wybiórcze blokowanie danych
        :param indent: poziom wcięcia - pozwala polepszyć logi wizualnie
        :param text: tekst do wyświetlenia
        :return: None
        """

        if level <= KDTree.DEBUG_LEVEL:
            print('{}{}'.format(('  ' * indent), text))

    def __init__(self, points):
        """Inicjalizacja i tworzenie drzewa na podstawie podanych punktów
        Drzewo jest prawidłowo zbalansowane, na każdym poziomie rekurencji
        wybierane są miediany z osi X lub Y
        Złożoność czasowa to O(N log N):
        - na początku sortowanie O(N log N)
        - potem rekurencyjne tworzenie drzewa o log N poziomach, każda operacja
          podziału jest przeprowadzana w czasie liniowym - proporcjonalnym
          do rozmiaru przekazanego poddrzewa
        Złożoność pamięciowa to O(N):
        - 1*N - wejściowa tablica punktów
        - 2*N - tablice posortowane po X i Y
        - w trakcie rekurencji tworzone są sortowane podtablice o łącznej
          wielkości, która nigdy nie przekracza wartości
          2xN (1 + 1/2 + 1/4 + 1/8 -> lim = 2)
        - wynikowa tablica zawierająca drzewo - pesymistyczny przypadek to rozmiar 2*N-1
          rozmiar taki pojawia się w momencie, kiedy ilość punktów = 2^x
          w takim przypadku ostatnie piętro drzewa będzie zawierało tylko 1 liść
          na 2^(x-1) miejsc

        :param points: zbiór punktów, z którego tworzymy kdtree
        """
        self.__logger(0, 0, 'Creating kdtree')
        self.__logger(1, 0, 'Input points: {}'.format(points))
        # sortowanie po X i Y
        xsorted = sorted(points)
        ysorted = sorted(points, key=lambda k: [k[1], k[0]])
        # przygotowanie zmiennych
        self.__size = self.__find_size(len(points))
        self.__tree = [None] * self.__size
        # tworzenie drzewa
        self.__make_split(0, 0, xsorted, ysorted)
        # przygotowanie zmiennych związanych z wyszukiwaniem obszarów
        self.range_points = None
        self.traversed_points = None
        self.range = [None, None]

    @property
    def size(self):
        """Getter prywatnej zmiennej __size

        :return: rozmiar drzewa
        """
        return self.__size

    def __getitem__(self, index):
        """Nadpisanie operatora [] dla klasy KDTree
        Pozwala na wygodny dostęp do elementów drzewa
        bez ryzyka zniszczenia go

        :param index: indeks elementu drzewa
        :return: element drzewa o zadanym indeksie
        """
        return self.__tree[index]

    def __str__(self):
        """Funkcja pomocnicza do sensownego wyświetlania drzewa w konsoli

        :return: opis drzewa w ASCII
        """
        tree_contents = "Tree of size {:d}\n".format(self.__size)
        level_size = 1
        while level_size < self.__size:
            tree_contents += " --> {}\n".format(self.__tree[level_size-1:2*level_size-1])
            level_size *= 2
        return tree_contents

    def __find_size(self, point_count):
        """Obliczenie minimalnej wielkości tablicy dla reprezentacji zbilansowanego kddrzewa

        :param point_count: liczba punktów zbioru, z którego budujemy drzewo
        :return: minimalna, bezpieczna wielkość tablicy, która pomieści punkty
        """
        size = 1
        while size <= point_count:
            size *= 2
        size -= 1
        self.__logger(1, 0, 'Size required: {:d}'.format(size))
        return size

    def __make_split(self, tree_level, index, xsorted, ysorted):
        """Funkcja budująca kolejne elementy drzewa (rekurencyjna)

        :param tree_level: poziom drzewa, na którym się znajdujemy (zagłębienie)
        :param index: indeks węzła w tablicy
        :param xsorted: zbiór punktów posortowanych względem X
        :param ysorted: ten sam zbiór punktów, ale posortowany względem Y
        :return: None
        """
        # przygotowanie zmiennych do wygodnego wyboru osi podziału
        points = (xsorted, ysorted)
        axis = tree_level % 2
        # aktualny rozmiar poddrzewa
        size = len(xsorted)
        if size == 0:
            return
        # obliczenie punktu podziału
        mid = size//2
        mid_point = points[axis][mid]
        # logowanie
        self.__logger(1, tree_level,
                      'Level: {:d} index: {:d} size: {:d}'.format(tree_level, index, size))
        self.__logger(2, tree_level, 'Data: {}'.format(points[axis]))
        # zapisanie punktu podziału
        self.__tree[index] = mid_point
        if size == 1:
            return
        # logowanie (tlyko jeśli faktycznie dzielimy tablice)
        self.__logger(2, tree_level,
                      'Split point at {:d}: {}'.format(mid, mid_point))
        # dzielenie tablic względem aktualnej osi
        primary_lo = points[axis][:mid]
        primary_hi = points[axis][mid+1:]
        # dzielenie tablic względem drugiej osi
        # korzysta z wbudowanego porównywania tuple
        secondary_lo = []
        secondary_hi = []
        for point in points[axis-1]:
            if (point[axis], point[axis-1]) < (mid_point[axis], mid_point[axis-1]):
                secondary_lo.append(point)
            elif (point[axis], point[axis-1]) > (mid_point[axis], mid_point[axis-1]):
                secondary_hi.append(point)
        # aktualizacja głębokości drzewa i indeksu elementów
        tree_level += 1
        index *= 2
        # wykonanie rekurencyjne na nowych podzbiorach danych
        if axis == 0:
            self.__make_split(tree_level, index + 1, primary_lo, secondary_lo)
            self.__make_split(tree_level, index + 2, primary_hi, secondary_hi)
        else:
            self.__make_split(tree_level, index + 1, secondary_lo, primary_lo)
            self.__make_split(tree_level, index + 2, secondary_hi, primary_hi)

    @staticmethod
    def __parent(index):
        """Oblicza indeks rodzica elementu o zadanym indeksie

        :param index: indeks elementu
        :return: indeks rodzica, -1 jeśli poza zakresem
        """
        if index <= 0:
            return -1
        return (index-1)//2

    def find_bounds(self, point_index, axis, axis_max):
        """Funkcja odnajduje ograniczenia zadanego punktu w podanej osi
        Potrzebna do prawidłowego rysowania obszarów zajmowanych przez elementy drzewa

        :param point_index: indeks punkdu, dla którego szukamy ograniczeń
        :param axis: oś, względem której działa wyszukiwanie (0=X, 1=Y)
        :param axis_max: graniczne rozpatrywane wartości (-;+) - optymalizacja rysowania
        :return: krotka składająca się z 2 współrzednych ograniczających dany punkt
        """
        # przygotowanie zmiennych
        result = (-axis_max, axis_max)
        point = self.__tree[point_index]
        parent_index = self.__parent(point_index)
        # flagi znalezionych granic
        min_found = False
        max_found = False
        self.__logger(1, 0, '{} Find {} bounds for {} {} {}'.format(
            '-' * 18, ('Y', 'X')[axis == 0], point, result, '-' * 18,))
        # trawersowanie w górę drzewa dopóki nie spotkamy granic lub roota
        while parent_index > -1 and not (min_found and max_found):
            parent = self.__tree[parent_index]
            self.__logger(2, 0, 'Checking: {}'.format(parent))
            # sprawdzenie współrzędnych
            if (parent[axis], parent[axis-1]) > (point[axis], point[axis-1]):
                if result[1] > parent[axis]:
                    result = (result[0], parent[axis])
                    max_found = True
            if (parent[axis], parent[axis-1]) < (point[axis], point[axis-1]):
                if result[0] < parent[axis]:
                    result = (parent[axis], result[1])
                    min_found = True
            self.__logger(2, 0, 'Updated bounds: {}'.format(result))
            # sprawdzamy tylko co 2-gie piętro (bo szukamy ograniczenia 1 osi)
            parent_index = self.__parent(self.__parent(parent_index))
        self.__logger(1, 0, 'Final bounds: {}'.format(result))
        return result

    def __point_in_range(self, point):
        """Sprawdza czy punkt znajduje się w przeszukiwanym obszarze
        Przeszukiwany obszar jest zapisany w klasie jako zmienna 'range'

        :param point: sprawdzany punkt
        :return: True jeślie punkt nalezy do obszaru, w przeciwnym razie False
        """
        in_range = False
        if self.range[0][0] <= point[0] <= self.range[1][0] \
                and self.range[0][1] <= point[1] <= self.range[1][1]:
            in_range = True
        self.__logger(5, 0, 'Point {} is{} in range {}'.format(
            point, (' not', '')[in_range], self.range))
        return in_range

    def __search_range_recursive(self, point_index, depth):
        """Rekurencyjne przeszukiwanie zadanego obszaru
        Obszar jest zapisany w zmiennej 'range'
        Punkty obszaru są zachowane w zmiennej 'range_points'

        :param point_index: indeks sprawdzanego elementu
        :param depth: poziom drzewa, na którym się znajdujemy
        :return: None
        """
        # sprawdzenie, czy znajdujemy się w prawidłowym węźle
        if point_index >= self.__size:
            return
        point = self.__tree[point_index]
        if point is None:
            return
        # dodanie węzła do zbioru odwiedzonych
        self.traversed_points.append(point)
        # znacznik osi (0 = X, 1 = Y)
        axis = depth % 2
        if point[axis] < self.range[0][axis]:
            self.__logger(3, depth, 'Point {} is smaller than {}'.format(point, self.range[0]))
            # jeżeli punkt jest niżej w rozważanym wymiarze - idź w prawo (w większe wartości)
            self.__search_range_recursive(point_index*2+2, depth+1)
        elif point[axis] > self.range[1][axis]:
            self.__logger(3, depth, 'Point {} is bigger than {}'.format(point, self.range[1]))
            # jeżeli punkt jest wyżej w rozważanym wymiarze - idź w lewo (w mniejsze wartości)
            self.__search_range_recursive(point_index*2+1, depth+1)
        else:
            self.__logger(
                3,
                depth,
                'Point {} X is in {}'.format(point, (self.range[0][axis], self.range[1][axis])))
            # punkt zawiera się w rozważanym wymiarze, sprawdź czy zawiera się w przedziale
            if self.__point_in_range(point):
                # jesli tak, to dodaj go do zbioru znalezionych punktów
                self.__logger(4, depth, 'Point valid')
                self.range_points.append(point)
            # i odzwiedź jego oba poddrzewa
            self.__search_range_recursive(point_index*2+1, depth+1)
            self.__search_range_recursive(point_index*2+2, depth+1)

    def search_range(self, bottom_left, top_right):
        """Funkcja uruchamiająca wyszukiwanie punktów należących do zadanego przedziału

        :param bottom_left: lewy dolny róg przedziału
        :param top_right: prawy górny róg przedziału
        :return: punkty należące do przedziału
        """
        self.__logger(0, 0, 'Range search in: [{} {}]'.format(bottom_left, top_right))
        # przygotowanie zmiennych
        self.range_points = []
        self.traversed_points = []
        self.range = [bottom_left, top_right]
        # uruchomienie wyszukiwania
        self.__search_range_recursive(0, 0)
        # funkcja zwraca znalezione punkty, można je również odczytać później bezpośrednio z klasy
        return self.range_points

if __name__ == "__main__":
    print('TEST')
    T = KDTree([(0,0), (1,1), (2,2), (3,3), (4,4), (5,5), (6,6)])
    print(T)
    print('Points in range:', T.search_range((2,2), (4,4)))
    input()
    print('--------------------Przykład nr 1--------------------')
    T = KDTree([(0, 3), (1, 3), (2, 3), (3, 3), (0, 2), (3, 2), (0, 1), (3, 1), (0, 0), (1, 0), (2, 0), (3, 0)])
    print(T)
    print('Points in range:', T.search_range((0, 0), (4, 3)))
    input()
    print('--------------------Przykład nr 2--------------------')
    print('Points in range:', T.search_range((1, 0), (2, 4)))
    input()
    print('--------------------Przykład nr 3--------------------')
    print('Points in range:', T.search_range((1, 1), (2, 2)))
    input()
    print('--------------------Przykład nr 4--------------------')
    print('Points in range:', T.search_range((0, 0), (4, 0)))
    input()
    print('--------------------Przykład nr 5--------------------')
    print('Points in range:', T.search_range((1, 1), (1, 1)))
    input()
    print('--------------------Przykład nr 6--------------------')
    print('Points in range:', T.search_range((0, 1), (0, 1)))
    input()
