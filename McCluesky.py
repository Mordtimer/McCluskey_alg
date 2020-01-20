from BoolFunction import BoolFunction


class McCluesky():
    @staticmethod
    def optimize(self):
        all_tabs = []
        current_vital_indexes_int = self._DNF[0] + self._DNF[1]
        current_vital_indexes = []
        for x in self._DNF[0]:
            current_vital_indexes.append([str(x)])
        for y in self._DNF[1]:
            current_vital_indexes.append([str(y)])

        sorted_tab = McCluesky._sortByHammingWeight(self._table, current_vital_indexes_int)
        sorted_tab = McCluesky._getNextStepTable(sorted_tab)
        indexes = McCluesky._removeUsedIndexes(sorted_tab, current_vital_indexes)
        current_vital_indexes = indexes[2]
        all_tabs.append(sorted_tab)
        # print(current_used_indexes)
        # print(current_splited_idexes)
        # print(current_vital_indexes)

        while True:
            # print("Next step: ")
            sorted_tab = McCluesky._repeatedSorting(sorted_tab)
            sorted_tab = McCluesky._getNextStepTable(sorted_tab)
            indexes = McCluesky._removeUsedIndexes(sorted_tab, current_vital_indexes)
            current_used_indexes = indexes[0]
            current_splited_idexes = indexes[1]
            current_vital_indexes = indexes[2]
            # print(current_used_indexes)
            # print(current_splited_idexes)
            # print(current_vital_indexes)
            # print("Hi")
            all_tabs.append(sorted_tab)
            if len(current_used_indexes) == 0:
                break

        McCluesky._lastStep(all_tabs, self._DNF, current_vital_indexes)

    @staticmethod
    def _lastStep(tab, DNF, vital_indexes):
        final_tabs = []
        final_implicants = []
        for x in vital_indexes:
            final_tabs.append(McCluesky._find(tab, x))
        # print(final_tabs)
        for final_tab in final_tabs:

            element = final_tab[len(final_tab)-1].split("i")
            element.remove(element[len(element)-1])
            final_implicants.append(element)
        print(final_implicants)

    @staticmethod
    def _find(tab_list, index):

        for tab_version_list in reversed(tab_list):
            for tab in tab_version_list:
                for element in tab:
                    element1 = element.split("i")
                    element1.remove(element1[len(element1) - 1])
                    #element1_int = []
                    #print(sorted(element1))
                    #print(sorted(index))
                    #for x in element1:
                        #element1_int.append(int(x))
                    if sorted(element1) == sorted(index):
                        print(tab)
                        return tab

    @staticmethod
    def _remDuplicates(mylist):
        return list(dict.fromkeys(mylist))

    @staticmethod
    def _removeUsedIndexes(tab, vital):
        used_ones_full = []
        used_ones_splited = []
        for row in tab:
            if len(row) > 0:
                index_info = row[len(row) - 1]
                index_info = index_info.split('i')
                index_info.remove(index_info[len(index_info) - 1])
                used_ones_full.append(index_info)

        for x in used_ones_full:
            for y in used_ones_full:
                if x != y:
                    if sorted(x) == sorted(y):
                        used_ones_full.remove(x)

        if len(used_ones_full) != 0:
            max_size = len(used_ones_full[len(used_ones_full) - 1])
        else:
            max_size = 2
        # print(used_ones_full)
        for i in range(len(used_ones_full)):

            if len(used_ones_full[i]) == max_size:
                element1 = []
                for j in range(int(max_size / 2)):
                    element1.append(used_ones_full[i][j])
                used_ones_splited.append(element1)
                element2 = []
                for j in range(int(max_size / 2), max_size):
                    element2.append(used_ones_full[i][j])
                used_ones_splited.append(element2)
            else:
                for j in range(len(used_ones_full[i])):
                    used_ones_splited.append(used_ones_full[i][j])

        # print(used_ones_splited)
        """for i in range(len(used_ones_splited)):
            for x in vital:
                # print("splited: " + str(used_ones_splited[i]) + "vital: " + str(x))
                if sorted(x) == sorted(used_ones_splited[i]):
                    vital.remove(x)"""

        # print("did it")
        # print("VITAL Indexes")
        # print(vital)
        for x in used_ones_full:
            vital.append(x)

        add = []
        for x in used_ones_full:
            for y in vital:
                for z in vital:
                    if sorted(x) == (sorted(y + z)):
                        add.append(y)
                        add.append(z)
                        vital.remove(y)
                        vital.remove(z)

        try:
            for x in used_ones_full:
                for z in vital:
                    for y in vital:
                        for a in add:
                            if sorted(x) == (sorted(z + a)):
                                add.append(z)
                                vital.remove(z)
                            if sorted(x) == (sorted(a + y)):
                                add.append(y)
                                vital.remove(y)
        except ValueError:
            pass

        return [used_ones_full, used_ones_splited, vital]

    @staticmethod
    def _getNextStepTable(sorted_tab):
        simple_implicants = [[]]
        # print(sorted_tab)
        try:
            for (i) in range(len(sorted_tab) - 1):

                """print("tab[i]:")
                print(sorted_tab[i])
                print("tab[i+1]:")
                print(sorted_tab[i+1])
                print("\n")"""
                for j in range(len(sorted_tab[i])):
                    for k in range(len(sorted_tab[i + 1])):
                        if McCluesky._bitDifference(sorted_tab[i][j], sorted_tab[i + 1][k]) == 1:

                            dif_index = McCluesky._bitDifferenceIndex(sorted_tab[i][j], sorted_tab[i + 1][k])
                            index_info = str(sorted_tab[i][j][len(sorted_tab[i][j]) - 1]) + \
                                         str(sorted_tab[i + 1][k][len(sorted_tab[i + 1][k]) - 1])

                            simple_implicant = []
                            for d in range(len(sorted_tab[i][j]) - 1):
                                simple_implicant.append(sorted_tab[i][j][d])
                            simple_implicant.append(index_info)
                            simple_implicant[dif_index] = "_"
                            """for x in simple_implicants:
                                the_same = 0
                                for z in range(len(x)-2):
                                    if simple_implicant[z] == x[z]:
                                        the_same += 1
                                if the_same == len(x)-1:"""

                            simple_implicants.append(simple_implicant)
                            """
                            print(sorted_tab[i][j])
                            print(sorted_tab[i+1][k])
                            print(simple_implicant)
                            print(index_info)"""


        except IndexError:
            print("ERROR at j:" + str(j) + " k:" + str(k))

        if len(simple_implicants[0]) == 0:
            simple_implicants.remove(simple_implicants[0])
        # print(simple_implicants)
        return simple_implicants

    @staticmethod
    def _repeatedSorting(tab):
        el_in_row = len(tab[0])
        sorted_tab = [[] for col in range(el_in_row + 1)]
        for row in tab:
            element = row
            current_weight = McCluesky._getHammingWeight(element, el_in_row)
            sorted_tab[current_weight].append(element)
        return sorted_tab

    @staticmethod
    def _sortByHammingWeight(tab, vital_indexes_int):
        how_much_rows = len(tab)

        el_in_row = len(tab[0])
        sorted_tab = [[] for col in range(el_in_row + 1)]
        for i in vital_indexes_int:
            try:
                index_info = str(i) + "i"
                element = tab[i] + [index_info]
                current_weight = McCluesky._getHammingWeight(element, el_in_row)
                sorted_tab[current_weight].append(element)
            except IndexError:
                print("Error at row: " + str(tab[i]) + " at index" + i)

        if len(sorted_tab[0]) == 0:
            sorted_tab.remove(sorted_tab[0])
        # print(sorted_tab)
        return sorted_tab

    @staticmethod
    def _getHammingWeight(row, el_in_row):
        weight = 0
        for i in range(el_in_row - 1):
            if row[i] == "1":
                weight += 1
        return weight

    @staticmethod
    def _bitDifference(row1, row2):
        if len(row1) != len(row2):
            return -1
        bit_dif = 0
        for i in range(len(row1) - 2):
            if row1[i] != row2[i]:
                bit_dif += 1
        return bit_dif

    @staticmethod
    def _bitDifferenceIndex(row1, row2):
        index = -1
        for i in range(len(row1) - 2):
            if row1[i] != row2[i]:
                index = i
        return index


function1 = BoolFunction("bool4.txt", "f")
function2 = BoolFunction("bool2.txt", "g")
function3 = BoolFunction("bool3.txt", "h")
function1.showDNF()
McCluesky.optimize(function1)

#McCluesky.optimize(function2)
