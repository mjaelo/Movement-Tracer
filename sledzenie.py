import sys

import cv2
import threading

# uwagi:
# interfejs graficzny powinien miec: pola do zmiany wartosci parametrow, guzik on/off gumki, guzik wyjscie

# mogę zmienic funkcje szukania koloru, by  miała tablice rozmiaru obrazka i kolorowanie by zapelnialo pola tego obrazka, oszczedzilo by to pamiec,
# ale i tak usuwam najstarsze pola, a tak, to bym dal jakis klor nieuzywany, by oznaczyc pola puste. Wtedy tez nie byloby usuwania starych pol


class Parameters:
    value = [255, 255, 255]  # szukany kolor
    thickness = 10
    search_area = [50, 50]
    draw_color = [0, 0, 255]  # kolor rysowania
    max_table_size = 500  # dlugosc ile pikseli naraz bedzie pokolorowanych
    tolerance=6000
    flipped=True


# dziala, prostrze, ale muli, bo patrzy na caly obrazek
def findclosestpix_all(value, img):
    min_avg = 100000  # min roznica wartosci koloru do poszukiwanego
    min_xy = [100, 100]  # wspolrzedne min_avg

    for row_nr in range(len(img)):
        row = img[row_nr]
        for pixel_nr in range(len(row)):
            pixel = row[pixel_nr]
            # szukanie sredniej ze wszystkich 3 pól kolorow pixela
            avg = 0
            for RGB in range(len(pixel)):
                temp = pixel[RGB] - value[RGB]  # roznica koloru pixela i poszukiwanego
                avg += temp * temp  # zapewnienie ze roznica jest >0

            if (avg < min_avg):
                min_avg = avg
                min_xy = [row_nr, pixel_nr]
    return min_xy


# srednio dziala, jest szybszy, bo patrzy tylko na czesc obrazka
# value= poszukiwany kolor, img= obraz, center_xy= xy ostatniego matchu, area = ilosc przeszukiwanych pixeli wokol pix
def findclosestpix_part(value, img, center_xy, area):
    min_avg = 100000  # min roznica wartosci koloru do poszukiwanego
    min_xy = [0, 0]  # wspolrzedne min_avg
    pozX = 0
    pozY = 0
    try:
        # przeszukiwanie czesci tablicy wokol center_xy
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
                # by center byl w srodku pola poszukiwania, nie w gornym lewym rogu.
                pozX = pozX - (area[1] / 2)
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
    except:
        print("[" + str(pozX) + "," + str(pozY) + "] searching error ")
        min_xy = findclosestpix_all(value, img)

    if min_avg>param.tolerance:
        min_xy=center_xy
    return min_xy


# organizowanie znalezionych pikseli do pokolorowania
def searchcam(param):
    is_on = True
    max_xy_tab = []
    pause=pause2=False

    cap = cv2.VideoCapture(0)
    ret, img = cap.read()  # pierwsza klatka w img

    size=[len(img),len(img[0])]
    print("\nwymiary obrazu: ", size[0],size[1] )

    #flip image, by nie yl lustrzany
    if param.flipped==True:
        img2=img
        for row in range(int(size[0]/2)):
            img[row]=img2[size[0]-1-row]

    latest_match = findclosestpix_all(param.value, img)
    max_xy_tab.append(
        [latest_match, param.draw_color])  # znalezienie najblizszego matchu na calym obrazie w pierwszej klatce

    while (is_on == True):
        # zczytanie klatek kamery do obrazu
        ret, img = cap.read()
        key = cv2.waitKey(30)

        #ustawienia
        if key==32:
            pause=True
        if pause2==True:
            config(param)
            pause2=False

        # dodanie lokacji najlepszego matchu do tablicy
        latest_match2 = findclosestpix_part(param.value, img, latest_match, param.search_area)
        # strednia starego i nowego punktu, by ograniczyc wariactwa
        latest_match = [int((latest_match[0] + latest_match2[0]) / 2),int((latest_match[1] + latest_match2[1]) / 2)]

        #pola zmiany koloru
        colors = [(122, 122, 122),(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
        img = cv2.rectangle(img, (40, 1), (140, 65), colors[0], -1)
        img = cv2.rectangle(img, (160, 1), (255, 65), colors[1], -1)
        img = cv2.rectangle(img, (275, 1), (370, 65), colors[2], -1)
        img = cv2.rectangle(img, (390, 1), (485, 65), colors[3], -1)
        img = cv2.rectangle(img, (505, 1), (600, 65), colors[4], -1)
        cv2.putText(img, "CLEAR ALL", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(img, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(img, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(img, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(img, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150, 150, 150), 2, cv2.LINE_AA)

        for i in range(len(colors)):
            temp=img[int(latest_match[0]),int(latest_match[1])]
            temp2=colors[i]
            if (temp == temp2).all():
                if i == 0:
                    max_xy_tab.clear()
                else:
                    temp=[int(colors[i][0]),int(colors[i][1]),int(colors[i][2])]
                    param.draw_color= temp

        #poruszanie sie klawiszami
        latest_temp = latest_match.copy()
        if(key==100):
            latest_temp[1] += 25#d
        if (key == 119):
            latest_temp[0] -= 25#w
        if (key == 97):
            latest_temp[1] -= 25#a
        if (key == 115):
            latest_temp[0] += 25#s
        if 0 < latest_temp[0] < size[0]-25 and 0 < latest_temp[1] < size[1]-25:
            latest_match=latest_temp

        #dodawanie nowejpozycji do tablicy
        max_xy_tab.append([latest_match, param.draw_color])
        if len(max_xy_tab) > param.max_table_size:
            max_xy_tab.remove(max_xy_tab[0])

        # rysowanie w zapisanych lokacjach
        if param.thickness > 1:
            for pnt in range(len(max_xy_tab)):
                point=max_xy_tab[pnt]
                point2=point
                if pnt != 0:
                    point2=max_xy_tab[pnt-1]

                for i in range(param.thickness):
                    for j in range(param.thickness):
                        if 0 < point[0][0] + i < len(img) and 0 < point[0][1] + i < len(img[1]):
                            if point != point2:
                                p1=(int(point[0][1]) + j,int(point[0][0]) + i)
                                p2=(int(point2[0][1]) + j,int(point2[0][0]) + i)
                                cv2.line(img,p2, p1,point[1], int(param.thickness/2))

                            # obecny punkt jako przeciwienstwo zwyklego koloru
                            if (point == max_xy_tab[len(max_xy_tab) - 1]):
                                img[int(point[0][0]) + i][int(point[0][1]) + j] = [255 - param.draw_color[0],
                                                                                   255 - param.draw_color[1],
                                                                                   255 - param.draw_color[2]]
                            else:
                                img[int(point[0][0]) + i][int(point[0][1]) + j] = point[1]

        if pause == True:
            pause2 = True
            pause = False
            cv2.putText(img, "PAUSED", (int(size[0] / 2), int(size[1] / 2)), cv2.FONT_HERSHEY_SIMPLEX, 3,
                        (255, 255, 255), 2, cv2.LINE_AA)

        #powiekszanie obrazka
        img = cv2.resize(img, (size[1]*2,size[0]*2))
        cv2.imshow('teraz', img)



    cap.release()
    cv2.destroyAllWindows()


def config(param):
    try:
        print("USTAWIENIA")
        choice = int(input(
            "1 = ogolne, " + "2 = porzadany kolor, " + "3 = kolor rysowania. 4 = poleposzukiwan"))

        if(choice==1):
            param.thickness = int(input("podaj grubosc linii (def=" + str(param.thickness) + ")"))
            param.max_table_size = int(input("podaj ilosc pixeli do rysowania (def=" + str(param.max_table_size) + ")"))
            param.tolerance = int(input("podaj poziom tolerancji koloru (def=" + str(param.tolerance) + ")"))
        if (choice == 2):
            print("podaj wartosci RGB porzadanego koloru (def=" + str(param.value) + ")")
            param.value[0] = int(input("B "))
            param.value[1] = int(input("G "))
            param.value[2] = int(input("R "))
        if (choice == 3):
            print("podaj wartosci RGB koloru rysowania (def=" + str(param.draw_color) + ")")
            param.draw_color[0] = int(input("B "))
            param.draw_color[1] = int(input("G "))
            param.draw_color[2] = int(input("R "))
        if (choice == 4):
            print("podaj rozmiar pola przeszukiwan (def=" + str(param.search_area) + ")")
            param.search_area[0] = int(input("X "))
            param.search_area[1] = int(input("Y "))
    except:
        print("wrong iput")


if __name__ == "__main__":
    # >pyinstaller -F plik.py    //do exe
    param = Parameters()

    if (input("czy chcesz poznac intrukcje? 1=tak") == "1"):
        input("OPIS: Program służy do rysowania ruchem przez kamere. program szuka punktow najbardziej zblizonych do pozadanego koloru i rysuje na nich porzadany kolor. ")
        input("Zaleca sie wybranie kontrolera o konktetnym kolorze, np. biale swiatlo z komorki przy szukaniu bialego koloru")
        input("Przy ustawianiu kolorow pamietaj, ze przyjmuja one wartosci 0-255 w skalach Blue Green Red")
        input("SPACE = pauza, ustawianie parametrow na konsoli")
        input("WSAD = alternatywne poruszanie sie po palecie")
        input("Po tej wiadomosci bedzie mozna ustalic pierwotne parametry\n")

    ok=False
    while ok==False:
        try:
            choice = int(input(
                "0 = domyslne parametry, " + "1 = podaj kolor i grubosc, " + "2 = podaj dokladne parametry"))

            if choice == 1:
                print("podaj wartosci RGB porzadanego koloru ")
                param.value[0] = int(input("B "))
                param.value[1] = int(input("G "))
                param.value[2] = int(input("R "))

                param.thickness = int(input("podaj grubosc linii (def="+str(param.thickness)+")"))

            if choice == 2:
                param.thickness = int(input("podaj grubosc linii (def="+str(param.thickness)+")"))
                param.max_table_size = int(input("podaj ilosc pixeli do rysowania (def="+str(param.max_table_size)+")"))
                param.tolerance = int(input("podaj poziom tolerancji koloru (def="+str(param.tolerance)+")"))
                param.flipped = bool(input("tryb flipped ENTER=False (def=" + str(param.flipped) + ")"))

                print("podaj wartosci RGB porzadanego koloru (def="+str(param.value)+")")
                param.value[0] = int(input("B "))
                param.value[1] = int(input("G "))
                param.value[2] = int(input("R "))

                print("podaj wartosci RGB koloru rysowania (def="+str(param.draw_color)+")")
                param.draw_color[0] = int(input("B "))
                param.draw_color[1] = int(input("G "))
                param.draw_color[2] = int(input("R "))

                print("podaj rozmiar pola przeszukiwan (def="+str(param.search_area)+")")
                param.search_area[0] = int(input("X "))
                param.search_area[1] = int(input("Y "))

            ok=True
        except:
            print("wrong input")

    searchcam(param)
    # searchcam([0, 0, 255], 20)