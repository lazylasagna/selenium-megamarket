import json
from prettytable import PrettyTable


def table(data, l):
    td = []
    print(f'Количество товаров: {len(data)}')
    case = input("\n\033[38m{}".format('Сортировка:\n1 - по % кэшбека\n2 - по конечной цене: '))

    def add():
        td.append(d['name'])
        td.append(d['price'])
        td.append(d['bonus'])
        td.append('{:5.2f}'.format(int(d['bonus']) * 100 / int(d['price'])))
        td.append(int(d['price']) - int(d['bonus']))
        td.append(d['url'])

    while case != '1' and case != '2':
        case = input('Выберите 1 или 2: ')
    if case == '1':
        th = ['Название', 'Цена', 'Кэшбек', "\033[31m{}".format('% Кэшбека') + "\033[38m{}".format(''), 'Разница',
              'Ссылка']
    elif case == '2':
        th = ['Название', 'Цена', 'Кэшбек', '% Кэшбека', "\033[31m{}".format('Разница') + "\033[38m{}".format(''),
              'Ссылка']
    if l > 1:
        for d in data:
            add()
    else:
        for e in data:
            for d in e:
                add()

    columns = len(th)

    table = PrettyTable(th)

    td_data = td[:]

    while td_data:
        table.add_row(td_data[:columns])
        td_data = td_data[columns:]

    if case == '1':
        print(table.get_string(sortby="\033[31m{}".format('% Кэшбека') + "\033[38m{}".format(''), reversesort=True))
    elif case == '2':
        print(table.get_string(sortby="\033[31m{}".format('Разница') + "\033[38m{}".format('')))


def main():
    with open("f.json", "r") as r:
        data = json.load(r)
    i = 1
    if len(data) > 1:
        for category in data:
            print(f'\n{i} из {len(data)}')
            table(category, len(data))
            i += 1
    else:
        table(data, len(data))


if __name__ == '__main__':
    main()
