import sys
import json
import itertools
import numpy as np
import statistics
from glob import glob
import os
from pathlib import Path
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def kappa_coef(val1, val2):
    total = len(val1.keys())
    agreed = 0
    val1_relevant = 0
    val2_relevant = 0
    for k, v in val1.items():
        if v == val2[k]:
            agreed += 1
        if v:
            val1_relevant += 1

    for k, v in val2.items():
        if v:
            val2_relevant += 1

    val1_nonrelevant = total - val1_relevant
    val2_nonrelevant = total - val2_relevant
    p_a = agreed/total
    p_rel = (val1_relevant/total)*(val2_relevant/total)
    p_nonrel = (val1_nonrelevant/total)*(val2_nonrelevant/total)
    p_e = p_rel + p_nonrel
    return (p_a - p_e)/(1 - p_e)

if __name__ == "__main__":
    validations = []
    files = glob(os.path.join('validations', 'assessor_*'))
    assert(len(files) > 1)
    for filename in files:
        with open(filename) as f:
            data = json.load(f)

        queries = data['queries']
        validation = dict()
        validation['name'] = filename
        validation['data'] = dict()
        for query in queries:
            for value in query['data']:
                validation['data'][(query['query'], value['url'])] = value['relevant']
        validations.append(validation)

    
    combinations = itertools.combinations(validations, 2)
    kappas = []
    df = []
    for val1, val2 in combinations:
        kappa = kappa_coef(val1['data'], val2['data'])
        print(f"The Cohen's kappa coefficient between {val1['name']} and {val2['name']} is {kappa}")
        kappas.append(kappa)
        df.append({
            'assessor1': Path(val1['name']).name,
            'assessor2': Path(val2['name']).name,
            'kappa': kappa
        })
    if len(kappas) > 1:
        print(f"The average of the pair-wise coefficients is: {statistics.mean(kappas)}")
        df = pd.DataFrame(df)
        df['assessors'] = df.apply(lambda row: row.assessor1 + row.assessor2, axis=1)
        df.drop(['assessor1', 'assessor2'], axis=1, inplace=True)
        df.set_index('assessors', inplace=True)
        print(df)
        sns_plot = sns.clustermap(df, cmap="YlGnBu", col_cluster=False)
        sns_plot.savefig('kappa.png')
