from BoolFunction import BoolFunction
import sys


class McCluesky:
    # Main loop agents
    @staticmethod
    def optimize(self):
        if len(self._DNF[0]) == 0:
            return "f(x) = 0"

        all_tabs = []
        current_vital_indexes_int = self._DNF[0] + self._DNF[1]
        current_vital_indexes = []
        for x in self._DNF[0]:
            current_vital_indexes.append([str(x)])
        for y in self._DNF[1]:
            current_vital_indexes.append([str(y)])

        sorted_tab = McCluesky._sortByHammingWeight(self._table, current_vital_indexes_int)
        first_sorted_tab = sorted_tab
        sorted_tab = McCluesky._getNextStepTable(sorted_tab)
        indexes = McCluesky._removeUsedIndexes(sorted_tab, current_vital_indexes)
        current_vital_indexes = indexes[2]

        # 1d table creating for all table list
        sorted_tab_bis = []
        for row in first_sorted_tab:
            for element in row:
                sorted_tab_bis.append(element)
        all_tabs.append(sorted_tab_bis)
        all_tabs.append(sorted_tab)
        del sorted_tab_bis
        del first_sorted_tab

        while True:
            sorted_tab = McCluesky._repeatedSorting(sorted_tab)
            sorted_tab = McCluesky._getNextStepTable(sorted_tab)
            indexes = McCluesky._removeUsedIndexes(sorted_tab, current_vital_indexes)
            current_used_indexes = indexes[0]
            # current_splited_idexes = indexes[1]
            current_vital_indexes = indexes[2]
            all_tabs.append(sorted_tab)
            if len(current_used_indexes) == 0:
                break

        return McCluesky._lastStep(all_tabs, self._DNF, current_vital_indexes)

    @staticmethod
    def _lastStep(tab, dnf, vital_indexes):
        final_tabs = []
        final_implicants = []
        for x in vital_indexes:
            final_tabs.append(McCluesky._find(tab, x))

        # split index inf row into a list
        for final_tab in final_tabs:
            element = final_tab[len(final_tab) - 1].split("i")
            element.remove(element[len(element) - 1])
            final_implicants.append(element)

        print("\nImplicants: ")
        for x in final_tabs:
            print(x)
        # sort indexes values in final tabs
        info_index = len(final_tabs[0]) - 1
        for x in final_tabs:
            x[info_index] = x[info_index].rstrip('i').split("i")
            McCluesky.sortStringAsInt(x, info_index)

        # sorting tables and implicants
        McCluesky._bubbleSortByLastIndex(final_tabs, info_index)
        McCluesky._removeFunctionValueAndInfo(final_tabs)
        # McCluesky._removeLastIndex(final_tabs)
        final_implicants = McCluesky._finalSorForImplicants(final_implicants)

        # print("\nlista przekazywana jako implicantsArray")
        # print(final_implicants)
        # print("\nlista przekazywana jako binaryArray")
        # for x in final_tabs:
        #   print(x)

        final_final = McCluesky._giveRelevantBinaryArrays(final_implicants, final_tabs, dnf[1])
        return McCluesky._convertToPrettyFunction(final_final)

    @staticmethod
    def _find(tab_list, index):

        for tab_version_list in reversed(tab_list):
            for tab in tab_version_list:
                for element in tab:
                    element1 = element.split("i")
                    element1.remove(element1[len(element1) - 1])
                    # element1_int = []
                    # print(sorted(element1))
                    # print(sorted(index))
                    # for x in element1:
                    # element1_int.append(int(x))
                    if sorted(element1) == sorted(index):
                        # print(tab)
                        return tab

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
                            simple_implicants.append(simple_implicant)

        except IndexError:
            print("ERROR")

        if len(simple_implicants[0]) == 0:
            simple_implicants.remove(simple_implicants[0])
        # print(simple_implicants)
        return simple_implicants

    @staticmethod
    def _repeatedSorting(tab):
        el_in_row = 0
        for x in tab:
            if len(x) != 0:
                el_in_row = len(x)
                break
        sorted_tab = [[] for col in range(el_in_row + 1)]
        for row in tab:
            element = row
            current_weight = McCluesky._getHammingWeight(element, el_in_row)
            sorted_tab[current_weight].append(element)
        return sorted_tab

    # Prep-functions. Used for first iteration
    @staticmethod
    def _sortByHammingWeight(tab, vital_indexes_int):

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

    # Help me pls!
    @staticmethod
    def _finalSorForImplicants(implicants):

        for implicant_str in implicants:
            implicant_int = []
            for element in implicant_str:
                implicant_int.append(int(element))
            implicant_int = sorted(implicant_int)
            implicant_str = []
            for element in implicant_int:
                implicant_str.append(str(element))
        return implicants

    @staticmethod
    def _bubbleSortByLastIndex(list_of_lists, index):
        n = len(list_of_lists)
        for i in range(n):
            for j in range(0, n - 1):
                if len(list_of_lists[j][index]) > len(list_of_lists[j + 1][index]):
                    list_of_lists[j], list_of_lists[j + 1] = list_of_lists[j], list_of_lists[j + 1]
                elif len(list_of_lists[j][index]) == len(list_of_lists[j + 1][index]):
                    leng = len(list_of_lists[j][index])
                    for k in range(leng):
                        if int(list_of_lists[j][index][k]) > int(list_of_lists[j + 1][index][k]):
                            list_of_lists[j], list_of_lists[j + 1] = list_of_lists[j + 1], list_of_lists[j]

    @staticmethod
    def _removeFunctionValueAndInfo(list_of_lists):
        for x in list_of_lists:
            del x[-2:]

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

    @staticmethod
    def sortStringAsInt(row, info_index):
        temp_int = []
        for str_el in row[info_index]:
            temp_int.append(int(str_el))
            temp_int = sorted(temp_int)
        row[info_index] = []
        for int_el in temp_int:
            row[info_index].append(str(int_el))

    @staticmethod
    def _giveRelevantBinaryArrays(implicants_array, binary_array, dont_care=None):
        if dont_care is None:
            dont_care = []
        digits = []
        number_of_digits = []
        binary_arrays_to_final_function = []
        implicants_arrays_to_final_function = []

        for imp in implicants_array:
            for digit in imp:
                if digit in digits:
                    index = digits.index(digit)
                    number_of_digits[index] += 1
                else:
                    digits.append(digit)
                    number_of_digits.append(1)

        for i in range(0, len(implicants_array)):
            for digit in implicants_array[i]:
                index = digits.index(digit)
                if number_of_digits[index] == 1 and digit not in dont_care:
                    binary_arrays_to_final_function.append(binary_array[i])
                    implicants_arrays_to_final_function.append(implicants_array[i])
                    break

        for i in range(0, len(digits)):
            connected = McCluesky._connectArrays(implicants_arrays_to_final_function)
            if digits[i] not in connected and digits[i] not in dont_care:
                missing_digit = digits[i]
                for how_many in range(0, len(implicants_array)):
                    if implicants_array[how_many] not in implicants_arrays_to_final_function and missing_digit in implicants_array[how_many]:
                        implicants_arrays_to_final_function.append(implicants_array[how_many])
                        binary_arrays_to_final_function.append(binary_array[how_many])
                        missing_digit = "$"

        return binary_arrays_to_final_function

    @staticmethod
    def _connectArrays(array):
        new = []
        for i in array:
            for j in i:
                new.append(j)
        return new

    @staticmethod
    def _convertToPrettyFunction(binary_arrays, function_name="f"):
        function = function_name + " = "
        attributes = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

        for j in range(0, len(binary_arrays)):
            bin_arr = binary_arrays[j]
            for i in range(0, len(bin_arr)):
                if bin_arr[i] != '_':
                    function += attributes[i]
                    if bin_arr[i] == '0':
                        function += '\''
            if j != len(binary_arrays) - 1:
                function += " + "

        return function


print("\n")
function1 = BoolFunction(sys.argv[1])
function1.showDNF()
result = McCluesky.optimize(function1)
print("\n" + result + "\n")
