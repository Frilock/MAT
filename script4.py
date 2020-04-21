# Промоделировать работу системы массового обслуживания с ограниченной очередью
# размеров b. Оценить путем моделирования среднее количество заявок в системе E[N] и
# среднюю задержку E[D]. Также произвести теоретический расчет двух данных величин.

import random


def theoretic():
    print("Теоретический расчет")


def system(queue_size, number_of_applications, processing_time):
    time = 0
    lambdas = 0.3  # интенсивность

    time += random.expovariate(1 / lambdas)


def main():
    queue_size = 5  # размер очереди
    number_of_applications = 10000  # количество заявок
    processing_time = 1  # время обработки заявки

    print("Моделирование", system(queue_size, number_of_applications, processing_time))
    print("", theoretic())


main()
