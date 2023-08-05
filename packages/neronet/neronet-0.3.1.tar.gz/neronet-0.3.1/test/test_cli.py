import unittest

import neronet.nerocli as cli

class TestCLI(unittest.TestCase):
    
    def setUp(self):
        self.parser = cli.create_argument_parser()

    def test_specify_experiment(self):
        folder_name = 'test_folder'
        parsed = self.parser.parse_args(['--experiment', folder_name])
        self.assertTrue(parsed.experiment)
        self.assertEqual(parsed.experiment[0], folder_name)

    def test_specify_cluster(self):
        cluster_id = 'triton'
        ssh_address = 'triton.aalto.fi'
        cluster_type = 'slurm'
        parsed = self.parser.parse_args(['--cluster', 
                cluster_id, ssh_address, cluster_type])
        self.assertTrue(parsed.cluster)
        self.assertEqual(parsed.cluster[0], cluster_id)
        self.assertEqual(parsed.cluster[1], ssh_address)
        self.assertEqual(parsed.cluster[2], cluster_type)

    def test_specify_user(self):
        name = 'Juha Pekka'
        email = 'juha.pekka@supermail.orz'
        parsed = self.parser.parse_args(['--user', name, email])
        self.assertTrue(parsed.user)
        self.assertEqual(parsed.user[0], name)
        self.assertEqual(parsed.user[1], email)

    def test_status(self):
        parsed = self.parser.parse_args(['--status'])
        self.assertTrue(parsed.status)

if __name__ == '__main__': 
        unittest.main()

