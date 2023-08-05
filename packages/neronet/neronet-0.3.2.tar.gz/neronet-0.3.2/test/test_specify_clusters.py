import unittest
import tempfile
import os
import shutil

import neronet.neroman as neroman
import neronet.config_parser as config_parser


class TestSpecifyClusters(unittest.TestCase):    
    
    def setUp(self):
        self.folder = tempfile.mkdtemp()
        self.clusterpath = 'clusters.yaml'
        os.chdir(self.folder)
        with open(self.clusterpath, 'w') as f:
            f.write("clusters:\n"
                    "   triton:\n"
                    "       ssh_address: triton.aalto.fi\n"
                    "       type: slurm\n"
                    "\n"
                    "groups: null\n")
        self.testman = neroman.Neroman(clusters_file = self.clusterpath)
    
    def tearDown(self):
        shutil.rmtree(self.folder)

    def test_load_clusters_from_clusters_yaml(self):
        self.assertEqual(self.testman.clusters['clusters']['triton']\
                        ['ssh_address'], 'triton.aalto.fi')
        self.assertEqual(self.testman.clusters['clusters']['triton']\
                        ['type'], 'slurm')

    def test_specify_clusters_normal(self):
        self.testman.specify_cluster('testcluster', 
                                    'testcluster.com', 'unmanaged')
        self.assertEqual(self.testman.clusters['clusters']['testcluster']\
                        ['type'], 'unmanaged')
        self.assertEqual(self.testman.clusters['clusters']['testcluster']\
                        ['ssh_address'], 'testcluster.com')

    def test_specify_clusters_bad_cluster_type(self):
        self.assertRaises(config_parser.FormatError, 
                self.testman.specify_cluster, 'testcluster',
                             'testcluster.com', 'badclustertype')


if __name__ == '__main__':
    unittest.main()
