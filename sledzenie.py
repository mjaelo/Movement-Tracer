import cv2
import os

# dziala, ale muli, bo patrzy na caly obrazek
def findclosestpix(value, img):
    max_sr = 100000  # wartosc maxymalnie zblizona do poszukiwanej wartosci
    max_xy = [0, 0]
    for r in range(len(img)):
        row = img[r]
        for pi in range(len(row)):
            pixel = row[pi]
            s = 0
            for num in range(len(pixel)):
                temp = pixel[num] - value[num]
                s += temp * temp
            srednia = s
            s = 0
            if (srednia < max_sr):
                max_sr = srednia
                max_xy = [r, pi]
    return max_xy


errors = 0
# srednio dziala, jest szybszy, bo patrzy tylko na czesc obrazka
def findclosestpix2(value, img, pix, area):
    global errors
    max_sr = 100000  # wartosc maxymalnie zblizona do poszukiwanej wartosci
    max_xy = pix
    pozX = 0
    pozY = 0
    try:
        for r in range(area[0]):
            pozY = r + pix[0]
            pozY = pozY - (area[0] / 2)
            if pozY > len(img):
                pozY = pix[0] - r
            if pozY < 10:
                pozY = 10
            row = img[int(pozY)]

            for pi in range(area[1]):
                pozX = pi + pix[1]
                pozX = pozX - (area[1] / 2)
                if pozX > len(img[0]):
                    pozX = pix[1] - pi
                if pozX < 10:
                    pozX = 10

                pixel = row[int(pozX)]

                s = 0
                for num in range(len(pixel)):
                    temp = pixel[num] - value[num]
                    s += temp * temp
                srednia = s
                s = 0
                if (srednia < max_sr):
                    max_sr = srednia
                    max_xy = [pozX, pozY]
        errors = 0
    except:
        ok = "ok"
        print("searching error nr." + str(errors))
        errors += 1
        if errors > 5:
            max_xy = findclosestpix(value, img)
            errors = 0
    return max_xy


def searchcam(value, thickness):
    cap = cv2.VideoCapture(0)
    ret, img2 = cap.read()
    cv2.imshow('przed', img2)
    temporary = "ok"
    max_xy_tab = []
    latest_match = findclosestpix(value, img2)
    max_xy_tab.append(latest_match)  # znalezienie najblizszego matchu na calym obrazie w pierwszej klatce

    print(len(img2), len(img2[0]))

    while (temporary == "ok"):
        # zczytuja sie po kolei klatki animacji
        ret, img = cap.read()
        key = cv2.waitKey(30)

        # dodanie lokacji najlepszego matchu do tablicy
        search_area = [100, 100]
        latest_match2 = findclosestpix2(value, img, latest_match, search_area)
        latest_match = [(latest_match[0] + latest_match2[0]) / 2,
                        (latest_match[1] + latest_match2[1]) / 2]  # strednia starego i nowego punktu, by ograniczyc wariactwa
        print(latest_match)
        max_xy_tab.append(latest_match)
        if len(max_xy_tab) > 30:
            max_xy_tab.remove(max_xy_tab[0])

        # rysowanie w zapisanych lokacjach
        draw_color = value  # kolor zaznaczenia
        if thickness > 1:
            for point in max_xy_tab:
                if (point == max_xy_tab[len(max_xy_tab) - 1]):
                    draw_color = [255 - value[0], 255 - value[1], 255 - value[2]]
                for i in range(thickness):
                    for j in range(thickness):
                        if 0 < point[0] + i < len(img) and 0 < point[1] + i < len(
                                img[1]):
                            try:
                                img[int(point[0]) + i][int(point[1]) + j] = draw_color
                            except:
                                print("coloring error")
                                ok = "ok"
        cv2.imshow('teraz', img)
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # >pyinstaller -F plik.py    //do exe
    value = [255, 255, 255]
    value[0] = int(input("podaj porzadana wartosc koloru B "))
    value[1] = int(input("podaj porzadana wartosc koloru G "))
    value[2] = int(input("podaj porzadana wartosc koloru R "))
    thickness = int(input("podaj grubosc linii "))

    searchcam(value,thickness)
    #searchcam([0, 0, 255], 20)
