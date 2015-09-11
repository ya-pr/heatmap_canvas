import math
import re


class Point2Draw:

    '''Класс работает с 2D массивом данных для рисования на карте
    (путём генерации соответствующих файлов)'''

    def __init__(self, xN, yN):
        self.data = [[0 for i in range(xN + 1)] for j in range(yN + 1)]
        self.xN = xN
        self.yN = yN

    def saveDataJS2(self, fileName):
        wf = open(fileName, 'w')
        wf.write("[]")
        for y in range(self.yN, 0, -1):
            wf.write("\n")
            for x in range(self.xN):
                wf.write(str(self.data[y][x]) + ",")
        wf.close()

    def saveDataJS3(self, fileName):
        wf = open(fileName, 'w')
        wf.write("[]")
        for y in range(self.yN, 0, -1):
            for x in range(self.xN):
                wf.write("\n")
                wf.write(str(x) + "," + str(y) + "," + str(self.data[y][x]))
        wf.close()

    def saveDataJS(self, fileName):
        sum = 0
        wf = open(fileName, 'w')
        wf.write("var x=" + str(self.xN) + ", y=" + str(self.yN) + ",\n")
        wf.write("data=[")
        for y in range(self.yN, 0, -1):
            wf.write("\n")
            for x in range(self.xN):
                wf.write(str(self.data[y][x]) + ",")
                sum += self.data[y][x]
        wf.write("];")
        wf.close()
        if(sum == 0):
            print("saveDataJS: sum=0")

    def saveDataOctave(self, fileName):
        wf = open(fileName, 'w')
        wf.write("# name: picData\n")
        wf.write("# type: matrix\n")
        wf.write("# rows: " + str(self.yN) + "\n")
        wf.write("# columns: " + str(self.xN) + "\n")
        for y in range(self.yN, 0, -1):
            wf.write("\n")
            for x in range(self.xN):
                wf.write(str(self.data[y][x]) + " ")
        wf.close()

    def setCoordData(self, lat0, lon0, dLat, dLon):
        print(lat0, lon0, dLat, dLon)
        self.lat0 = lat0
        self.dLat = dLat
        self.lon0 = lon0
        self.dLon = dLon

    def makeBigBlocks(self, blockS):
        self.xBlockN = math.floor((self.xN - 1) / blockS)
        self.yBlockN = math.floor((self.yN - 1) / blockS)
        self.blockS = blockS
        self.dataB = [[0 for i in range(self.xBlockN + 1)]
                      for j in range(self.yBlockN + 1)]
        for y in range(self.yBlockN):
            for x in range(self.xBlockN):
                for xi in range(blockS + 1):
                    for yi in range(blockS + 1):
                        self.dataB[y][x] += self.data[
                            y * blockS + yi][x * blockS + yi]
        for y in range(self.yBlockN):
            for x in range(self.xBlockN):
                self.dataB[y][x] /= (blockS + 1) * (blockS + 1)
        if 0:
            for y in range(self.yBlockN):
                print(">")
                for x in range(self.xBlockN):
                    print(self.dataB[y][x],)

    def saveBigDataOnMap(self, fileName, numMin, numMax):
        self.numMax = numMax
        self.numMin = numMin
        # рисуем на карте DrawOnMap=dom :-)
        domFr = open(r'drawOnMapT.html', 'r')
        domFw = open(fileName, 'w')

        domLine = domFr.readline()
        while(domLine):
            domFw.write(domLine)
            if(domLine == "//startRewriteFromHere\n"):
                break
            domLine = domFr.readline()
        domFw.write('map.setCenter(new YMaps.GeoPoint(' +
                    str(self.lon0 + self.yN * self.dLon / 2) + ',' +
                    str(self.lat0 + self.xN * self.dLat / 2) + '), 11);\n')

        pointsN = 0
        for y in range(self.yBlockN):
            for x in range(self.xBlockN):
                if(self.dataB[y][x] > 0):
                    if pointsN >= 1000:
                        break
                    pointsN += self.printRectPointToHTML(domFw,
                                                         x * self.dLon * self.blockS + self.lon0, y *
                                                         self.dLat *
                                                         self.blockS +
                                                         self.lat0,
                                                         self.dLon * (self.blockS + 1), self.dLat * (self.blockS + 1), self.dataB[y][x])

        domLine = domFr.readline()
        while(domLine):
            if(domLine == "//endRewriteHere\n"):
                break
            domLine = domFr.readline()
        while(domLine):
            domFw.write(domLine)
            domLine = domFr.readline()

        domFr.close()
        domFw.close()

    def printRectPointToHTML(self, f, lon, lat, dLon, dLat, num):
        numMin = self.numMin
        numMax = self.numMax
        if(num <= numMin):
            return 0
        n = (num - numMin) / (numMax - numMin)
        if(n > 1):
            n = 1
        style = int(n * 3) + 1

        f.write('pl = new YMaps.Polygon([new YMaps.GeoPoint(' + str(lon) + ',' + str(lat) +
                '),new YMaps.GeoPoint(' + str(lon) + ',' + str(lat + dLat) +
                '),new YMaps.GeoPoint(' + str(lon + dLon) + ',' + str(lat + dLat) +
                '),new YMaps.GeoPoint(' + str(lon + dLon) + ',' + str(lat) + ')]);\n')
        f.write('pl.name="' + str(float(num)) + '";\n')
        f.write(
            'pl.setStyle("rect' + str(style) + '");\ngCollection.add(pl);\n')
        return 1
