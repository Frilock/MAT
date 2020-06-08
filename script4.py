# Промоделировать работу системы массового обслуживания с ограниченной очередью
# размеров b. Оценить путем моделирования среднее количество заявок в системе E[N] и
# среднюю задержку E[D]. Также произвести теоретический расчет двух данных величин.
# среднее число сообщений в очереди, используя формулу Литла
import matplotlib.pyplot as plot
import random
import numpy as np
import math


def theoretical_markov_chain(buffer_size):
    matrix_size = buffer_size + 1
    lambda_array = np.arange(0.1, 1.1, 0.1)
    theoretic_average_size_array = []
    theoretic_delay_array = []

    for intensity in lambda_array:
        matrix = [[0] * matrix_size] * matrix_size
        matrix = np.asarray(matrix, dtype=float)

        for i in range(0, matrix_size - 1):  # заполняем первую строчку, кроме последнего элемента
            matrix[0, i] = matrix[1, i] = math.pow(intensity, i) * np.exp(-intensity) / math.factorial(i)
        matrix[0, matrix_size - 1] = 1 - sum(matrix[0])
        matrix[1, matrix_size - 2] = 0

        for i in range(2, matrix_size - 1):
            index = 0
            for j in range(i - 1, matrix_size - 2):
                matrix[i, j] = math.pow(intensity, index) * np.exp(-intensity) / math.factorial(index)
                index += 1

        for i in range(1, matrix_size):
            matrix[i, matrix_size - 2] = 1 - sum(matrix[i])

        matrix[matrix_size - 1, matrix_size - 2] = 1

        for i in range(0, matrix_size):
            matrix[i, i] -= 1

        matrix = np.transpose(matrix)
        matrix[matrix_size - 1] = np.array([1] * matrix_size)

        vector = np.array([0] * (buffer_size + 1))
        vector[buffer_size] = 1

        matrix_temp = np.linalg.solve(matrix, vector)

        temp_average = 0
        for j in range(0, len(matrix_temp)):
            temp_average += j * matrix_temp[j]
        theoretic_average_size_array.append(temp_average)

        lambda_out = 1 - matrix_temp[0]  # matrix_temp = Pi
        theoretic_delay_array.append(temp_average / lambda_out)

    return theoretic_delay_array, theoretic_average_size_array


def system(buffer_size, count_message):
    lambda_array = np.arange(0.1, 1.1, 0.1)
    delay_array = []
    average_size_array = []

    for intensity in lambda_array:
        time = 0
        buffer = []
        count_sent_message = 0  # количество обработанных заявок
        count_window = 0  # номер окна
        delay = 0  # задержка
        average_size = 0  # среднее количество заявок в системе
        count_request = 0  # заявок сгенерировано

        while count_sent_message != count_message:
            count_window += 1
            while time <= count_window:
                count_request += 1
                time += np.random.poisson(1 / intensity)
                # time += random.expovariate(intensity)
                if len(buffer) <= buffer_size and time <= count_window:
                    buffer.append(time)

            if len(buffer) != 0:
                in_time = buffer.pop()
                out_time = count_window + 1
                delay += (out_time - in_time)
                count_sent_message += 1

            average_size += len(buffer)

        average_size /= count_sent_message
        delay /= count_sent_message
        delay_array.append(delay)
        average_size_array.append(average_size)

    theoretic_delay_array, theoretic_average_size_array = \
        theoretical_markov_chain(buffer_size)

    plot.figure()
    plot.xlabel('lambda')
    plot.ylabel('delay and M[N]')
    plot.plot(lambda_array, delay_array, color='red', label='delay')
    plot.plot(lambda_array, average_size_array, color='blue', label='M[N]')
    plot.plot(lambda_array, theoretic_delay_array, color='green', label='theoretic delay')
    plot.plot(lambda_array, theoretic_average_size_array, color='black', label='theoretic M[N]')
    plot.legend()
    plot.show()


def main():
    buffer_size = 10  # размер очереди
    count_message = 1000  # количество заявок

    system(buffer_size, count_message)
    # theoretical_markov_chain(buffer_size)


main()
