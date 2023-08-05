import unittest
from core import ExperimentWarning, Cluster, Experiment

class Core_test(unittest.TestCase):
    
    def test_experiment_warning(self):
        
        w = ExperimentWarning("name", "var1", 50.0, "gt", "immediately", "kill")
        self.assertEqual(w.get_action("war 50"), "no action")
        self.assertEqual(w.get_action("var1 nfasdjk"), "no action")
        self.assertEqual(w.get_action("var1 50"), "no action")
        self.assertEqual(w.get_action("var1 49"), "no action")
        self.assertEqual(w.get_action("var1 51"), "kill")
        
        w = ExperimentWarning("name", "var1", 35.0, "lt", "immediately", "kill")
        self.assertEqual(w.get_action("var1 35"), "no action")
        self.assertEqual(w.get_action("var1 34"), "kill")
        self.assertEqual(w.get_action("var1 36"), "no action")
        
        w = ExperimentWarning("name", "var1", 50.0, "geq", "immediately", "kill")
        self.assertEqual(w.get_action("var1 50"), "kill")
        self.assertEqual(w.get_action("var1 49"), "no action")
        self.assertEqual(w.get_action("var1 51"), "kill")
        
        w = ExperimentWarning("name", "var1", 50.0, "leq", "immediately", "warn")
        self.assertEqual(w.get_action("var1 50"), "warn")
        self.assertEqual(w.get_action("var1 49"), "warn")
        self.assertEqual(w.get_action("var1 51"), "no action")
        
        w = ExperimentWarning("name", "var1", 50.01, "eq", "immediately", "email")
        self.assertEqual(w.get_action("var1 50.01"), "email")
        self.assertEqual(w.get_action("var1 49"), "no action")
        self.assertEqual(w.get_action("var1 51"), "no action")
        
        w = ExperimentWarning("name", "var2", 50, "geq", "time 6000", "email")
        self.assertEqual(w.get_action("var2 50"), "no action")
        self.assertEqual(w.get_action("var2 49"), "no action")
        self.assertEqual(w.get_action("var2 51"), "no action")
        
        w = ExperimentWarning("name", "variable", 50, "geq", "time 0", "email")
        self.assertEqual(w.get_action("variable 50"), "email")
        self.assertEqual(w.get_action("variable 49"), "no action")
        self.assertEqual(w.get_action("variable 51"), "email")
        self.assertEqual(w.get_action("var1 51"), "no action")
    
    def test_cluster_str(self):
        
        c = Cluster("triton","slurm", "triton.aalto.fi")
        self.assertEqual(c.__str__(), "triton (slurm, triton.aalto.fi)")
        
        c = Cluster("kosh","unmanaged", "kosh.aalto.fi")
        self.assertEqual(c.__str__(), "kosh (unmanaged, kosh.aalto.fi)")
        
        #TODO: write more tests for different cluster methods
        
    def test_experiment_get_action(self):
        
        c = {'name' : ExperimentWarning("name", "var1", 50.0, "gt", "immediately", "kill")}
        e = Experiment("exp1", "python", "run.py",
                    {'param1': 20, 'param2' : 30}, "{param1} {param2}", "", conditions=c)
        
        self.assertEqual(e.get_action("var1 60"), ("kill", "name"))
        self.assertEqual(e.get_action("var1 49.9999"), ("no action", ""))
        
    def test_experiment_callstring(self):
    
        c = {'name' : ExperimentWarning("name", "var1", 50.0, "gt", "immediately", "kill")}
        e = Experiment("exp1", "python", "run.py",
                    {'param1': 20, 'param2' : 30}, "{param1} {param2}", "", conditions=c)
                    
        self.assertEqual(e.callstring, "python run.py 20 30")
    
    def test_experiment_set_warning(self):
        
        c = {'name' : ExperimentWarning("name", "var1", 50.0, "gt", "immediately", "kill")}
        e = Experiment("exp1", "python", "run.py",
                    {'param1': 20, 'param2' : 30}, "{param1} {param2}", "", conditions=c)
                       
        self.assertEqual(e.has_warnings(), "")
        self.assertEquals(e.get_warnings(), [])
        
        e.set_warning("name")
        
        self.assertEqual(e.has_warnings(), "WARNING")        
        self.assertIsNotNone(e.get_warnings()[0])
    
    def test_experiment_state(self):
        
        c = {'name' : ExperimentWarning("name", "var1", 50.0, "gt", "immediately", "kill")}
        e = Experiment("exp1", "python", "run.py",
                    {'param1': 20, 'param2' : 30}, "{param1} {param2}", "", conditions=c)
        
        self.assertEqual(len(e._fields['states_info']), 1)
        e.update_state(Experiment.State.submitted)
        self.assertEqual(len(e._fields['states_info']), 2)
        
        #TODO: write more tests
        
        

if __name__ == '__main__':
    unittest.main()
