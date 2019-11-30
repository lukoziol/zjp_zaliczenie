
class KDTree:
    
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
        print('Creating kdtree')
        print('Input points: {}'.format(points))
        # sortowanie po X i Y
        xsorted = sorted(points)
        ysorted = sorted(points, key=lambda k: [k[1], k[0]])
        # przygotowanie zmiennych
        self.size = self.find_size(len(points))
        self.tree = [None] * self.size
        # tworzenie drzewa
        self.make_split(0, 0, xsorted, ysorted)
        # przygotowanie zmiennych związanych z wyszukiwaniem obszarów
        self.range_points = None
        self.traversed_points = None
        self.range = [None, None]


    def __str__(self):
        # Funkcja pomocnicza do sensownego wyświetlania drzewa w konsoli
        tree_contents = "Tree of size {:d}\n".format(self.size)
        level_size = 1
        while level_size < self.size:
            tree_contents += " --> {}\n".format(self.tree[level_size-1:2*level_size-1])
            level_size *= 2
        return tree_contents


    def find_size(self, point_count):
        # Obliczenie minimalnej wielkości tablicy dla reprezentacji zbilansowanego kddrzewa
        size = 1
        while size <= point_count:
            size *= 2
        size -= 1
        print('Size required: {:d}'.format(size))
        return size


    def make_split(self, tree_level, index, xsorted, ysorted):
        """Funkcja budująca kolejne elementy drzewa (rekurencyjna)

        :param tree_level: poziom drzewa, na którym się znajdujemy (zagłębienie)
        :param index: indeks węzła w tablicy
        :param xsorted: zbiór punktów posortowanych względem X
        :param ysorted: ten sam zbiór punktów, ale posortowany względem Y
        :return: None
        """
        
        # aktualny rozmiar poddrzewa
        size = len(xsorted)
        if size == 0:
            return
        if tree_level % 2 == 0:
            # obliczenie punktu podziału dla osi X
            mid = size//2
            mid_point = xsorted[mid]
            # logowanie
            print((' ' * tree_level), 'Level: {:d} index: {:d} size: {:d}'.format(tree_level, index, size))
            print((' ' * tree_level), 'Data: {}'.format(xsorted))
            # zapisanie punktu podziału
            self.tree[index] = mid_point
            if size == 1:
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
        else:
            # obliczenie punktu podziału dla osi Y
            mid = size//2
            mid_point = ysorted[mid]
            # logowanie
            print((' ' * tree_level), 'Level: {:d} index: {:d} size: {:d}'.format(tree_level, index, size))
            print((' ' * tree_level), 'Data: {}'.format(ysorted))
            # zapisanie punktu podziału
            self.tree[index] = mid_point
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
        self.make_split(tree_level, index + 1, x_lo, y_lo)
        self.make_split(tree_level, index + 2, x_hi, y_hi)


    def search_range_recursive(self, tree_level, index):
        """Rekurencyjne przeszukiwanie zadanego obszaru
        Obszar jest zapisany w zmiennej 'range'
        Punkty obszaru są zachowane w zmiennej 'range_points'

        :param tree_level: indeks sprawdzanego elementu
        :param index: poziom drzewa, na którym się znajdujemy
        :return: None
        """
        # sprawdzenie, czy znajdujemy się w prawidłowym węźle
        if index >= self.size:
            return
        point = self.tree[index]
        if point is None:
            return
        # dodanie węzła do zbioru odwiedzonych
        self.traversed_points.append(point)
        if tree_level % 2 == 0:
            # rozważamy oś X
            if point[0] < self.range[0][0]:
                print((' ' * tree_level), 'Point {} is smaller than {}'.format(point, self.range[0]))
                # jeżeli punkt jest niżej w rozważanym wymiarze - idź w prawo (w większe wartości)
                self.search_range_recursive(tree_level+1, index*2+2)
            elif point[0] > self.range[1][0]:
                print((' ' * tree_level), 'Point {} is bigger than {}'.format(point, self.range[1]))
                # jeżeli punkt jest wyżej w rozważanym wymiarze - idź w lewo (w mniejsze wartości)
                self.search_range_recursive(tree_level+1, index*2+1)
            else:
                print((' ' * tree_level), 'Point {} X is in {}'.format(point, (self.range[0][0], self.range[1][0])))
                # punkt zawiera się w rozważanym wymiarze, sprawdź czy zawiera się w przedziale
                if self.range[0][0] <= point[0] <= self.range[1][0] and self.range[0][1] <= point[1] <= self.range[1][1]:
                    # jesli tak, to dodaj go do zbioru znalezionych punktów
                    print((' ' * tree_level), 'Point in range')
                    self.range_points.append(point)
                # i odzwiedź jego oba poddrzewa
                self.search_range_recursive(tree_level+1, index*2+1)
                self.search_range_recursive(tree_level+1, index*2+2)
        else:
            # rozważamy oś Y            
            if point[1] < self.range[0][1]:
                print((' ' * tree_level), 'Point {} is smaller than {}'.format(point, self.range[0]))
                # jeżeli punkt jest niżej w rozważanym wymiarze - idź w prawo (w większe wartości)
                self.search_range_recursive(tree_level+1, index*2+2)
            elif point[1] > self.range[1][1]:
                print((' ' * tree_level), 'Point {} is bigger than {}'.format(point, self.range[1]))
                # jeżeli punkt jest wyżej w rozważanym wymiarze - idź w lewo (w mniejsze wartości)
                self.search_range_recursive(tree_level+1, index*2+1)
            else:
                print((' ' * tree_level), 'Point {} Y is in {}'.format(point, (self.range[0][1], self.range[1][1])))
                # punkt zawiera się w rozważanym wymiarze, sprawdź czy zawiera się w przedziale
                if self.range[0][0] <= point[0] <= self.range[1][0] and self.range[0][1] <= point[1] <= self.range[1][1]:
                    # jesli tak, to dodaj go do zbioru znalezionych punktów
                    print((' ' * tree_level), 'Point in range')
                    self.range_points.append(point)
                # i odzwiedź jego oba poddrzewa
                self.search_range_recursive(tree_level+1, index*2+1)
                self.search_range_recursive(tree_level+1, index*2+2)


    def search_range(self, bottom_left, top_right):
        #Funkcja uruchamiająca wyszukiwanie punktów należących do zadanego przedziału
        print('Range search in: [{} {}]'.format(bottom_left, top_right))
        # przygotowanie zmiennych
        self.range_points = []
        self.traversed_points = []
        self.range = [bottom_left, top_right]
        # uruchomienie wyszukiwania
        self.search_range_recursive(0, 0)
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


    
    
