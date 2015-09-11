class StatCalc:

    '''Cчитает качество и доверительный интервал'''

    def reset(self):
        self.N = 0
        self.sum = 0

    def __init__(self):
        self.reset()

    def insert(self, x, w=1):
        self.N += w
        self.sum += x

    def getAverage(self):
        if self.N == 0:
            return
        return self.sum / self.N


class StatCalcStore:

    '''Считает какую-либо статистику для набора чисел'''

    def __init__(self):
        self.values = []

    def insert(self, x):
        self.values.append(x)

    def getNumber(self):
        return len(self.values)

    def getMedian(self):
        vlen = len(self.values)
        if vlen == 0:
            return
        elif vlen % 2:
            return sorted(self.values)[int((vlen - 1) / 2)]
        else:
            half = int(vlen / 2)
            return sum(sorted(self.values)[half - 1:half + 1]) / 2

    def getAverage(self):
        pass

    def getDispersionRoot(self):
        pass

    def back(self):
        return sorted(self.values)
