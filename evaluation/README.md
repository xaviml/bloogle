## Evaluation
This module is responsible for evaluating the system based on assessors judgements.

### Instructions for assessors
This section is for assessors to now what they are evaluating and how our system works. First of all, Bloogle is a blog post search engine. This means that all content is extracted from Blog pages, in our case:
- Medium
- Wired
- Gizmodo
- TechCrunch
- The Verge
- Steemit
- Buzzfeed

Most of our content is related to technolgy, so most of our queries will related to it.

The queries will be given to the assessor by the Bloogle team. However, is essential to know the features of the system. They are as follows:
- **Full text search.** You can search for an exact piece of text by wrapping the words between quotes. E.g.: "Machine learning"
- **Rule out terms.** It excludes a word by adding a prepended hyphen. E.g.: Machine learning -deep
- **Mandatory term.** It includes a word by adding a prepended plus sign. E.g.: Machine learning +deep

### Queries
These are the evaluated queries:
- machine learning
- machine learning online courses
- "apple" +fruit -ios
- "apple" -fruit +ios
- "deep learning" python
- angular vs. react
- artificial intelligence +jobs -steve
- steve jobs and bill gates
- itunes spotify
- quantum computer


## Offline metrics
They all are query oriented:
### Unranked evaluation
Precision

### Ranked evaluation
Precision at rank k (we will try k = 10) - P@10
Reciprocal rank: 1/rank of first relevant item
Average precision (AP)

#### User-oriented evaluation
DCG
Normalized DCG
