# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

    search = 3
    tab = [95, 11, 25, 32, 86, 2, 63, 3]

    # algo recherche liste non trié

    def search_algo(tab, search):
        return "true" if len([i for i in tab if i == search]) >= 1 else "false"

    def search_algo2(tab, search, i):
        return "true" if tab[i] == search else search_algo2(tab, search, i+1) if len(tab)-1 > i else "false"

    print("algo recherche liste non trié :", search_algo(tab, search))
    print("algo recherche liste non trié :", search_algo2(tab, search, 0))

    # algo recherche liste trié

    tab = [1, 2, 3, 5, 10, 12, 15, 22]
    def search_algo_not(tab, search):
        return "true" if len([i for i in tab if i == search and i <= search]) >= 1 else "false"

    def search_algo_not2(tab, search, i):
        return "true" if tab[i] == search else search_algo2(tab, search, i+1) if len(tab)-1 > i or tab[i] < search else "false"

    print("algo recherche liste trié     :", search_algo_not(tab, search))
    print("algo recherche liste trié     :", search_algo_not2(tab, search, 0))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
