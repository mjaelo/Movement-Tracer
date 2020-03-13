import cv2
import base64
import os


def search(imgname, value, frames_nr, thicc):
    img2 = cv2.imread(imgname + "1.png")  # obraz przed animacja
    for cos in range(frames_nr):
        img = cv2.imread(imgname + str(cos + 1) + ".png")  # t.png
        # zczytuja sie po kolei klatki animacji

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

        change = [0, 0, 0]  # kolor zaznaczenia
        img2[max_xy[0]][max_xy[1]] = change
        if thicc > 1:
            for i in range(thicc):
                for j in range(thicc):
                    if 0 < max_xy[0] + i < len(img) and 0 < max_xy[1] + i < len(
                            img[1]):
                        try:
                            img2[max_xy[0] + i][max_xy[1] + j] = change
                        except:
                            print("out of bounds")
        print(str(cos + 1) + " roznica: " + str(max_sr) + "  pozycja:" + str(max_xy))

    cv2.imwrite(imgname + "_out.png", img2)
    print("wynik zapisano do pliku: " + imgname + "_out.png")
    os.system("PAUSE")


if __name__ == "__main__":
    # >pyinstaller -F plik.py    //do exe
    value = [255, 255, 255]
    value[0] = int(input("podaj porzadana wartosc koloru B "))
    value[1] = int(input("podaj porzadana wartosc koloru G "))
    value[2] = int(input("podaj porzadana wartosc koloru R "))

    thicc = int(input("podaj grubosc linii "))
    imgname = input("podaj nazwe poczatkowa obrazow(ex1.png, ex2.png, itp) ")
    frames_nr = input("ile klatek animacji? ")
    search(imgname, value, int(frames_nr), thicc)
