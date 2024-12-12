import json


def main(rank_a_json, rank_b_json):
    rank_a = json.loads(rank_a_json)
    rank_b = json.loads(rank_b_json)


    position_a = {item: pos for pos, group in enumerate(rank_a) for item in (group if isinstance(group, list) else [group])}
    position_b = {item: pos for pos, group in enumerate(rank_b) for item in (group if isinstance(group, list) else [group])}


    disagreements = []
    for item1 in position_a:
        for item2 in position_a:
            if item1 != item2:
                a_condition = position_a[item1] < position_a[item2]
                b_condition = position_b[item1] > position_b[item2]
                if a_condition and b_condition:
                    disagreements.append({item1, item2})

    core_disagreements = []
    for disagreement in disagreements:
        if disagreement not in core_disagreements:
            core_disagreements.append(list(disagreement))

    return json.dumps(core_disagreements)



if __name__ == "__main__":
    rank_a = '[1,[2,3],4,[5,6,7],8,9,10]'
    rank_b = '[[1,2],[3,4,5],6,7,9,[8,10]]'
    print(main(rank_a, rank_b))


