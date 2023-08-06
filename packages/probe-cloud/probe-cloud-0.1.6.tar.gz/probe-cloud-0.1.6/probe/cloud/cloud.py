from .rdir_watcher import RDirWatcher
import logging
import subprocess
from multiprocessing import Process, Pipe
import time
import socket
import psutil
from psutil import NoSuchProcess, AccessDenied
from ConfigParser import SafeConfigParser
import sys, os
import signal
import copy
import paramiko
from probe.params import SimParams
import traceback

logger = logging.getLogger(__name__)

def clean_up(signalno, frame):

    logger.warning('cleanup, signalno: %s, frame: %s', signalno, frame)

    with open('pids.log') as f:
        lines = f.readlines()

    logger.debug('lines: %s', lines)

    parent_pid, child_pid, sim_pid = [pid.strip() for pid in lines[-1].split(',')]
    logger.warning('parent_pid: %s, child_pid: %s, sim_pid: %s', parent_pid, child_pid, sim_pid)

    logger.warning('killing CHILD: %s', child_pid)
    output = subprocess.check_output(['kill', '-9', child_pid])
    logger.warning('CHILD killed: %s', output)

    logger.warning('killing simulation: %s', sim_pid)
    output = subprocess.check_output(['kill', '-9', sim_pid])
    logger.warning('simulation killed: %s', output)

    sys.exit(0)

signal.signal(signal.SIGTERM, clean_up)

def run_cmd(pipe, cmd, stdout=None):
    '''
    This function starts a Popen process with specified command. Command has to be
    list of individual arguments (example: cmd = ['cat', 'a.out']). Note that stderr
    is automatically redirected to stdout. Stdout is by default printed to the screen,
    but can be redirected somewhere else. To do that, use `stdout` kwarg (it can be
    unix file descriptor or python file object). Pipe argument is a duplex, immediatelly
    after the command is executed, it's pid is send using duplex to the parent process
    (process that called this function).

    Args:
        pipe        duplex
        cmd         command to be executed
    Kwargs:
        stdout      where to redirect stdout from the command
    '''
    try:
        logger.info('CHILD: starting simulation with cmd: %s', cmd)
        sim = subprocess.Popen(cmd, stdout=stdout, stderr=subprocess.STDOUT)
        # send sim id to parent
        logger.info('CHILD: sim.pid: %s', sim.pid)
        pipe.send(sim.pid)
        sim.wait()
    except Exception as e:
        logger.exception('CHILD: Exception: %s', e)
        raise


def show_callstack(logger=None):
    exc_type, exc_value, exc_traceback = sys.exc_info()
    lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
    for line in lines:
        for it in line.split('\n'):
            if it:
                msg = 'CALL STACK: {}'.format(it)
                msg = msg.replace('%', '%%')
                if logger is not None:
                    logger.error(msg)
                else:
                    sys.stderr.write('ERROR: {}\n'.format(msg))


class Cloud(object):

    def __init__(self, cfg_path):
        logger.debug('initializing Cloud object')
        logger.debug('cfg_path: %s', cfg_path)
        self.cfg = Cloud.get_config(cfg_path)
        logger.debug('self.cfg: %s', self.cfg)
        self.rdirwatcher = RDirWatcher(self.cfg)

    def check(self):
        logger.info('going to check')
        comps = self.rdirwatcher.check()
        logger.debug('checked, comps: %s', comps)
        return comps

    @staticmethod
    def get_config(cfg_path):

        parser = SafeConfigParser()
        parser.read(cfg_path)

        opt_pkey_file = '{}/.ssh/id_rsa'.format(os.environ['HOME'])
        if parser.has_option('ssh', 'pkey_file'):
            opt_pkey_file = parser.get('ssh', 'pkey_file')

        # return set if the hostnames are missing; you can iterate
        # through but no checks happen
        opt_hostnames = set()
        if parser.has_option('ssh', 'hostnames'):
            opt_hostname = parser.get('ssh', 'hostnames', set())
            opt_hostnames = opt_hostname.split(',')
            opt_hostnames = set([hostname.strip() for hostname in opt_hostnames])
            if len(list(opt_hostnames)) == 1 and list(opt_hostnames)[0] == '':
                opt_hostnames = set()

        opt_username = os.environ['USER']
        if parser.has_option('ssh', 'username'):
            opt_username = parser.get('ssh', 'username')

        opt_watch_dir = None
        if parser.has_option('watch', 'watch_dir'):
            opt_watch_dir = parser.get('watch', 'watch_dir')
        if opt_watch_dir is None:
            opt_watch_dir = '/tmp'

        opt_watch_pattern = parser.get('watch', 'watch_pattern')
        opt_watch_max_age = float(parser.get('watch', 'watch_max_age'))
        opt_watch_every = float(parser.get('watch', 'watch_every'))
        opt_reestablish_connections = int(parser.get('watch', 'reestablish_connections'))

        opt_cmd = parser.get('simulation', 'cmd')
        opt_cmd = [it.strip() for it in opt_cmd.split(',')]

        opt_sim_start = int(parser.get('simulation', 'sim_start'))
        opt_sim_end = int(parser.get('simulation', 'sim_end'))

        return {
            'pkey_file': opt_pkey_file,
            'hostnames': opt_hostnames,
            'username': opt_username,
            'watch_dir': opt_watch_dir,
            'watch_pattern': opt_watch_pattern,
            'watch_max_age': opt_watch_max_age,
            'watch_every': opt_watch_every,
            'reestablish_connections': opt_reestablish_connections,
            'cmd': opt_cmd,
            'sim_start': opt_sim_start,
            'sim_end': opt_sim_end,
        }

    def run_simulation(self):
        for no_run in range(self.cfg['sim_start'], self.cfg['sim_end']):
            logger.info('starting new simulation run, number: %s', no_run)
            cmd = copy.copy(self.cfg['cmd'])
            cmd.append(str(no_run))
            logger.info('running simulation with cmd: %s', cmd)

            if os.path.exists('params.cfg'):
                logger.info('new simulation type detected, going to create appropriate common group')
                sim_params = SimParams('params.cfg')
                sim_params.prepare_sim(h5file='sim.h5', groupno=no_run)

            if os.path.exists('rng'):
                logger.info('rng file found; deleting it')

            if not self.run_command(cmd):
                logger.error('run_command returns False, something went wrong, exit')
                sys.exit(1)

    def run_command(self, command, niceness=30):

        parent_conn, child_conn = Pipe()
        child = Process(target=run_cmd, args=(child_conn, command))
        child.start()
        sim_pid = parent_conn.recv()
        logger.info('PAREND: child.pid: %s', child.pid)
        logger.info('PARENT: sim.pid: %s', sim_pid)

        with open('pids.log', 'a') as f:
            f.write('{},{},{}\n'.format(os.getpid(), child.pid, sim_pid))

        # hostname of this computer - getfqdn returns fully qualified named of host,
        # this is in contrast with gethostname (first return argo.physics.muni.cz, meanwhile
        # second can return only argo), we need full name
        hostname = socket.getfqdn()
        logger.info('PARENT: hostname: %s', hostname)
        simulation = psutil.Process(sim_pid)
        logger.info('PARENT: simulation: %s', simulation)
        simulation.nice(niceness)
        logger.info('PARENT: niceness set to %s: ', niceness)

        is_simulation_suspended = False
        checks_before_last_reestablishment = 0

        while True:

            try:
                is_alive = simulation.is_running()
                logger.info('is simulation alive: {}'.format(is_alive))

                if not is_alive:
                    logger.info('simulation is dead')
                    return True

                logger.info('PARENT: going to check computers')
                try:
                    comps = self.check()
                except (paramiko.SSHException, socket.error) as e:
                    logger.warning('exception caught while checking comps: %s', e)
                    time.sleep(self.cfg['watch_every'])
                    continue

                logger.info('checked: %s', comps)

                hostname_in_comps = False
                for comp in comps:
                    if comp in hostname:
                        logger.info('comp: {} is contained in hostname: {}'.format(comp, hostname))
                        hostname_in_comps = True

                if hostname_in_comps and not is_simulation_suspended:
                    logger.info('suspending simulation')
                    try:
                        # we have to send SIGTSTP (not SIGSTOP) to mpirun!
                        # mpirun send SIGSTOP to all jobs in reaction to SIGTSTP
                        simulation.send_signal(signal.SIGTSTP)
                        is_simulation_suspended = True
                    except (NoSuchProcess, AccessDenied) as e:
                        # this might happen in case that simulation ends between
                        # is_running check (few lines above) and suspend
                        logger.exception('PARENT: Exception in suspend block, e: %s', e)
                        return True

                if not hostname_in_comps and is_simulation_suspended:
                    logger.info('resuming simulation')
                    try:
                        simulation.resume()
                    except (NoSuchProcess, AccessDenied) as e:
                        # this shouldn't happen!
                        logger.exception('PARENT: Exception in resume block, e: %s', e)
                        return False

                    is_simulation_suspended = False

                checks_before_last_reestablishment += 1
                if checks_before_last_reestablishment >= self.cfg['reestablish_connections']:
                    logger.info('going to reestablish connections, %s >= %s', checks_before_last_reestablishment,
                              self.cfg['reestablish_connections'])
                    self.rdirwatcher.reestablish_connections()
                    checks_before_last_reestablishment = 0

                time.sleep(self.cfg['watch_every'])
            except Exception as e:
                logger.error('PARENT general exception caught while checking computers, e: %s', str(e))
                show_callstack(logger=logger)
                logger.error('going to do the clean_up')
                clean_up(simulation.pid, sim_pid)

