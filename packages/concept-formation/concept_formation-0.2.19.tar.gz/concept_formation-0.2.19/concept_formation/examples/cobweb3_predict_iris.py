from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

import matplotlib.pyplot as plt
import numpy as np

from concept_formation.examples.examples_utils import avg_lines
from concept_formation.predict import incremental_prediction
from concept_formation.cobweb3 import Cobweb3Tree
from concept_formation.dummy import DummyTree
from concept_formation.datasets import load_iris

num_runs = 30
num_examples = 30
irises = load_iris()

naive_data = incremental_prediction(DummyTree(), irises,
                                  run_length=num_examples,
                                  runs=num_runs, attr="class")
cobweb_data = incremental_prediction(Cobweb3Tree(alpha=0.01), irises,
                                  run_length=num_examples,
                                  runs=num_runs, attr="class")

naive_data.sort()
cobweb_data.sort()

cobweb_x, cobweb_y = [], []
naive_x, naive_y = [], []

for x,y in cobweb_data:
    cobweb_x.append(x)
    cobweb_y.append(y)
for x,y in naive_data:
    naive_x.append(x)
    naive_y.append(y)

cobweb_x = np.array(cobweb_x)
cobweb_y = np.array(cobweb_y)
naive_x = np.array(naive_x)
naive_y = np.array(naive_y)

cobweb_y_smooth, cobweb_lower_smooth, cobweb_upper_smooth = avg_lines(cobweb_x, cobweb_y)
naive_y_smooth, naive_lower_smooth, naive_upper_smooth = avg_lines(naive_x, naive_y)

plt.fill_between(cobweb_x, cobweb_lower_smooth, cobweb_upper_smooth, alpha=0.5,
                 facecolor="green")
plt.fill_between(naive_x, naive_lower_smooth, naive_upper_smooth, alpha=0.5,
                 facecolor="red")

plt.plot(cobweb_x, cobweb_y_smooth, label="COBWEB/3", color="green")
plt.plot(naive_x, naive_y_smooth, label="Naive Predictor", color="red")

plt.gca().set_ylim([0.00,1.0])
plt.gca().set_xlim([0,max(naive_x)-1])
plt.title("Incremental Iris Classification Prediction Accuracy")
plt.xlabel("# of Training Examples")
plt.ylabel("Avg. Probability of True Class (Accuracy)")
plt.legend(loc=4)

plt.show()
