import unittest

import neronet.core

class TestExperiment(unittest.TestCase):
    def setUp(self):
        self.test_dict = {'experiment_id': 'test', 
                                'run_command_prefix': 'python',
                                'main_code_file': 'exp.py',
                                'parameters': {'x': 1, 'y': 2},
                                'parameters_format': '{x} {y}',
                                'collection': 'tests',
                                'required_files': ['aux_file.txt'],
                                'conditions': 'termination',
                                'path': 'some_folder'}
        self.test_exp_dict = {self.test_experiment['experiment_id']: \
                            {key: value for key, value in \
                                self.test_experiment.items() \
                                if key != 'experiment_id'}}

        self.test_experiment = neronet.code.Experiment(**self.test_experiment)

    def test_create(self):
        exp_dict = self.test_experiment.as_dict()
        for exp_id in self.test_exp_dict.keys():
            self.assertIn(exp_id, exp_dict)
            for field in self.test_exp_dict[exp_id].keys():
                with self.subTest(field=field):
                    self.assertEqual(self.test_exp_dict[exp_id][field],
                                    exp_dict[exp_id][field])
