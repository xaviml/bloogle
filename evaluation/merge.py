from glob import glob
import os
import json
import numpy as np

if __name__ == "__main__":
    paths = glob(os.path.join('validations', 'assessor_*'))
    datas = []
    for filename in paths:
        with open(filename) as f:
            data = json.load(f)
            datas.append(data)
    output = {**datas[0]}
    for idx_query, query in enumerate(output['queries']):
        for idx_data, _ in enumerate(query['data']):
            values = np.array([data['queries'][idx_query]['data'][idx_data]['relevant'] for data in datas if data['queries'][idx_query]['query'] == query['query']])
            output['queries'][idx_query]['data'][idx_data]['relevant'] = True if np.mean(values) > 0.5 else False
    
    path = os.path.join('validations', 'global.json')
    with open(path, 'w', encoding="utf-8") as f:
        json.dump(output,f)
    