alternatives = [
    [85, 30, 22, 0.65, 6],
    [60, 20, 10, 0.6, 7],
    [30, 12, 5, 0.45, 5],
    [75, 24, 13, 0.7, 8],
    [40, 15, 7, 0.55, 7]]

weights = [7, 5, 6, 8, 6]

min_values = [min(column) for column in zip(*alternatives)]
max_values = [max(column) for column in zip (*alternatives)]

normalized_alternatives = []
for alternative in alternatives:
    normalized_alternative = []
    for i, (value, min_val, max_val) in enumerate(zip(alternative, min_values, max_values)):
        if i == 1:
            normalized_value = (max_val - value) / (max_val - min_val)
        else:
            normalized_value = (value - min_val) / (max_val - min_val)
        normalized_alternative.append(normalized_value)
    normalized_alternatives.append(normalized_alternative)

calculated_values = [sum(value * weight for value, weight in zip(alternative, weights)) for alternative in normalized_alternatives]

alternatives_names = ['A1', 'A2', 'A3', 'A4', 'A5']

highest_alternative_value = max(calculated_values)
highest_alternative_index = calculated_values.index(highest_alternative_value) 
highest_alternative = alternatives_names [highest_alternative_index]

print(f"Всі альтернативи: {calculated_values}")
print(f"Найкраща альтернатива: {highest_alternative}")
print(f"Максимальна функція корисності: {highest_alternative_value}")