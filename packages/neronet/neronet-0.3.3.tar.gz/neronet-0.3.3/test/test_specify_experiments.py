import unittest
import tempfile
import os
import shutil

import neronet.neroman as neroman
import neronet.config_parser as config_parser


class TestSpecifyExperiments(unittest.TestCase):    
    
    def setUp(self):
        
        #Create a testfolder and specify config filenames
        self.testfolder = tempfile.mkdtemp()
        os.chdir(self.testfolder)
        self.database_file = "default.yaml"
        self.preferences_file = "preferences.yaml"
        self.clusters_file = "clusters.yaml"
        with open(self.database_file, 'w') as f:
            f.write("experiment1:\n"
                    "   cluster: null\n"
                    "   collection: exps\n"
                    "   main_code_file: party.py\n"
                    "   parameters:\n"
                    "        when: now\n"
                    "   run_command_prefix: python3\n"
                    "   parameters_format: 'when'\n"
                    "state: defined\n"
                    "cluster:\n"
                    "time_created: 15:12:01 12-12-2014")
        
        #Initialize Neroman with database
        self.testman = neroman.Neroman(self.database_file,
                                        self.preferences_file, 
                                        self.clusters_file)
        #Create an experiment folder
        self.expfolder = tempfile.mkdtemp(dir = self.testfolder)
        self.path = os.path.join(self.expfolder, config_parser.CONFIG_FILENAME)
        with open(self.path, 'w') as f:
            f.write("run_command_prefix: python\n"
                    "main_code_file: sleep.py\n"
                    "collection: test\n"
                    "parameters:\n"
                    "   count: 5\n"
                    "   interval: 5\n"
                    "parameters_format:\n"
                    "   '{count} {interval}'\n"
                    "sleep_demo:\n")
    
    def tearDown(self):
        shutil.rmtree(self.testfolder)

    def test_no_experiment_folder(self):
        with self.assertRaises(FileNotFoundError):
            self.testman.specify_experiments('/nonexistent')


    def test_no_config_file_in_folder(self):
        empty_folder = tempfile.mkdtemp(dir = self.testfolder)
        with self.assertRaises(FileNotFoundError):
            self.testman.specify_experiments(empty_folder)

    def test_empty_config_file(self):
        open(self.path, 'w').close()
        with self.assertRaises(config_parser.FormatError):
            self.testman.specify_experiments(self.expfolder)

    def test_read_experiment(self):
        self.testman.specify_experiments(self.expfolder)
        fields = ['run_command_prefix', 'main_code_file', 
                'parameters', 'parameters_format']
        values = ['python', 'sleep.py', {'count': 5, 'interval': 5}, 
                '{count} {interval}']
        for i, field in enumerate(fields):
            with self.subTest(field=field):
                self.assertEqual(values[i], 
                                self.testman.experiments['sleep_demo'][field])

    def test_badly_formatted_config_file(self):
        with open(self.path, 'w') as f:
            f.write("run_command_prefix: python\n"
                    "parameters:\n"
                    "   count: 5\n"
                    "   interval: 5\n"
                    "parameters_format:\n"
                    "   'count interval'\n")
        with self.assertRaises(config_parser.FormatError):
            self.testman.specify_experiments(self.expfolder)


if __name__ == '__main__':
    unittest.main()
