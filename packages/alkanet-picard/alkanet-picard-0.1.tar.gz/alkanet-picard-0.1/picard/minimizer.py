'''
    Minimizer Class
'''
import time
import numpy as np
from hyperopt import fmin, tpe, STATUS_OK
from keras.optimizers import RMSprop

from picard.parse_hypermodel import parse_config
from picard.build_model import build_model

class Minimizer(object):
    '''
        An experiment determined by
            - training & testing data
            - a search space
            - a hyperopt trials object
    '''

    def __init__(self, data=None, space_config=None, trials=None):
        self.data = data
        self.space = parse_config(space_config)
        self.trials = trials

    def eval_model(self, model_config):
        '''
            train model on data
        '''
        model = build_model(model_config)
        rms = RMSprop()
        model.compile(loss='categorical_crossentropy', optimizer=rms)

        model.fit(
            np.array(self.data['xTrain']),
            np.array(self.data['yTrain']),
            show_accuracy=True,
            verbose=1,
            validation_data=(
                np.array(self.data['xTest']),
                np.array(self.data['yTest'])
            ),
            **(model_config['fit'])
        )

        score, acc = model.evaluate(
            np.array(self.data['xTest']),
            np.array(self.data['yTest']),
            show_accuracy=True,
            verbose=1
        )

        weights_file_name = './tmp/weights/' + str(time.time()) +'.h5'
        model.save_weights(weights_file_name)
        return {
            'loss': -acc,
            'status': STATUS_OK,
            'modelConfig': model_config,
            'modelJSON': model.to_json(),
            'score': score,
            'weights_file': weights_file_name
        }

    def get_min_model(self, algo=tpe.suggest, max_evals=5, rseed=1234):
        minParams = fmin(
            self.eval_model,
            space=self.space,
            trials=self.trials,

            algo=algo,
            max_evals=max_evals,
            rseed=rseed
        )

        return get_min_trial(minParams, self.trials)['result']

def get_min_trial(min_params, trials):

    for trial in trials:

        params = trial['misc']['vals']


        for key in params.keys():
            if not params[key]:
                params.pop(key, None)
            else:
                params[key] = params[key][0]

        if params == min_params:
            return trial