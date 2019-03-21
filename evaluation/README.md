## Evaluation
This module is responsible for evaluating the system based on assessors judgements.

## Checker
Each assessor has a validation output (JSON format). The script checker.py will check they all are consistent in terms of queries and documents judged.

### Run
~~~
python checker.py
~~~
No need of parameters, it will read from the _validation_ folder.

## Cohen's kappa coefficient
To ensure the reliability of the judged documents, we compute the cohen's kappa coefficient for the inter-assessor agreement. This coefficient will tell us how reliable the judgments are and it is only computable between two assessors. In case of having more than two assessors, it computes the average of the pairwise coefficients.

### Run
~~~
python kappa_coefficient.py
~~~
No need of parameters, it will read from the _validation_ folder.

## Merge evaluations
*TODO*

## Offline metrics
They all are query oriented:
- Unranked evaluation
    - Precision
- Ranked evaluation
    - Precision at rank k (we will try k = {2,5}) - P@2, P@5
    - Reciprocal rank: 1/rank of first relevant item
    - Average precision (AP)
- User-oriented evaluation
    - Normalized DCG

### Run
~~~
python calculate_metrics.py
~~~
No need of parameters, it will read from the validation/global.json
