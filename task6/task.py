import json


def membership_function(value, points):
    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]
        if x1 <= value <= x2:
            # Линейная интерполяция между двумя точками
            return y1 + (value - x1) * (y2 - y1) / (x2 - x1)
    return 0  # Если значение не попадает в интервал


def fuzzify(value, fuzzy_sets):
    membership = {}
    for fuzzy_set in fuzzy_sets:
        term_id = fuzzy_set["id"]
        points = fuzzy_set["points"]
        membership[term_id] = membership_function(value, points)
    return membership


def apply_rules(temp_membership, rules, heating_sets):
    heating_membership = {}
    for rule in rules:
        temp_term = rule[0]
        heating_term = rule[1]
        if temp_term in temp_membership:
            degree = temp_membership[temp_term]
            if heating_term not in heating_membership:
                heating_membership[heating_term] = degree
            else:
                heating_membership[heating_term] = max(heating_membership[heating_term], degree)
    return heating_membership


def defuzzify(heating_membership, heating_sets):
    numerator = 0
    denominator = 0
    for heating_set in heating_sets:
        term_id = heating_set["id"]
        points = heating_set["points"]
        if term_id in heating_membership:
            degree = heating_membership[term_id]
            # Центроид функции принадлежности
            area = 0
            center = 0
            for i in range(len(points) - 1):
                x1, y1 = points[i]
                x2, y2 = points[i + 1]
                trapezoid_area = (y1 + y2) * (x2 - x1) / 2
                trapezoid_center = (x1 + x2) / 2
                area += trapezoid_area
                center += trapezoid_area * trapezoid_center
            if area > 0:
                centroid = center / area
                numerator += centroid * degree
                denominator += degree
    return numerator / denominator if denominator != 0 else 0


def task(temp_sets_json, heating_sets_json, rules_json, current_temp):
    temp_sets = json.loads(temp_sets_json)["температура"]
    heating_sets = json.loads(heating_sets_json)["температура"]
    rules = json.loads(rules_json)

    temp_membership = fuzzify(current_temp, temp_sets)

    heating_membership = apply_rules(temp_membership, rules, heating_sets)
    
    return defuzzify(heating_membership, heating_sets)


# Пример использования
if __name__ == "__main__":
    temp_sets_json = json.dumps({
        "температура": [
            {
                "id": "холодно",
                "points": [[0, 1], [18, 1], [22, 0], [50, 0]]
            },
            {
                "id": "комфортно",
                "points": [[18, 0], [22, 1], [24, 1], [26, 0]]
            },
            {
                "id": "жарко",
                "points": [[0, 0], [24, 0], [26, 1], [50, 1]]
            }
        ]
    })

    heating_sets_json = json.dumps({
        "температура": [
            {
                "id": "слабый",
                "points": [[0, 0], [0, 1], [5, 1], [8, 0]]
            },
            {
                "id": "умеренный",
                "points": [[5, 0], [8, 1], [13, 1], [16, 0]]
            },
            {
                "id": "интенсивный",
                "points": [[13, 0], [18, 1], [23, 1], [26, 0]]
            }
        ]
    })

    rules_json = json.dumps([
        ["холодно", "интенсивный"],
        ["комфортно", "умеренный"],
        ["жарко", "слабый"]
    ])

    current_temp = 20  # Пример текущей температуры
    result = task(temp_sets_json, heating_sets_json, rules_json, current_temp)
    print(f"Результат управления: {result}")
