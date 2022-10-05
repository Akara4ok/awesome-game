import itertools
from itertools import permutations

def flatten(l):
    return [item for sublist in l for item in sublist]


def divideArray(my_list, n):
    return [my_list[i * n:(i + 1) * n] for i in range((len(my_list) + n - 1) // n )]


def getAllSingleArrayCombinations(a):
    result = a[0]
    for index, comb in enumerate(a[1:]):
        result = list(itertools.product(result, comb))
        flatten = []
        if (index >= 1):
            for res in result:
                flatten.append((*res[0], res[1]))
            result = flatten

    return result

def getAllArrayCombinations(a, b):
    all_combinations = list(itertools.product(a, b))
    # printing unique_combination list
    divided_combinations = divideArray(all_combinations, len(b))

    result = divided_combinations[0]
    for index, comb in enumerate(divided_combinations[1:]):
        result = list(itertools.product(result, comb))
        flatten = []
        if (index >= 1):
            for res in result:
                flatten.append((*res[0], res[1]))
            result = flatten


    
    
    return result