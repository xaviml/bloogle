import sys
import json
from glob import glob
import os


def check(data, filename):
    queries = data['queries']
    if len(queries) != 10:
        print(f'{filename} has {len(queries)} queries')
        return False
    for query in queries:
        if len(query['data']) != 10:
            print(
                f'{filename} has {len(query["data"])} elements for the query: {query["query"]}')
            return False
    return True


if __name__ == "__main__":
    paths = glob(os.path.join('validations', '*'))
    for filename in paths:
        with open(filename) as f:
            data = json.load(f)

        try:
            checked_passed = check(data, filename)
        except:
            checked_passed = False

        if checked_passed:
            print(f'{filename} passed all the tests')
        else:
            print(f'{filename} did not pass the tests')
