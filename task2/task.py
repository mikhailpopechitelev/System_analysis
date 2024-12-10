import csv
import sys
from collections import defaultdict, deque


def read_edges_from_csv(file_path):
    with open(file_path, 'r') as csv_file:
        return [tuple(map(int, row)) for row in csv.reader(csv_file)]


def build_adjacency_lists(edges):
    adjacency_list = defaultdict(list)
    reverse_adjacency_list = defaultdict(list)
    for parent, child in edges:
        adjacency_list[parent].append(child)
        reverse_adjacency_list[child].append(parent)
    return adjacency_list, reverse_adjacency_list


def calculate_l_values(edges, node_count):
    adjacency_list, reverse_adjacency_list = build_adjacency_lists(edges)


    l_values = [[0] * 5 for _ in range(node_count)]


    for parent, children in adjacency_list.items():
        l_values[parent - 1][0] = len(children)
        for child in children:
            l_values[child - 1][1] += 1

    for node in range(1, node_count + 1):
        visited = set()
        queue = deque([(node, 0)])

        while queue:
            current, depth = queue.popleft()
            if current in visited:
                continue
            visited.add(current)
            if depth > 1:
                l_values[node - 1][2] += 1
                l_values[current - 1][3] += 1
            for neighbor in adjacency_list[current]:
                queue.append((neighbor, depth + 1))

    # Подсчет количества братьев и сестер
    for node in range(1, node_count + 1):
        siblings = set()
        for parent in reverse_adjacency_list[node]:
            siblings.update(adjacency_list[parent])
        siblings.discard(node)
        l_values[node - 1][4] = len(siblings)

    return l_values


def output_l_values(l_values):
    return '\n'.join(','.join(map(str, row)) for row in l_values)


def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_csv_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    edges = read_edges_from_csv(file_path)
    node_count = max(max(pair) for pair in edges)
    l_values = calculate_l_values(edges, node_count)
    print(output_l_values(l_values))


if __name__ == "__main__":
    main()
