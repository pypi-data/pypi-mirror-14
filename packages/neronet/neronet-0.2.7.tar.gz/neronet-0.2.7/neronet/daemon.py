# daemon.py

"""
Classes to make it possible to create asynchronous processes that can be
communicated with.
"""

import os
import sys
import time
import signal
import traceback
import socket
import pickle
import re
import datetime
import shutil
#import threading

import neronet.core

TIMEOUT = 3.0

class Query():
  """A daemon query class."""

  def __init__(self, name, callback):
    self.name = name
    self.callback = callback
    self.tprocess = 0
    self.scsc = 0
    self.errc = 0

  def process(self, *args, **kwargs):
    try:
      #print('process:', self.callback, args, kwargs)
      rv = self.callback(*args, **kwargs)
      self.scsc += 1
      self.tprocess = time.time()
      return rv
    except Exception as err:
      self.errc += 1
      raise err

class Daemon(object):
    """A generic daemon class.

    See:
    - https://www.python.org/dev/peps/pep-3143/
    - https://docs.python.org/3.5/library/socketserver.html
    - http://stackoverflow.com/questions/15652791/how-to-create-a-python-socket-listner-deamon

    Attributes:
      name (str): Name of daemon process. Must be unique.
      pdir (str): The directory to contain the daemon files (see below)
      pfin (str): The file path for standard input
      pfout (str): The file path for standard output
      pferr (str): The file path for standard error
      pfpid (str): The file path for storing the process ID number
      pfport (str): The file path for storing the socket port number
      queries (dict): The dictionary that contains all the Queries the
        daemon listens to.
      trun (int): The start timestamp of the `run` method
      port (int): The socket port number
      host (int): The hostname of the system
      tdo (float): The socket timeout
      sckt (int): The socket object
    """

    class NoPidFileError(Exception):
        pass

    def __init__(self, name, tdo=TIMEOUT):
        self._name = name
        self._pdir = os.path.join(os.path.expanduser('~/.neronet'), self._name)
        self._pfin = os.path.join(self._pdir, 'in')
        self._pfout = os.path.join(self._pdir, 'out')
        self._pferr = os.path.join(self._pdir, 'err')
        self._pfpid = os.path.join(self._pdir, 'pid')
        self._pfport = os.path.join(self._pdir, 'port')
        self._queries = {}
        self.add_query('uptime', self.qry_uptime)
        self.add_query('status', self.qry_status)
        self.add_query('stop', self.qry_stop)
        self._trun = 0
        self._port = 0
        self._host = neronet.core.get_hostname() # FIXME kosh != kosh.aalto.fi
        self._tdo = tdo
        self._sckt = None

    def add_query(self, name, callback):
        self._queries[name] = Query(name, callback)

    def _log_pform(self, prefix, message):
        return '%s %s  %s\n' % (prefix,
            time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
            message)

    def log(self, message):
        sys.stdout.write(self._log_pform('LOG', message))
        sys.stdout.flush()

    def wrn(self, message):
        sys.stdout.write(self._log_pform('WRN', message))
        sys.stdout.flush()

    def err(self, message, err=None):
        output = self._log_pform('ERR', message)
        sys.stdout.write(output)
        sys.stdout.flush()
        if err:
            sys.stderr.write(output)
            traceback.print_exc()
            sys.stderr.write('\n')
        else:
            sys.stderr.write(output)
        sys.stderr.flush()

    def abort(self, message, err=None):
        self.err(message, err)
        self._quit()

    def _read_i_or_nan(self, pf):
        try: return int(neronet.core.read_file(pf))
        except: return None

    def _rpfpid(self):
        self._pid = self._read_i_or_nan(self._pfpid)
        return self._pid

    def _rpfport(self):
        self._port = self._read_i_or_nan(self._pfport)
        return self._port

    def _cleanup(self, outfiles=False):
        """Remove daemon instance related files.

        Returns:
            int: The number of files removed."""
        self.log('cleanup(): Removing instance related files...')
        file_paths = [self._pfpid, self._pfport] + \
            ([self._pfout, self._pferr] if outfiles else [])
        #self.log('cleanup(): Files: %s' % (file_paths))
        remove_count = 0
        for pf in file_paths:
            if os.path.exists(pf):
                self.log('cleanup(): Removing "%s"...' % (pf))
                shutil.move(pf, pf + '.old')
                remove_count += 1
        return remove_count

    def _quit(self):
        self._cleanup(outfiles=True)
        self.log("quit(): Exiting... Bye!")
        sys.exit(0)

    def _recv_signal(self, sign, frme):
        self.log('recv_signal(): Received signal "%s"!' % (sign))
        if sign in (signal.SIGTERM, signal.SIGQUIT):
            self._quit()

    def _daemonize(self):
        """Daemonize the process.

        Essentially
        - Daemonizes the process by double forking
        - Redefines a few variables and a few handles to unix signals
        - Defines stdout, stderr and logging streams
        - Writes the pid file
        """
        self.log("daemonize(): Daemonizing the process...")

        # Exit first parent (first fork)
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError as err:
            self.err('daemonize(): Fork #1 failed!', err=err)
            sys.exit(1)

        # Decouple from parent environment and make sure we have a clean
        # daemon directory to store log output etc.
        os.umask(0027)
        if os.path.exists(self._pdir):
            # Clean up any daemon related files and wait for any possible
            # existing deamon to notice the cleanup and exit and then cleanup
            # again
            remove_count = self._cleanup(outfiles=True)
            if remove_count > 0:
                self.wrn('daemonize(): %d files had to be cleaned!' %
                        (remove_count))
                time.sleep(self._tdo)
                self._cleanup(outfiles=True)
        else:
            os.mkdir(self._pdir)
        os.chdir(self._pdir)
        os.setsid() # create a session and set the process group ID

        # Do second fork
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError as err:
            self.err('daemonize(): Fork #2 failed!', err=err)
            sys.exit(1)

        ## Standard IO redirection
        # Flush the standard output streams
        sys.stdout.flush()
        sys.stderr.flush()
        # Initialize an input stream file
        neronet.core.write_file(self._pfin, '')
        # Open new IO streams
        si = open(self._pfin, 'r')
        so = open(self._pfout, 'w')
        se = open(self._pferr, 'w')
        # Duplicate the new streams to replace the standard ones and close
        # the existing standard file descriptors if open
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        # Update PID
        self._pid = os.getpid()
        self.log('daemonize(): Forked to PID = %d...' % (self._pid))
        neronet.core.write_file(self._pfpid, self._pid)

        # Add signal handlers
        self.log('daemonize(): Adding a signal handler...')
        signal.signal(signal.SIGTERM, self._recv_signal)
        signal.signal(signal.SIGQUIT, self._recv_signal)

        # Print encoding info
        import locale
        self.log(
            'daemonize(): Encodings: %s (system), %s (preferred)...' %
            (sys.getfilesystemencoding(), locale.getpreferredencoding()))

        self.log("daemonize(): Attributes:")
        self.log("daemonize():   time    %s" % (datetime.datetime.now()))
        self.log("daemonize():   name    %s" % (self._name))
        self.log("daemonize():   pdir    %s" % (self._pdir))
        self.log("daemonize():   pfout   %s" % (self._pfout))
        self.log("daemonize():   pferr   %s" % (self._pferr))
        self.log("daemonize():   cwd     %s" % (os.getcwd()))
        self.log("daemonize():   pid     %s" % (self._pid))

    def _run(self):
        """The daemon process loop."""
        # Create a socket with a timeout and bind it to any available port on
        # localhost
        sckt = socket.socket()
        sckt.settimeout(self._tdo)
        sckt.bind(('0.0.0.0', self._port))
        # Put the socket into server mode and retrieve the chosen port number
        sckt.listen(1)
        host, self._port = sckt.getsockname()
        neronet.core.write_file(self._pfport, self._port)
        self.log('run(): Listening at (%s, %d)...' % (host, self._port))
        self._trun = time.time()
        self._doquit = False
        while not self._doquit:
            self.log('run(): Looping...')
            try:
                conn, addr = sckt.accept()
                self.log('run(): Handling...')
                self._handle(conn)
            except socket.timeout:
                self.log('run(): Timeout...')
                self.ontimeout()
            except socket.error as err:
                self.err('run(): Socket error: %s' % (socket.error), err)
            #thread = threading.Thread(target=self.handle, args=[conn])
            #thread.daemon = True
            #thread.start()
            if self._read_i_or_nan(self._pfpid) != self._pid:
                self.log('run(): PID file altered! Aborting...')
                self._doquit = True
        self._quit()

    def _handle(self, conn):
        self.log('Handle %s...' % (str(conn.getsockname())))
        conn.settimeout(self._tdo/6)
        result = ''
        try:
            while True:
                self.log('Receiving data...')
                byts = conn.recv(2048)
                if byts:
                    result += byts
                else:
                    break
        except socket.timeout:
            pass
        data = pickle.loads(result)
        self.log('Received %s' % (data))
        self._uptime = time.time() - self._trun
        self._reply = {'rv': 9, 'uptime': self._uptime}
        if data and 'name' in data:
            name = data['name']
            args = data['args'] if 'args' in data else []
            kwargs = data['kwargs'] if 'kwargs' in data else {}
            if name in self._queries:
                self.log('Running query "%s" with %s %s...' % (name, args, kwargs))
                self._queries[name].process(*args, **kwargs)
            else:
                self._reply['msgbody'] = 'Unsupported query "%s"!' % (name)
        self.log('Sending the reply %s...' % (self._reply))
        # Send the reply to the connected socket
        conn.sendall(pickle.dumps(self._reply, -1))

    def qry_uptime(self):
        self._reply['rv'] = 0

    def qry_status(self):
        self._reply['msgbody'] = 'Hi! I\'m alive since %d secs!' % (self._uptime)
        self._reply['rv'] = 0

    def qry_stop(self):
        self._reply['msgbody'] = 'Ok but I\'m sad to say good bye!'
        self._reply['rv'] = 0
        self._doquit = True

    def ontimeout(self):
        """
        You should override this method when you subclass Daemon. It will
        be called if the process does not receive input.
        """
        pass

class QueryInterface(object):

    class NoPortFileError(RuntimeError): pass
    class NoPortNumberError(RuntimeError): pass
    class ConnectError(RuntimeError): pass

    def __init__(self, daemon, port=None, host='127.0.0.1', verbose=False):
        self.daemon = daemon
        self.port = port
        self.host = host
        self.verbose = verbose
        try:
            self.determine_port()
        except self.NoPortFileError:
            pass

    def inf(self, msg):
        if not self.verbose: return
        print(msg)

    def wrn(self, msg):
        if not self.verbose: return
        print('WRN: %s' % (msg))

    def err(self, msg):
        if not self.verbose: return
        print('ERR: %s' % (msg))

    def abort(self, code, msg):
        print('ABORT: %s' % (msg))
        sys.exit(code)

    def determine_port(self):
        if self.port:
            return
        localhost = neronet.core.get_hostname()
        if self.host in ('127.0.0.1', 'localhost', localhost):
            if os.path.exists(self.daemon._pfport):
                self.port = int(neronet.core.read_file(self.daemon._pfport))
            else:
                raise self.NoPortFileError('No daemon port file at "%s"!'
                        % (self.daemon._pfport))
                #self.abort(10, 'No daemon port file found! Is it running?')
        else:
            raise self.NoPortNumberError('No daemon port number!')
            #self.abort(10, 'No daemon port number defined!')

    def query(self, name, *pargs, **kwargs):
        trials = 4
        self.determine_port()
        self.inf('Query "%s" with %s, %s to (%s, %s)...' % (name, pargs,
                kwargs, self.host, self.port))
        if name not in self.daemon._queries:
            raise RuntimeError('No such query "%s"!' % (name))
            #self.abort(11, 'No such query "%s"!' % (name))
        # Create a TCP/IP socket
        sckt = socket.socket()
        sckt.settimeout(self.daemon._tdo)
        # Connect to the daemon
        for i in range(trials):
            try:
                sckt.connect((self.host, self.port))
                data = {'name': name, 'args': pargs, 'kwargs': kwargs}
                #self.inf('Sending data...')
                sckt.sendall(pickle.dumps(data, -1))
                #self.inf('Listening for a reply...')
                try:
                    byts = sckt.recv(4096)
                    data = pickle.loads(byts) if byts else None
                    self.inf('Received reply: %s' % (data))
                except socket.timeout:
                    self.inf('No reply received!')
                    data = None
                #self.inf('Closing socket.')
                sckt.close()
                return data
            except socket.error:
                time.sleep(0.3)
        raise self.ConnectError('Unable to connect to the daemon at %s, %s!'
                % (self.host, self.port))
        #self.abort(11, 'Unable to connect to the daemon.')

    def daemon_is_alive(self):
        try:
            reply = self.query('uptime')
            if not reply or 'uptime' not in reply:
                return False
            uptime = reply['uptime']
            return uptime > 0 if uptime != None else False
        except self.NoPortFileError:
            return False
        except self.ConnectError:
            return None

    def cleanup(self):
        """Erase daemon instance related files."""
        self.daemon._cleanup(outfiles=True)

    def start(self):
        """Start the daemon."""
        self.inf('start(): Starting the daemon...')
        if self.daemon_is_alive():
            self.wrn('start(): The daemon is already running!')
            return
        # Fork a new thread that starts the daemon
        pid = os.fork()
        if pid == 0:
            self.daemon._daemonize()
            self.inf('start(): Executing run...')
            self.daemon._run()

    def stop(self):
        """Stop the daemon."""
        if not self.daemon_is_alive():
            self.wrn('stop(): The daemon is not even running!')
            return
        self.inf('stop(): Stopping the daemon...')
        self.query('stop')
        time.sleep(self.daemon._tdo*0.5)
        if os.path.exists(self.daemon._pfport):
            self.wrn('stop(): The daemon failed to cleanup!')
            self.daemon._cleanup(outfiles=True)
        else:
            self.inf("stop(): The daemon exited cleanly.")

    def restart(self):
        """Restart the daemon."""
        self.inf("restart(): Restarting the daemon...")
        self.stop()
        self.start()

class Cli(QueryInterface):
    """A base class for easy control of daemons."""

    #RE_ARG = re.compile(r'--(\w+) (\w+)* (\w+=\w+)*')
    ## Command line argument parser regexes
    # Function name identifier
    RE_FUNC = re.compile(r'--([\w.]+)')
    # Keyword argument
    RE_KARG = re.compile(r'([\w.]+=.*)')
    # Positional argument
    RE_PARG = re.compile(r'(.*)')

    def __init__(self, daemon):
        super(Cli, self).__init__(daemon, verbose=True)
        self.funcs = {
            'default': self.func_default,
            'cleanup': self.func_cleanup,
            'start': self.func_start,
            'stop': self.func_stop,
            'restart': self.func_restart,
            'query': self.func_query,
            'input': self.func_input
        }

    def parse_arguments(self, cli_args=None):
        """
        Parse and execute CLI arguments.

        The arguments must be in format:
          '--func parg kwarg=kwvalue'

        The default function is always executed. Pos. and keyw. arguments
        parsed before any '--func' arguments are found are given to default.
        """
        #self.inf('Parse arguments: %s' % (sys.argv))
        cli_args = cli_args if cli_args else sys.argv[1:]
        work_queue = []
        pargs = []
        kargs = {}
        # Before any '--func' arguments are found, give all found pos. arguments
        # and keyword arguments to the default function
        work_queue.append(('default', pargs, kargs))
        # Go through and parse the arguments, organizing them into a queue of
        # function calls with their positional and key word arguments
        for arg in cli_args:
            #self.inf('Parsing argument "%s"...' % (arg))
            mtch = self.RE_FUNC.match(arg)
            if mtch:
                func = mtch.group(1)
                pargs = []
                kargs = {}
                work_queue.append((func, pargs, kargs))
                continue
            mtch = self.RE_KARG.match(arg)
            if mtch:
                kargs[mtch.group(1)] = mtch.group(2)
                continue
            mtch = self.RE_PARG.match(arg)
            if mtch:
                pargs.append(mtch.group(1))
                continue
            self.abort(1, 'Unrecognized argument: "%s"' % (arg))
        # Go through the work queue and execute the functions
        for func, pargs, kargs in work_queue:
            if func in self.funcs:
                #self.inf('Executing function "%s" with %s %s...' 
                #    % (func, pargs, kargs))
                self.funcs[func](*pargs, **kargs)
            else:
                self.abort(2, 'Unrecognized function: "%s"' % (func))

    def func_default(self):
        pass

    def func_cleanup(self):
        """Erase daemon instance related files."""
        self.cleanup()

    def func_start(self):
        """Start the daemon."""
        self.start()

    def func_stop(self):
        """Stop the daemon."""
        self.stop()

    def func_restart(self):
        """Restart the daemon."""
        self.restart()

    def func_query(self, name, *pargs, **kwargs):
        reply = self.query(name, *pargs, **kwargs)
        if not reply:
            self.err('No reply received!')
        else:
            self.inf('Received a reply with code %d.' % (reply['rv']))
            if 'msgbody' in reply:
              self.inf('Message:\n%s' % (reply['msgbody']))

    def func_input(self):
        """Read data input from stdin."""
        print('Reading stdin...')
        byts = ''
        for ln in sys.stdin:
            print('Read %d bytes ("%s").' % (len(ln), ln))
            byts += ln
        print('Reading finished!')
        data = pickle.loads(byts)
        print('Received %s' % (data))
        try:
            reply = self.query('input', data)
        except self.NoPortFileError:
            reply = {'rv': 1, 'msgbody': 'No port file!'}
        print('Reply %s' % (reply))