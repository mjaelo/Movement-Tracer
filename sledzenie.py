import cv2
import os

#uwagi:
# interfejs graficzny powinien miec: pola do zmiany wartosci parametrow, guzik on/off gumki, guzik wyjscie

# mogę zmienic funkcje szukania koloru, by  miała tablice rozmiaru obrazka i kolorowanie by zapelnialo pola tego obrazka, oszczedzilo by to pamiec,
# ale i tak usuwam najstarsze pola, a tak, to bym dal jakis klor nieuzywany, by oznaczyc pola puste. Wtedy te nie byloby usuwania starych pol

class Parameters:
    value = [255, 255, 255] # szukany kolor
    thickness = 10
    search_area = [100, 100]
    draw_color = [255, 255, 255] # kolor rysowania
    max_table_size = 100 #dlugosc ile pikseli naraz bedzie pokolorowanych

# dziala, prostrze, ale muli, bo patrzy na caly obrazek
def findclosestpix_all(value, img):
    min_avg = 100000  # min roznica wartosci koloru do poszukiwanego
    min_xy = [0, 0] # wspolrzedne min_avg

    for row_nr in range(len(img)):
        row = img[row_nr]
        for pixel_nr in range(len(row)):
            pixel = row[pixel_nr]
            #szukanie sredniej ze wszystkich 3 pól kolorow pixela
            avg = 0
            for RGB in range(len(pixel)):
                temp = pixel[RGB] - value[RGB] # roznica koloru pixela i poszukiwanego
                avg += temp * temp #zapewnienie ze roznica jest >0

            if (avg < min_avg):
                min_avg = avg
                min_xy = [row_nr, pixel_nr]
    return min_xy


errors = 0 #ilosc bledow przy szukaniu. po 5 z rzedu, wskakuje do findclosestpix_all. Może zrobie, ze zawsze tam wchdzi przy bledzie

# srednio dziala, jest szybszy, bo patrzy tylko na czesc obrazka
# value= poszukiwany kolor, img= obraz, center_xy= xy ostatniego matchu, area = ilosc przeszukiwanych pixeli wokol pix
def findclosestpix_part(value, img, center_xy, area):
    global errors
    min_avg = 100000  # min roznica wartosci koloru do poszukiwanego
    min_xy = [0, 0]  # wspolrzedne min_avg
    pozX = 0
    pozY = 0
    try:
        #przeszukiwanie czesci tablicy wokol center_xy
        for row_nr in range(area[0]):
            pozY = row_nr + center_xy[0]
            pozY = pozY - (area[0] / 2)
            # zabespieczenie Y by nie wychodzilo za plansze
            if pozY > len(img):
                pozY = center_xy[0] - row_nr
            if pozY < 10:
                pozY = 10

            row = img[int(pozY)]

            for pixel_nr in range(area[1]):

                pozX = pixel_nr + center_xy[1]
                pozX = pozX - (area[1] / 2)#by center byl w srodku pola poszukiwania, nie w gornym lewym rogu. moze przeniose to pozniej, nwm
                # zabespieczenie X by bylo w planszy
                if pozX > len(img[0]):
                    pozX = center_xy[1] - pixel_nr
                if pozX < 10:
                    pozX = 10

                pixel = row[int(pozX)]
                # szukanie sredniej ze wszystkich 3 pól kolorow pixela
                avg = 0
                for RGB in range(len(pixel)):
                    temp = pixel[RGB] - value[RGB]  # roznica koloru pixela i poszukiwanego
                    avg += temp * temp  # zapewnienie ze roznica jest >0

                if (avg < min_avg):
                    min_avg = avg
                    min_xy = [pozX, pozY]
        errors = 0
    except:
        errors += 1
        print("["+str(pozX)+","+str(pozY)+"] searching error nr." + str(errors))
        if errors > 5:
            errors = 0
            min_xy = findclosestpix_all(value, img)
            print("fixed")
    return min_xy

#organizowanie znalezionych pikseli do pokolorowania
def searchcam(param):
    is_on = True
    max_xy_tab = []

    cap = cv2.VideoCapture(0)
    ret, img = cap.read()  # pierwsza klatka w img
    print("wymiary obrazu: ", len(img), len(img[0]))

    latest_match = findclosestpix_all(param.value, img)
    max_xy_tab.append([latest_match,param.draw_color])  # znalezienie najblizszego matchu na calym obrazie w pierwszej klatce

    while (is_on == True):
        # zczytanie klatek kamery do obrazu
        ret, img = cap.read()
        key = cv2.waitKey(30)

        # dodanie lokacji najlepszego matchu do tablicy
        latest_match2 = findclosestpix_part(param.value, img, latest_match, param.search_area)
        latest_match = [(latest_match[0] + latest_match2[0]) / 2,
                        (latest_match[1] + latest_match2[
                            1]) / 2]  # strednia starego i nowego punktu, by ograniczyc wariactwa
        max_xy_tab.append([latest_match,param.draw_color])
        if len(max_xy_tab) > param.max_table_size:
            max_xy_tab.remove(max_xy_tab[0])


        # rysowanie w zapisanych lokacjach
        if param.thickness > 1:
            for point in max_xy_tab:
                for i in range(param.thickness):
                    for j in range(param.thickness):
                        if 0 < point[0][0] + i < len(img) and 0 < point[0][1] + i < len(
                                img[1]):
                            try:
                                # obecny punkt jako przeciwienstwo zwyklego koloru
                                if (point == max_xy_tab[len(max_xy_tab) - 1]):

                                    img[int(point[0][0]) + i][int(point[0][1]) + j] = [255 - param.draw_color[0],
                                                                                 255 - param.draw_color[1],
                                                                                 255 - param.draw_color[2]]
                                else:
                                    img[int(point[0][0]) + i][int(point[0][1]) + j] = point[1]
                            except:
                                print("coloring error")
                                ok = "ok"
        cv2.imshow('teraz', img)
    cap.release()
    cv2.destroyAllWindows()



if __name__ == "__main__":
    # >pyinstaller -F plik.py    //do exe
    param=Parameters()

    choice = int(input(
        "0 = domyslne parametry, " + "1 = podaj kolor i grubosc, " + "2 = podaj dokladne parametry"))

    if choice == 1:
        print("podaj wartosci RGB porzadanego koloru ")
        param.value[0] = int(input("B "))
        param.value[1] = int(input("G "))
        param.value[2] = int(input("R "))

        param.thickness = int(input("podaj grubosc linii "))

    if choice == 2:
        param.thickness = int(input("podaj grubosc linii "))
        param.max_table_size = int(input("podaj ilosc pixeli do rysowania"))

        print("podaj wartosci RGB porzadanego koloru ")
        param.value[0] = int(input("B "))
        param.value[1] = int(input("G "))
        param.value[2] = int(input("R "))

        print("podaj wartosci RGB koloru rysowania ")
        param.draw_color[0] = int(input("B "))
        param.draw_color[1] = int(input("G "))
        param.draw_color[2] = int(input("R "))

        print("podaj rozmiar pola przeszukiwan")
        param.search_area[0] = int(input("X "))
        param.search_area[1] = int(input("Y "))

    searchcam(param)
    # searchcam([0, 0, 255], 20)
