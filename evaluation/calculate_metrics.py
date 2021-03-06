import sys
import json
import itertools
import numpy as np
import os
import math
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def checker(func):
    def wrapper(rank, *args, **kwargs):
        return 0 if sum(rank) == 0 else func(rank, *args, **kwargs)
    return wrapper

@checker
def calc_precision_at_k(rank, k):
    return sum(rank[:k])/k

@checker
def calc_average_precision(rank):
    precisions_at_k = [calc_precision_at_k(rank, idx+1) for idx, value in enumerate(rank) if value]
    return sum(precisions_at_k) / len(precisions_at_k)

@checker
def calc_reciprocal_rank(rank):
    return next((1/(idx+1) for idx, value in enumerate(rank) if value), 0)

@checker
def calc_DCG(rank):
    # We are adding 2 in the denominator because the idx is 0-based index, so we need to add an extra 1
    return sum((math.pow(2, value)-1)/(math.log2(idx+2)) for idx, value in enumerate(rank))

@checker
def calc_normalized_DCG(rank):
    ideal_rank = sorted(rank, reverse=True)
    DCG = calc_DCG(rank)
    IDCG = calc_DCG(ideal_rank)
    return DCG/IDCG

@checker
def calc_err(rank, theta=1):
    """Expected reciprocal rank"""
    rank = list(map(lambda r: r/max(rank), rank))
    err = 0
    for k, R_k in enumerate(rank, 1):
        # at k
        p = np.prod([1-R_i for R_i in rank[:k-1]])

        err += 1/k * p * R_k * (theta**(k-1))

    return err

if __name__ == "__main__":
    with open('validations/global.json') as f:
        data = json.load(f)
    
    df = []
    queries = data['queries']
    for query in queries:
        relevancy = [elem['relevant'] for elem in query['data']]
        precission_at_2 = calc_precision_at_k(relevancy, 2)
        precission_at_5 = calc_precision_at_k(relevancy, 5)
        precision_at_10 = calc_precision_at_k(relevancy, 10)
        reciprocal_rank = calc_reciprocal_rank(relevancy)
        average_precision = calc_average_precision(relevancy)
        normalized_DCG = calc_normalized_DCG(relevancy)
        item = {
            'query': query['query'],
            'precission at rank 2': precission_at_2,
            'precission at rank 5': precission_at_5,
            'precission at rank 10': precision_at_10,
            'reciprocal rank': reciprocal_rank,
            'average precision': average_precision,
            'normalized DCG': normalized_DCG
        }
        df.append(item)
        print(f'Query: {query["query"]}')
        print(f'Precision at 2: {precission_at_2:.3f}')
        print(f'Precision at 5: {precission_at_5:.3f}')
        print(f'Precision at 10: {precision_at_10:.3f}')
        print(f'Reciprocal rank: {reciprocal_rank:.3f}')
        print(f'Average precision (AP): {average_precision:.3f}')
        print(f'Normalized DCG: {normalized_DCG:.3f}')
        print()
    
    df = pd.DataFrame(df)
    df.set_index('query', inplace=True)
    sns_plot = sns.clustermap(df, cmap="YlGnBu", col_cluster=True)
    plt.setp(sns_plot.ax_heatmap.get_xticklabels(), rotation=45) # For x axis

    # The table that prints out is too long, we will need a way to make it fit
    # if we want to put the table on the report
    #print(df.to_latex(float_format='%.3f'))

    sns_plot.savefig('metrics.png')