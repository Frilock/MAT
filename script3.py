# Промоделировать работу Марковской цепи с одним поглощающим состоянием из трех.
# Путем моделирования оценить среднее время достижения поглощающего состояния и
# вычислить его теоретически.

import random
import numpy as np


def theoretical(matrix):
    vector = np.array([1, 1, 1])
    current_matrix = -matrix
    current_matrix[0][0] = 1 - matrix[0][0]
    current_matrix[1][1] = 1 - matrix[1][1]
    return np.linalg.inv(current_matrix).dot(vector)[0]


def practical(matrix, n):
    current_time = 0

    for j in range(0, n):
        current_state = 0
        while True:
            c = random.random()
            if current_state == 0:
                current_state = get_current_state(matrix, 0, c)
                current_time += 1
            elif current_state == 1:
                current_state = get_current_state(matrix, 1, c)
                current_time += 1
            else:
                current_time -= 1
                break
    return current_time / n


def get_current_state(matrix, i, c):
    if c < matrix[i][0]:
        return 0
    elif c < (matrix[i][0] + matrix[i][1]):
        return 1
    else:
        return 2


def main():
    matrix = np.array([[0.7, 0.2999, 0.0001], [0.6, 0.2999, 0.1001], [0, 0, 1]])
    n = 100000

    print("Среднее время до поглощяющего состояния (практика):", practical(matrix, n),
          "при количестве итераций равном", n)
    print("Среднее время до поглощающего состояния (теория):", theoretical(matrix))


main()
