import sys
import json
import itertools
import numpy as np
import os
import math


def calc_precission_at_k(rank, k):
    return sum(rank[:k])/k


def calc_precision(rank):
    return calc_precission_at_k(rank, len(rank))


def calc_average_precision(rank):
    precisions_at_k = [calc_precission_at_k(rank, idx+1) for idx, value in enumerate(rank) if value]
    return sum(precisions_at_k) / len(precisions_at_k)


def calc_reciprocal_rank(rank):
    return next((1/(idx+1) for idx, value in enumerate(rank) if value), None)


def calc_DCG(rank):
    # We are adding 2 in the denominator because the idx is 0-based index, so we need to add an extra 1
    return sum((math.pow(2, value)-1)/(math.log2(idx+2)) for idx, value in enumerate(rank))


def calc_normalized_DCG(rank):
    ideal_rank = sorted(rank, reverse=True)
    DCG = calc_DCG(rank)
    IDCG = calc_DCG(ideal_rank)
    return DCG/IDCG

"""Expected reciprocal rank"""
def err(rank, theta=1):
    rank = list(map(lambda r: r/max(rank), rank))
    err = 0
    for k, R_k in enumerate(rank, 1):
        # at k
        p = np.prod([1-R_i for idx_i, R_i in enumerate(rank[:k-1])])

        err += 1/k * p * R_k * (theta**(k-1))

    return err
if __name__ == "__main__":
    with open('validations/global.json') as f:
        data = json.load(f)
    
    queries = data['queries']
    for query in queries:
        relevancy = [elem['relevant'] for elem in query['data']]
        print(f'Query: {query["query"]}')
        print(f'Precision: {calc_precision(relevancy):.3f}')
        print(f'Precision at 2: {calc_precission_at_k(relevancy, 2):.3f}')
        print(f'Precision at 5: {calc_precission_at_k(relevancy, 5):.3f}')
        print(f'Reciprocal rank: {calc_reciprocal_rank(relevancy):.3f}')
        print(f'Average precision (AP): {calc_average_precision(relevancy):.3f}')
        print(f'DCG: {calc_DCG(relevancy):.3f}')
        print(f'Normalized DCG: {calc_normalized_DCG(relevancy):.3f}')
        print(f'Normalized DCG: {calc_normalized_DCG(relevancy):.3f}')
        print(f'Expected Reciprocal Rank: {err(relevancy, 1):.3f}')
        print()