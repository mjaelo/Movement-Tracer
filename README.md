# Movement-Tracer
## Opis
Program służy do rysowania ruchem przez kamerę kmputera. Program szuka punktow najbardziej zbliżonych do pożądanego koloru i rysuje na nich wybranym kolorem.
## Rady
- Zaleca sie wybranie kontrolera o konkretnym kolorze, np. biale swiatlo z komorki przy szukaniu bialego koloru
- Przy ustawianiu kolorow pamietaj, ze przyjmuja one wartosci 0-255 w skalach Blue Green Red
- Aby uruchomic program, nalezy posiadac srodowisko python i uruchomic Tracer.py, badz uruchoomic Tracer.exe w folderze dist
## Sterowanie
- wybrany kontroler o charakterystycznym kolorze do rysowania, aby program mógł śledzić jego ruch
- klawiatura do podawania parametrow w trybie pauzy, bądz przy uruchomieniu programu.
- SPACE = pauza, ustawianie parametrow na konsoli
- WSAD = alternatywne poruszanie sie po palecie
## Działanie
- Ustalanie poczatkowych parametrow, lub wybranie domyslych
- Otworzenie ekranu z obrazem z kamery, na którym można rysować. Program najpierw szuka na calym obrazie punktu najbardziej zblizonego kolorem do poszukiwanego, a potem szuka punktow w ustalonej odleglosci od niego.
- W kazdym momencie mozna zatrzymac rysowanie, naciskajac pauze. W konsoli mozna zmienic obecne parametry
- Kolor rysowania można zmienić wchodząc w ustawienia, bądź najeżdżając kursorem na kolorowe prostokąty na górze ekranu
- Aby usunąć swój rysunek, należy najechać na skrzynkę "clear all" po lewej górnej części ekranu
## Parametry
program posiada klase Paarameters, ktorej wartosci odzialuja na jego dzialanie. Wartosci mozna zmienic przy uruchomieniu progamu, badz w trybie pauzy

- value - szukany kolor
- thickness - grubosc linii
- search_area - rozmiar pola przeszukiwan nowego punktu wokol poprzedniego punktu
- draw_color - kolor rysowania
- max_table_size - dlugosc ile pikseli naraz bedzie pokolorowanych
- tolerance - poziom tolerancji koloru. Im wyzszy, tym wieksza szansa, ze znajdzie pasujacy piksel do koloru. Oznacza to tez zmniejszona stabilnosc
- flipped - tryb lustrzanego obrazu. przy podaniu enter przyjmuje wartosc False, w przeciwnym wypadku True.

## Obiekty
- Parameters - klasa z parametrami rysowania
- main - Funkcja ustalajaca parametry wstępne
- config - Funkcja z menu konfiguracji paramertow rysowania
- searchcam - Funkcja z petlą do rysowania. Pobiera współrzędne piksela z poniższych funkcji, dodaje go do listy pikseli z kolorem. Następnie koloruje je i piksele wokół nich na wyznaczony kolor.
- findclosestpix_part - Funkcja znajdująca współrzędne piksela najbardziej zbliżonego do poszukiwanego koloru z częsci obrazka wokół poprzedniego piksela. Szybsza, ale zawodniejsza. Używana w standardowym poszukiwaniu piksela.
- findclosestpix_all - Funkcja znajdująca współrzędne piksela najbardziej zbliżonego do poszukiwanego koloru z całego obrazka. Wolniejsza, ale powoduje mniej błędów. Urzywana na starcie gry i w przypadku pojawienia się błędu

## Wykorzystane Technologie
- Python 3.7
- Biblioteka OpenCV
