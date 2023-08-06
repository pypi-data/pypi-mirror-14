import unittest
import tempfile
import os
import shutil

import neronet.neroman as neroman
import neronet.config_parser as config_parser


class TestStatusReport(unittest.TestCase):    
    
    def setUp(self):
        #Create a testfolder and specify config filenames
        self.testfolder = tempfile.mkdtemp()
        os.chdir(self.testfolder)
        self.database_file = "default.yaml"
        self.preferences_file = "preferences.yaml"
        self.clusters_file = "clusters.yaml"
        #Create test config files
        with open(self.clusters_file, 'w') as f:
            f.write("clusters:\n"
                    "   triton:\n"
                    "       ssh_address: triton.aalto.fi\n"
                    "       type: slurm\n"
                    "\n"
                    "groups: null\n")
        
        
        #Initialize Neroman
        self.testman = neroman.Neroman(self.database_file,
                                        self.preferences_file, 
                                        self.clusters_file)
        #Create an experiment folder and submit it to Neroman
        self.expfolder = tempfile.mkdtemp(dir = self.testfolder)
        self.path = os.path.join(self.expfolder, config_parser.CONFIG_FILENAME)
        with open(self.path, 'w') as f:
            f.write("experiment_id: sleep_demo\n"
                    "run_command_prefix: python\n"
                    "main_code_file: sleep.py\n"
                    "parameters:\n"
                    "   count: 5\n"
                    "   interval: 5\n"
                    "parameters_format:\n"
                    "   'count interval'")
        self.testman.specify_experiments(self.expfolder)
    
    def tearDown(self):
        shutil.rmtree(self.testfolder)

    def test_experiment_is_defined(self):
        self.assertEqual(
            self.testman.experiments['sleep_demo']['state'].pop()[0], 
            'defined')

if __name__ == '__main__':
    unittest.main()
