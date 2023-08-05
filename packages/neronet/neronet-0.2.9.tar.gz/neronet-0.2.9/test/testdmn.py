# -*- coding: utf-8 -*-
"""This module defines a test daemon for development purposes."""

import sys
import neronet.daemon
import subprocess
import pickle

class Testdmn(neronet.daemon.Daemon):

    """A class to test the Daemon class."""

    def __init__(self, name):
        super(Testdmn, self).__init__('testdmn-%s' % (name))

class TestdmnCli(neronet.daemon.Cli):

    """A class to test the Daemon class."""

    def __init__(self, dmn):
        super(TestdmnCli, self).__init__(dmn)
        self.funcs.update({
            'input': self.func_input,
            'output': self.func_output,
        })

    def func_input(self):
        """Read stdin."""
        print('Reading stdin...')
        byts = ''
        for ln in sys.stdin:
            print('Read %d bytes ("%s").' % (len(ln), ln))
            byts += ln
        print('Reading finished!')
        data = pickle.loads(byts)
        print('Received %s' % (data))

    def func_output(self):
        """Write to stdin."""
        proc = subprocess.Popen(['python', 'test/testdmn.py', 'in', '--input'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE)
        print('Communicating...')
        data = {'val': 1, 'str': 'I love honeybees'}
        out, err = proc.communicate(pickle.dumps(data, -1))
        rv = proc.poll()
        print('Finished: %d, "%s", "%s"' % (rv, out, err))

def main():
    """Create a CLI interface object and process CLI arguments."""    
    name = 'default'
    if len(sys.argv) >= 2 and sys.argv[1][0] != '-':
        name = sys.argv[1]
        sys.argv.pop(1)
    cli = TestdmnCli(Testdmn(name))
    cli.parse_arguments()

if __name__ == '__main__':
    main()