from __future__ import print_function
from hyperopt import Trials
import numpy as np
import random

from picard.minimizer import Minimizer

class SparkMinimizer(object):

    def __init__(self, sc, num_workers=4):
        self.spark_context = sc
        self.num_workers = num_workers

    def compute_trials(self, space, data, min_config):

        worker = Worker(
            self.spark_context.broadcast(space),
            self.spark_context.broadcast(data),
            self.spark_context.broadcast(min_config)
        )

        dummy_rdd = self.spark_context.parallelize([i for i in range(1, 1000)])
        dummy_rdd = dummy_rdd.repartition(self.num_workers)
        trials_list = dummy_rdd.mapPartitions(worker.minimize).collect()

        return trials_list

    def minimize(self, space, data, min_config):
        trials_list = self.compute_trials(
            space,
            data,
            min_config
        )

        best_val = 1e7
        for trials in trials_list:
            for trial in trials:
                val = trial.get('result').get('loss')
                if val < best_val:
                    best_val = val
                    best_model_json = trial['result']['model_JSON']
                    best_model_weights = trial['result']['weights_file']

        return {
            "modelJSON": best_model_json,
            "weights_file": best_model_weights
        }

class Worker(object):

    def __init__(self, spaceBC, dataBC, minConfigBC):
        self.space_config = spaceBC.value
        self.data = dataBC.value
        self.min_config = minConfigBC.value

    def minimize(self, dummy_iterator):
        trials = Trials()

        elem = dummy_iterator.next()
        random.seed(elem)
        rand_seed = np.random.randint(elem)

        minimizer = Minimizer(
            space_config=self.space_config,
            data=self.data,
            trials=trials
        )

        minimizer.get_min_model(
            rseed=rand_seed,
            **self.min_config
        )

        yield trials
