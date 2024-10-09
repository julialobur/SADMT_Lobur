import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate

# функція для виводу матриці порівнянь
def print_matrix(matrix, row_names, col_names):
    formatted_matrix = np.column_stack((row_names, matrix))
    print(tabulate(formatted_matrix, headers=[''] + col_names, showindex=False, floatfmt=".2f"))

# функція для обчислення геометричного середнього для рядка матриці
def g_mean(row: np.array):
    return np.prod(row) ** (1 / row.shape[0])

# функція для обчислення ваг критеріїв або альтернатив
def calculate_weights(matrix: np.array):
    weights = np.array([g_mean(row) for row in matrix])
    norm_weights = weights / np.sum(weights)
    matrix_with_weights = np.column_stack((matrix, weights, norm_weights))
    return matrix_with_weights

# функція для виводу матриці з вагами, з додаванням заголовку
def process_and_print_matrix(matrix, row_names, col_names, title):
    matrix_with_weights = calculate_weights(matrix)
    print(f'{title}:')
    print_matrix(matrix_with_weights, row_names, col_names)
    print('\n')
    return matrix_with_weights

# функція для перевірки узгодженості матриці за методом Сааті
def check_consistency(matrix, printSteps=False):
    nRows = matrix.shape[0]
    sum_row = np.sum(matrix[:, :-2], axis=0)

    m_lambda = np.dot(sum_row, matrix[:, -1])
    ic = (m_lambda - nRows) / (nRows - 1)

    cc_table = [0, 0, 0.58, 0.90, 1.12, 1.24, 1.32, 1.41, 1.45, 1.49]
    cc = cc_table[nRows - 1]
    oc = ic / cc

    if printSteps:
        print('Власне значення матриці: {:.2f}'.format(m_lambda))
        print('Індекс узгодженості: {:.2f}'.format(ic))
        print('Середнє значення індексу узгодженості:', cc)
        print('Відношення узгодженості: {:.2%}'.format(oc))
        print('\nДумки експерта узгоджені' if oc < 0.1 else 'Думки експерта не узгоджені')
        print('\n')

    return oc < 0.1

# функція для обчислення глобальних пріоритетів
def calculate_global_priorities(criterion_weights, alt_priorities):
    return np.dot(alt_priorities, criterion_weights)

# функція для візуалізації результатів
def visualize_results(global_priorities, alt_names):
    labels = ['A1', 'A2', 'A3', 'A4']
    
    # стовпчаста діаграма
    plt.figure(figsize=(10, 5))
    plt.bar(alt_names, global_priorities, color=['yellow', 'orange', 'green', 'blue'])
    plt.title('Глобальні пріоритети секретарів')
    plt.xlabel('Секретарі')
    plt.ylabel('Глобальний пріоритет')
    plt.ylim(0, 1)
    plt.axhline(y=max(global_priorities), color='g', linestyle='--')
    plt.show()

    # пелюсткова діаграма (радіальна)
    angles = np.linspace(0, 2 * np.pi, len(global_priorities), endpoint=False).tolist()
    values = np.concatenate((global_priorities, [global_priorities[0]])) 
    angles += angles[:1]
    
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.fill(angles, values, color='violet', alpha=0.25)
    ax.plot(angles, values, color='violet', linewidth=2)

    ax.set_yticklabels([]) 
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)

    plt.title('Пелюсткова діаграма глобальних пріоритетів')
    plt.show()

# основна функція для обчислень
def main():
    # матриця критеріїв
    comparison_matrix_criteria = np.array([
        [1, 1/5, 1/7],
        [5, 1, 1/3],
        [7, 3, 1],
    ])
    criterion_names = ['K1', 'K2', 'K3']
    col_names_criteria = criterion_names + ['Wi', 'Wнорм']
    comparison_matrix_criteria = process_and_print_matrix(comparison_matrix_criteria, criterion_names, col_names_criteria, 'Матриця парних порівнянь')

    # перевірка узгодженості
    check_consistency(comparison_matrix_criteria, printSteps=True)

    # альтернативи за К1
    comparison_matrix_k1 = np.array([
        [1, 3, 1/5, 2],
        [1/3, 1, 1/7, 5],
        [5, 7, 1, 3],
        [1/2, 1/5, 1/3, 1]
    ])
    alt_names = ['A1', 'A2', 'A3', 'A4']
    col_names_alternatives = alt_names + ['Wi', 'Wнорм']
    comparison_matrix_k1 = process_and_print_matrix(comparison_matrix_k1, alt_names, col_names_alternatives, 'Вибір секретаря, зважаючи на знання ПК (К1)')
    check_consistency(comparison_matrix_k1)

    # альтернативи за К2
    comparison_matrix_k2 = np.array([
        [1, 1/3, 1/7, 1/2],
        [3, 1, 1/5, 2],
        [7, 5, 1, 3],
        [2, 1/2, 1/3, 1]
    ])
    comparison_matrix_k2 = process_and_print_matrix(comparison_matrix_k2, alt_names, col_names_alternatives, 'Вибір секретаря, зважаючи на англійську мову (К2)')
    check_consistency(comparison_matrix_k2)

    # альтернативи за К3
    comparison_matrix_k3 = np.array([
        [1, 5, 1/3, 4],
        [1/5, 1, 1/7, 1/2],
        [3, 7, 1, 2],
        [1/4, 2, 1/2, 1]
    ])
    comparison_matrix_k3 = process_and_print_matrix(comparison_matrix_k3, alt_names, col_names_alternatives, 'Вибір секретаря, зважаючи на вміння комунікувати (К3)')
    check_consistency(comparison_matrix_k3)

    # обчислення пріоритетів за критеріями
    criterion_weights = comparison_matrix_criteria[:, -1]

    # матриця пріоритетів альтернатив за кожним критерієм
    alt_priorities = np.column_stack([
        comparison_matrix_k1[:, -1],
        comparison_matrix_k2[:, -1],
        comparison_matrix_k3[:, -1]
    ])

    # глобальні пріоритети
    global_priorities = calculate_global_priorities(criterion_weights, alt_priorities)

    # вивід результатів
    print_matrix(global_priorities.reshape(-1, 1), alt_names, ['Глобальний пріоритет'])

    best_alt = alt_names[np.argmax(global_priorities)]
    print(f'\nСекретар {best_alt} є найкращою альтернативою.')

    # візуалізація результатів
    visualize_results(global_priorities, alt_names)
    
main()