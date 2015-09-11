#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-

from math import pi, cos
from Point2Draw import Point2Draw
from StatCalcStore import StatCalcStore


class drawDensity:

    '''Класс создаёт js-файл с 2D-массивом данных'''

    def __init__(self, lat0, lon0, lat1, lon1, pix_height, pix_width):
        # Высчитываем высоту и ширину карты в километрах
        heightKM = (lat1 - lat0) / (1 / 6372.795 / pi * 180)
        widthKM = (lon1 - lon0) / \
            (1 / 6372.795 / pi * 180 / cos((lat0 + lat1) / 2 * pi / 180))

        # Высчитываем количество пикселей по высоте и ширине
        # при заданном размере одного пикселя
        yN = int(heightKM / pix_height)
        xN = int(widthKM / pix_width)

        # Выводим на экран размер картинки в пикселях, размер картинки в
        # километрах (ширина и высота) и размер одного пикселя в километрах
        print('Map in px: ' + str(xN) + ' x ' + str(yN) +
              '\nMap in km: %.1f x %.1f' % (widthKM, heightKM) +
              '\n1 px in km: %.1f x %.1f' % (widthKM / xN, heightKM / yN))

        self.lon0 = lon0
        self.lon1 = lon1
        self.lat0 = lat0
        self.lat1 = lat1
        self.yN = yN
        self.xN = xN
        self.total = 0

        self.drawP = Point2Draw(xN, yN)  # класс для отрисовки результатов

        # Создаем таблицу размером (xN + 1)*(yN + 1), соответствующую созданной
        # координатной сетке. В ячейках будут находиться списки всех значений
        # для данного квадрата.
        self.statStore = [[StatCalcStore() for i in range(xN + 1)]
                          for j in range(yN + 1)]

    def insertLatLon(self, lat, lon, v):
        '''Функция работает следующим образом: если передаваемые координаты
        выходят за границы рассматриваемой карты, то они не учитываются.
        Для всех остальных координат возвращается значение x и y (определяется
        принадлежность к определенному пикселю на карте) и параметр v'''
        if(lat >= self.lat1 or lat < self.lat0):
            return
        if(lon >= self.lon1 or lon < self.lon0):
            return

        y = int((lat - self.lat0) / (self.lat1 - self.lat0) * self.yN)
        x = int((lon - self.lon0) / (self.lon1 - self.lon0) * self.xN)

        # Добавляем каждый параметр v в соответствующий квадрат нашей
        # координатной сетки
        self.statStore[y][x].insert(v)

    def addDataV4(self, f, delimiter=','):
        '''Забираем данные из файла и отдаем их функции.
        Формат данных: широта,долгота,параметр'''
        for line in f:
            data = line.strip().split(delimiter)
            try:
                data = [float(x) for x in data]
            except ValueError:
                continue
            lat = data[0]
            lon = data[1]
            v = data[2]
            self.insertLatLon(lat, lon, v)


def main():
    # Задаем границы карты в координатах
    town = 'msk_big2'
    if town == 'spb':
        (lon0, lat0) = (29.98492, 59.762993)
    if town == 'ukr':
        (lon0, lat0) = (21.727321, 43.347907)
    if town == 'kiev':
        (lon0, lat0, lon1, lat1) = (30.323687, 50.324807, 30.697222, 50.5559)
    if town == 'msk_s1':
        (lat0, lon0, lat1, lon1) = (55.5525, 37.22, 55.9475, 37.94)
    if town == 'msk_big':
        (lat0, lon0, lat1, lon1) = (55.367793, 37.209804, 56.013183, 37.973353)
    if town == 'msk_big2':
        (lat0, lon0, lat1, lon1) = (55.436562, 37.016856, 56.054702, 38.114116)
    if town == 'russia':
        (lat0, lon0, lat1, lon1) = (7.81, 0, 67.61, 132.41)

    pix_width = 0.3
    pix_height = 0.3

    # Рассчитываем все начальные параметры, создаём координатную сетку
    d = drawDensity(lat0, lon0, lat1, lon1, pix_height, pix_width)

    # Добавляем данные в координатную сетку
    d.addDataV4(open('data/data.csv', encoding='utf-8'),
                delimiter=';')

    # Теперь для каждого квадрата получаем какое-то одно число: среднее,
    # медиану или количество значений в ячейке (или что-нибудь ещё)
    for y in range(d.yN + 1):
        for x in range(d.xN + 1):
            num = d.statStore[y][x].getNumber()
            d.drawP.data[y][x] = num
            d.total += num

    # Пишем результат в js-массив
    d.drawP.saveDataJS('heatmap/data/data.js')

    print('Total=' + str(d.total))

if __name__ == '__main__':
    main()
