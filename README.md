# Movement-Tracer
## Opis
Program służy do rysowania ruchem przez kamere. program szuka punktow najbardziej zblizonych do pozadanego koloru i rysuje na nich porzadany kolor.
## Rady
- Zaleca sie wybranie kontrolera o konktetnym kolorze, np. biale swiatlo z komorki przy szukaniu bialego koloru
- Przy ustawianiu kolorow pamietaj, ze przyjmuja one wartosci 0-255 w skalach Blue Green Red
- Aby uruchomic program, nalezy posiadac srodowisko python i uruchomic Tracer.py, badz uruchoomic Tracer.exe w folderze dist
## Sterowanie
- wybrany kontroler ocharakterystycznym kolorze do rysowania
- klawiatura do podawania parametrow
- SPACE = pauza, ustawianie parametrow na konsoli
- WSAD = alternatywne poruszanie sie po palecie
## Dzialanie
- ustalanie poczatkowych parametrow, lub wybranie domyslych
- otwiera sie ekran z obrazem z kamery, na ktorym mozna rysowac. Program najpierw szuka na calym obrazie punktu najbardziej zblizonego kolorem do poszukiwanego, a potem szuka punktow w ustalonej odleglosci od niego
- w kazdym momencie mozna zatrzymac rysowanie, naciskajac pauze. W konsoli mozna zmienic obecne parametry
## Parametry
program posiada klase Paarameters, ktorej wartosci odzialuja na jego dzialanie. Wartosci mozna zmienic przy uruchomieniu progamu, badz w trybie pauzy

- value - szukany kolor
- thickness - grubosc linii
- search_area - rozmiar pola przeszukiwan nowego punktu wokol poprzedniego punktu
- draw_color - kolor rysowania
- max_table_size - dlugosc ile pikseli naraz bedzie pokolorowanych
- tolerance - poziom tolerancji koloru. Im wyzszy, tym wieksza szansa, ze znajdzie pasujacy piksel do koloru. Oznacza to tez zmniejszona stabilnosc
- flipped - tryb lustrzanego obrazu

## Obiekty
- Parameters - klasa z parametrami rysowania
- main - Funkcja ustalajaca parametry wstępne
- config - Funkcja z menu konfiguracji paramertow rysowania
- searchcam - Funkcja z petlą do rysowania. Pobiera współrzędne piksela z poniższych funkcji, dodaje go do listy pikseli z kolorem. Następnie koloruje je i piksele wokół nich na wyznaczony kolor.
- findclosestpix_part - Funkcja znajdująca współrzędne piksela najbardziej zbliżonego do poszukiwanego koloru z częsci obrazka wokół poprzedniego piksela
- findclosestpix_all - Funkcja znajdująca współrzędne piksela najbardziej zbliżonego do poszukiwanego koloru z całego obrazka

## Wykorzystane Technologie
- Python 3.7
- Biblioteka OpenCV
