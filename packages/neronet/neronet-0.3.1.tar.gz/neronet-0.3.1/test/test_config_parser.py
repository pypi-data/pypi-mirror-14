import unittest
import tempfile
import os
import shutil

import yaml

import neronet.config_parser as cp

def ltd(l):
    exps = {}
    for exp in l:
        exps[exp.experiment_id] = exp.fields
    return exps

class TestConfigParser(unittest.TestCase):

    def setUp(self):
        
        self.testfolder = tempfile.mkdtemp()
        os.chdir(self.testfolder)
        self.expfolder = tempfile.mkdtemp(dir = self.testfolder)
        self.path = os.path.join(self.expfolder, cp.CONFIG_FILENAME)

        self.fields = ['run_command_prefix', 'main_code_file', 'parameters', 
                        'parameters_format']
        self.values = ['test_runner', 'main_code', {'n': 1}, '{n}']
        with open(self.path, 'w') as f:
            f.write(yaml.dump(dict(zip(self.fields + ['test'],
                                        self.values + [None])), 
                                        default_flow_style=False))
        self.parser = cp.ConfigParser()

    def tearDown(self):
        shutil.rmtree(self.testfolder)

    def test_no_experiment_folder(self):
        with self.assertRaises(FileNotFoundError):
            self.parser.parse_experiments('/not_a_existing_folder')
    
    def test_no_config_file(self):
        empty_folder = tempfile.mkdtemp(dir = self.expfolder)
        with self.assertRaises(FileNotFoundError):
            self.parser.parse_experiments(empty_folder)

    def test_empty_config_file(self):
        open(self.path, 'w').close()
        with self.assertRaises(cp.FormatError):
            self.parser.parse_experiments(self.expfolder)

    def test_missing_field_in_config_file(self):
        self.fields += ['test1']
        self.values += [None]
        n = len(self.fields)
        for err in range(n):
            fields = self.fields[0:err] + self.fields[err+1:n] 
            values = self.values[0:err] + self.values[err+1:n]
            with open(self.path, 'w') as f:
                f.write(yaml.dump(dict(zip(fields, values)),
                                  default_flow_style=False))
            with self.subTest(missing_field=self.fields[err]):
                with self.assertRaises(cp.FormatError):
                    self.parser.parse_experiments(self.expfolder)
                    
    def test_parse_simple_experiment(self):
        experiments = self.parser.parse_experiments(self.expfolder)
        experiments = ltd(experiments)
        for field, value in zip(self.fields, self.values):
            with self.subTest(value=value):
                self.assertEqual(experiments['test'][field], value)
    
    def test_parse_experiment_with_simple_inheritance(self):
        with open(self.path, 'w') as f:
            f.write(yaml.dump(dict(zip(self.fields + ['test1'],
                                        self.values + [{'test2': None}])), 
                                default_flow_style=False))
        experiments = self.parser.parse_experiments(self.expfolder)
        experiments = ltd(experiments)
        for experiment in ['test1', 'test2']:
            with self.subTest(experiment=experiment):
                for field, value in zip(self.fields, self.values):
                    self.assertEqual(experiments[experiment][field], value)

    def test_parse_experiment_with_inheritance_overriding(self):
        overrides = ['other_test_runner', 'other_main_code', {'n': 3}, '{n} {n}']
        for field, override in zip(self.fields, overrides):
            with self.subTest(override=field):
                with open(self.path, 'w') as f:
                    f.write(yaml.dump(dict(zip(self.fields + ['test1'],
                        self.values + [{'test2': {field: override}}])), 
                                default_flow_style=False))
                experiments = self.parser.parse_experiments(self.expfolder)
                experiments = ltd(experiments)
                for field2, value in zip(self.fields, self.values):
                    self.assertEqual(experiments['test1'][field2], value)
                    if field == field2:
                        self.assertEqual(experiments['test2'][field2],
                                        override)
                    else:
                        self.assertEqual(experiments['test2'][field2], value)

    def test_parse_experiment_with_simple_combinations(self):
        self.values[-2]['n'] = [1,2]
        self.values[-2]['x'] = [3,4]
        values = [{'n':1, 'x':3},{'n':2, 'x':3},{'n':1, 'x':4},{'n':2, 'x':4}]
        with open(self.path, 'w') as f:
            f.write(yaml.dump(dict(zip(self.fields + ['test'],
                                        self.values + [None])), 
                                default_flow_style=False))
        experiments = self.parser.parse_experiments(self.expfolder)
        experiments = ltd(experiments)
        experiment_ids = ['test_n-1_x-3', 'test_n-2_x-3',
                            'test_n-1_x-4', 'test_n-2_x-4']
        for i, experiment in enumerate(experiment_ids):
            with self.subTest(experiment=experiment):
                for field, value in zip(self.fields, self.values):
                    if field == 'parameters':
                        self.assertEqual(experiments[experiment][field], 
                                        values[i])
                    else:
                        self.assertEqual(experiments[experiment][field], value)

def print_experiments(experiments):
    for experiment_id in sorted(experiments.keys()):
        print("Experiment", experiment_id)
        experiment = experiments[experiment_id]
        for field in sorted(experiment.keys()):
            print(field, experiment[field])

if __name__ == "__main__":
    unittest.main()
