# Промоделировать работу системы массового обслуживания с ограниченной очередью
# размеров b. Оценить путем моделирования среднее количество заявок в системе E[N] и
# среднюю задержку E[D]. Также произвести теоретический расчет двух данных величин.
# среднее число сообщений в очереди, используя формулу Литла
import matplotlib.pyplot as plot
import numpy as np
import random
import math


def theoretical_markov_chain(buffer_size):
    matrix_size = buffer_size + 1
    lambda_array = np.arange(0.1, 2.1, 0.1)
    theoretic_average_size_array = []
    theoretic_delay_array = []

    for intensity in lambda_array:
        matrix = np.zeros((matrix_size, matrix_size), dtype=float)

        for i in range(0, matrix_size - 1):  # заполняем первую и вторую строчку, кроме последнего элемента
            matrix[0, i] = matrix[1, i] = math.pow(intensity, i) * np.exp(-intensity) / math.factorial(i)
        matrix[0, matrix_size - 1] = 1 - sum(matrix[0])
        matrix[1, matrix_size - 2] = 0

        for i in range(2, matrix_size - 1):
            index = 0
            for j in range(i - 1, matrix_size - 2):
                matrix[i, j] = math.pow(intensity, index) * np.exp(-intensity) / math.factorial(index)
                index += 1
            matrix[i, matrix_size - 2] = 1 - sum(matrix[i])
        matrix[matrix_size - 1][matrix_size - 2] = 1

        matrix = np.transpose(matrix)

        for i in range(0, matrix_size):
            matrix[i, i] -= 1  # из диагонали вычитаем еденицы
            matrix[-1][i] = 1  # нижнюю строчку еденицами

        vector = np.array([0] * (buffer_size + 1))
        vector[buffer_size] = 1

        matrix_temp = np.linalg.solve(matrix, vector)  # matrix_temp = Pi

        temp_average = 0
        for j in range(0, matrix_size):
            temp_average += j * matrix_temp[j]
        theoretic_average_size_array.append(temp_average)

        lambda_out = 1 - matrix_temp[0]  # matrix_temp = Pi
        theoretic_delay_array.append(temp_average / lambda_out)

    return theoretic_delay_array, theoretic_average_size_array


def system(buffer_size, count_message):
    lambda_array = np.arange(0.1, 2.1, 0.1)
    delay_array = []
    average_size_array = []

    for intensity in lambda_array:
        buffer = []
        count_sent_message = 0  # количество обработанных заявок
        count_window = 0  # номер окна
        delay = 0  # задержка
        average_size = 0  # среднее количество заявок в системе

        while count_sent_message != count_message:
            time = random.expovariate(intensity)
            while time < 1:
                if len(buffer) < buffer_size:
                    buffer.append(count_window)
                time += random.expovariate(intensity)

            if len(buffer) != 0 and buffer[0] != count_window:
                in_time = buffer.pop(0)
                out_time = count_window
                delay += (out_time - in_time)
                count_sent_message += 1

            count_window += 1
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
    count_message = 10000  # количество заявок

    system(buffer_size, count_message)


main()
