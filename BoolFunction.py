class BoolFunction:
    def __init__(self, path, name):
        self._path = path
        self._name = name
        self._table = self._getFromFile()
        self._r_len = self._getRowLen()
        self._el_index = {
            1: "x1",
            2: "x2",
            3: "x3",
            4: "x4",
            5: "x5",
            6: "x6",
            7: "x7",
        }
        self._DNF = self._getDNF()
        del self._path

    def _getRowLen(self):
        return len(self._table[1])

    def _getFromFile(self):
        tab = [[]]
        file = open(self._path, "r")
        for rows in file:
            row = []
            for element in rows:
                if element != "\n":
                    row.append(element)
            tab.append(row)
        file.close()
        tab.remove(tab[0])
        return tab

    def __str__(self):
        str_tab = ""
        # header
        for i in range(1, self._r_len):
            str_tab += str(self._el_index.get(i)) + " "
        str_tab += self._name + "(x)\n"
        # rest
        for row in self._table:
            for x in row:
                str_tab += x + "  "
            str_tab += "\n"
        return str_tab

    def _getDNF(self):
        tab = [[]]
        row = []
        i = 0
        # index values for DNF
        for f_x in self._table:
            if f_x[self._r_len-1] == "1":
                tab[0].append(i)
            i += 1
        i = 0
        tab.append(row)
        # don't care index
        for f_x in self._table:
            if f_x[self._r_len - 1] == "x":
                tab[1].append(i)
            i += 1
        return tab

    def showDNF(self):
        print("DNF " + self._name + "(x):")
        print("sum" + str(self._DNF[0]) + "\ndon't care: " + str(self._DNF[1]))
