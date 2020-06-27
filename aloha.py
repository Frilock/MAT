import numpy as np
import matplotlib.pyplot as plot
import random
import math
from scipy.special import comb


def init_user_buffer(user_count):
    user_buffer = dict()
    for i in range(user_count):
        user_buffer[i] = -1
    return user_buffer


def markov_chain(user_count, lambda_array):
    matrix_size = user_count + 1
    theoretic_average_size_array = []
    theoretic_delay_array = []
    p = 1 / user_count
    m = user_count

    for intensity in lambda_array:
        y = math.exp(-intensity)
        q = 1 - y

        matrix = np.zeros((matrix_size, matrix_size), dtype=float)
        for i in range(0, matrix_size):
            for j in range(0, matrix_size):
                pr = i * p * ((1 - p) ** (i - 1))
                matrix[i][j] = \
                    comb(m - i, j - i) * (q ** (j - i)) * (y ** (m - j)) * (1 - pr) \
                    + comb(m - i, j - i + 1) * (q ** (j - i + 1)) * (y ** (m - j - 1)) * pr
        print(matrix)

        matrix = np.transpose(matrix)
        for i in range(0, matrix_size):
            matrix[i, i] -= 1  # из диагонали вычитаем еденицы
            matrix[-1][i] = 1  # нижнюю строчку еденицами

        vector = np.array([0] * (user_count + 1))
        vector[user_count] = 1

        matrix_temp = np.linalg.solve(matrix, vector)  # matrix_temp = Pi

        temp_average = 0
        for j in range(0, matrix_size):
            temp_average += j * matrix_temp[j]
        theoretic_average_size_array.append(temp_average)

        lambda_out = temp_average * p * (1 - p) ** (temp_average - 1)
        theoretic_delay_array.append(temp_average / lambda_out)

    return theoretic_average_size_array, theoretic_delay_array


def simulate_aloha(message_count, user_count, lambda_array):
    delay_array = []
    average_size_array = []
    requests_array = []
    send_probability = 1 / user_count

    for intensity in lambda_array:
        user_buffer = init_user_buffer(user_count)
        count_sent_message = 0  # количество переданных заявок
        window_number = 0  # номер окна
        delay = 0  # задержка
        average_size = 0  # количество заявок в системе
        requests = 0  # количество сгенерированных заявок

        while count_sent_message < message_count:
            time = random.expovariate(intensity)
            requests += 1
            while time < 1:
                user_number = np.random.randint(user_count)
                if user_buffer[user_number] == -1:
                    user_buffer[user_number] = window_number
                time += random.expovariate(intensity)

            ready_users = []
            for i in range(user_count):  # Формируем массив абонентов, которые собираются передавать в этом окне
                if user_buffer[i] != -1 and user_buffer[i] != window_number:
                    if np.random.uniform() < send_probability:
                        ready_users.append(i)

            if len(ready_users) == 1:  # успех
                delay += window_number - user_buffer[ready_users[0]]
                count_sent_message += 1
                user_buffer[ready_users[0]] = -1

            for user in range(user_count):
                if user_buffer[user] != -1:
                    average_size += 1
            window_number += 1

        delay_array.append(delay / count_sent_message)
        average_size_array.append(average_size / window_number)
        requests_array.append(count_sent_message / requests)

    theoretic_average_size_array, theoretic_delay_array = markov_chain(user_count, lambda_array / user_count)

    plot.figure()
    plot.xlabel('lambda')
    plot.ylabel('M[D] and M[N]')
    plot.plot(lambda_array, delay_array, color='red', label='M[D]')
    plot.plot(lambda_array, average_size_array, color='blue', label='M[N]')
    plot.plot(lambda_array, theoretic_average_size_array, color='green', label='M[N] markov_chain')
    # plot.plot(lambda_array, requests_array, color='pink', label='lambda_out')
    plot.plot(lambda_array, theoretic_delay_array, color='black', label='M[D] markov_chain')
    plot.plot()
    plot.legend()
    plot.show()


def main():
    lambda_array = np.arange(0.1, 5.1, 0.1)
    user_count = 30
    message_count = 100000

    simulate_aloha(message_count, user_count, lambda_array)


main()
