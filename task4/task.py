import math
from collections import Counter


def entropy(probabilities):
    return -sum(p * math.log2(p) for p in probabilities if p > 0)


def joint_entropy(joint_dist):
    total_count = sum(joint_dist.values())
    probabilities = (count / total_count for count in joint_dist.values())
    return entropy(probabilities)


def marginal_distribution(joint_dist, mode):
    marginal = Counter()
    for (sum_key, prod_key), count in joint_dist.items():
        key = sum_key if mode == "sum" else prod_key
        marginal[key] += count
    return marginal


def dice_joint_distribution():
    outcomes = [(i, j) for i in range(1, 7) for j in range(1, 7)]
    return Counter((i + j, i * j) for i, j in outcomes), len(outcomes)


def main():
    # Генерация совместного распределения и общего числа исходов
    joint_dist, total_outcomes = dice_joint_distribution()

    H_AB = joint_entropy(joint_dist)

    marginal_sum = marginal_distribution(joint_dist, mode="sum")
    marginal_prod = marginal_distribution(joint_dist, mode="prod")


    H_A = entropy(count / total_outcomes for count in marginal_sum.values())
    H_B = entropy(count / total_outcomes for count in marginal_prod.values())

    H_B_given_A = H_AB - H_A
    I_AB = H_B - H_B_given_A

    # Округленные результаты
    return [round(H_AB, 2), round(H_A, 2), round(H_B, 2), round(H_B_given_A, 2), round(I_AB, 2)]


if __name__ == "__main__":
    print(main())
