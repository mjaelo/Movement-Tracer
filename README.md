# Movement-Tracer
## opis
Program służy do rysowania ruchem przez kamere. program szuka punktow najbardziej zblizonych do pozadanego koloru i rysuje na nich porzadany kolor.
## rady
- Zaleca sie wybranie kontrolera o konktetnym kolorze, np. biale swiatlo z komorki przy szukaniu bialego koloru
- Przy ustawianiu kolorow pamietaj, ze przyjmuja one wartosci 0-255 w skalach Blue Green Red
## sterowanie
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
- tolerance - poziom tolerancji koloru
- flipped - tryb lustrzanego obrazu
