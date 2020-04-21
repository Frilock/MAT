# Смоделировать работу Марковской цепи с двумя состояниями за t шагов. Оценить
# вероятность того, что она окажется в i-ом состоянии на шаге t. Также произвести
# теоретический расчет данной вероятности.
import random
import matplotlib.pyplot as plt
import numpy as np

listPrState0 = []
listPrState1 = []
list_pr0 = []
list_pr1 = []


def theoretic(matrix):
    p0 = np.array([1, 0])
    for step in range(0, 100):
        p0 = p0.dot(matrix)
        list_pr0.append(p0[0])
        list_pr1.append(p0[1])


def probability(n, t, matrix):
    flag = True
    count_state0 = 0
    count_state1 = 0

    for j in range(0, n):
        for step in range(0, t):
            c = random.random()
            if flag:
                if c > matrix[0][0]:
                    flag = False
            else:
                if c > matrix[1][1]:
                    flag = True
        if flag:
            count_state0 += 1
        else:
            count_state1 += 1
    listPrState0.append(count_state0 / n)
    listPrState1.append(count_state1 / n)


def main():
    time_list = []
    matrix = np.array([[0.8, 0.2], [0.6, 0.4]])

    for t in range(0, 100):
        time_list.append(t)
        probability(5000, t, matrix)

    theoretic(matrix)

    plt.figure()
    plt.plot(time_list, listPrState0, color='red', label='State(0)')
    plt.plot(time_list, listPrState1, color='green', label='State(1)')
    plt.plot(time_list, list_pr0, color='blue', label='Theoretic(0)')
    plt.plot(time_list, list_pr1, color='black', label='Theoretic(1)')
    plt.legend()
    plt.xlabel('T(time)')
    plt.ylabel('Pr(probability)')
    plt.savefig('res1.png')
    plt.show()


main()
