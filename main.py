from pprint import pprint
import json
import math
import copy


def update(data, service, count):
    """

    из-за того, что все сервисы одинаково загружают сервер, достаточно работать с
    общей загруженностью сервера.
    суть алгоритма состоит в том, чтобы постепенно увеличивать загруженность серверов
    и приближать значения загруженности сервера к среднему значению загруженности
    для достижения равномерности распределения в виде уменьшения среднеквадратичного отклонения.
    квадратный корень в формулах используется для уменьшения среднеквадратичного отклонения,
    тогда количество итераций будет большее, но распределение будет более равномерное



    :param data:
    :param service:
    :param count:
    :return:
    """

    if count < 0:
        raise AttributeError("Count must be greater or equal zero")

    servers_data = copy.deepcopy(data)
    service_count_left = count
    while(service_count_left):

        # creating dict like {'service' : load}
        server_load = {server: sum(services.values()) for server, services in servers_data.items()}

        min_loaded_server = min(zip(server_load.values(), server_load.keys()))[1]
        avg_load = sum(server_load.values()) / len(server_load)


        # 1. к минимально загруженному серверу добавляется сервисы в количестве квадратного корня от разницы между
        # средней загруженностью и загруженностью данного сервера
        # 2. в случаях, если все серверы загружены одинаково, первое значение будет 0, тогда стоит ускорить
        # процесс, добавив в один из серверов часть остатка сервисов
        # 3. при малом количестве остатка сервисов, предыдущие значения могут быть 0, в таком случае достаточно
        # добавлять сервисы поштучно
        next_load_ct = \
            int(math.sqrt(avg_load - server_load[min_loaded_server])) \
            or int(service_count_left / len(servers_data)) \
            or 1

        # если полученное выше число превышает остаток сервисов, то тогда брать остаток сервисов
        next_load_ct = min(next_load_ct, int(math.sqrt(service_count_left)))

        servers_data[min_loaded_server][service] = \
            next_load_ct + (servers_data[min_loaded_server].get(service) or 0)

        service_count_left -= next_load_ct

    # если я правильно понял подзадание 4, стоит работать с копией исходного словаря, чтобы значения в нем
    # поменялись ра один раз с исходного на новое
    for key in data:
        data[key] = copy.deepcopy(servers_data[key])


def main():
    with open('data_example.json', 'r') as f:
        example_data = json.loads(f.read())

    print("Configuration before:")
    pprint(example_data)

    update(example_data, 'pylons', 10)

    print("Configuration after:")
    pprint(example_data)

if __name__ == '__main__':
    main()
