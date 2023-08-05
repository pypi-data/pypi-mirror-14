import argparse
import codecs
import os

if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import kian.fitness
from kian import TrainedModel

parser = argparse.ArgumentParser(description='Evaluate a trained model')
parser.add_argument('--file', '-f', nargs='?', required=True,
                    help='name of the model to train')
args = parser.parse_args()

file_path = os.path.join(args.file)

if not os.path.isfile(file_path):
    raise ValueError('You should train the model first')
with codecs.open(file_path, 'r', 'utf-8') as f:
    cv_set = eval(f.read())
total_edits = len(cv_set[1]) + len(cv_set[0])
AUC = kian.fitness.AUC(cv_set)
print('AUC of the classifier: {0:.5}'.format(AUC))
thrashholds = []
for beta in [0.125,0.25,0.5,1,2,3,4]:
    res = kian.fitness.optimum_thrashhold(cv_set, beta)
    i = 0
    for case in (cv_set[0] + cv_set[1]):
        if case > res[0]:
            i += 1
    print('f{0}-score (thrashhold, precision, recall, edits to review, total edits):'
          ' {1:.5}, {2:.5}, {3:.5}, {4}, {5} ({6:.5}%)'.format(beta, res[0], res[1][0],
            res[1][1], i, total_edits, (i * 100) / total_edits))
