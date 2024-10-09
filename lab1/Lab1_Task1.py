alternatives = [
    [3, 7, 2, 9],
    [8, 3, 6, 7],
    [4, 8, 3, 5],
    [9, 6, 5, 4]]

weights = [8, 9, 6, 7]

calculated_values = [sum(value * weight for value, weight in zip(alternative, weights)) for alternative in alternatives]

alternatives_names = ['A1', 'A2', 'A3', 'A4']

highest_alternative_value = max(calculated_values)
highest_alternative_index = calculated_values.index(highest_alternative_value)
highest_alternative = alternatives_names[highest_alternative_index]

print(f"Всі функції корисності альтернатив: {calculated_values}")
print(f"Найкраща альтернатива: {highest_alternative}")
print(f"Максимальна функція корисності: {highest_alternative_value}")