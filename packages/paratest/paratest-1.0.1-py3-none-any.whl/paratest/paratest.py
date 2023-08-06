import os
import sys
import shutil
import tempfile
import argparse
import queue
import threading
import logging
import time
from yapsy.PluginManager import PluginManager
from subprocess import Popen, PIPE
import sqlite3


logger = logging.getLogger('paratest')
shared_queue = queue.PriorityQueue()
INFINITE = sys.maxsize
FINISH = object()
THIS_DIR = os.path.dirname(os.path.realpath(__file__))


class Abort(Exception):
    pass


def configure_logging(verbosity):
    VERBOSITIES = [logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG]
    level = VERBOSITIES[min(int(verbosity), len(VERBOSITIES) -1)]
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(level)


def main():
    parser = argparse.ArgumentParser(description='Run tests in parallel')
    parser.add_argument('action',
                        choices=('plugins', 'run', 'show'),
                        help='Action to perform')
    parser.add_argument(
        '--source',
        default='.',
        help='Path to tests',
    )
    parser.add_argument(
        '--project-name',
        dest='project_name',
        default=None,
        help='The project name. Allow to share results between different sources. The source by default.')
    parser.add_argument(
        '--path-workspaces',
        dest='workspace_path',
        default=None,
        help='Path where create workers workspaces',
    )
    parser.add_argument(
        '--path-output',
        dest='output_path',
        default='output',
        help='Path where store the output file from tests execution',
    )
    parser.add_argument(
        '--path-plugins',
        dest='plugins',
        default='plugins',
        help='Path to search for plugins',
    )
    parser.add_argument(
        '--path-db',
        dest='path_db',
        default=os.path.join(os.path.expanduser("~"), 'paratest.db'),
        help="Path to paratest database.",
    )
    parser.add_argument(
        '--test-pattern',
        dest='test_pattern',
        default='',
        help='Pattern to find test files on workspace',
    )
    parser.add_argument(
        '--plugin',
        help='Plugin to be activated',
    )
    parser.add_argument(
        '-w', '--workers',
        type=int,
        default=5,
        help="Number of workers to be created (tests in parallel)",
    )
    parser.add_argument(
        '-v', '--verbosity',
        action='count',
        default=0,
        help='Increase the verbosity level'
    )
    parser.add_argument(
        '--setup',
        help='Script to prepare everything; it will be run once at the beginning'
    )
    parser.add_argument(
        '--setup-workspace',
        dest='setup_workspace',
        help='Script to prepare the workspace; it will be run once by worker',
    )
    parser.add_argument(
        '--setup-test',
        dest='setup_test',
        help='Script to prepare a test; it will be run before each test'
    )
    parser.add_argument(
        '--teardown-test',
        dest='teardown_test',
        help='Script to finalize a test; it will be run after each test'
    )
    parser.add_argument(
        '--teardown-workspace',
        dest='teardown_workspace',
        help='Script to finalize a workspace; it will be run once by worker when no more tests are available'
    )
    parser.add_argument(
        '--teardown',
        help='Script to finalize; it will be run once at the end'
    )

    args = parser.parse_args()
    configure_logging(args.verbosity)
    scripts = Scripts(
        setup=args.setup,
        setup_workspace=args.setup_workspace,
        setup_test=args.setup_test,
        teardown_test=args.teardown_test,
        teardown_workspace=args.teardown_workspace,
        teardown=args.teardown,
    )

    workspace_path = (
        tempfile.mkdtemp()
        if args.workspace_path is None
        else None
    )
    try:
        persistence = Persistence(args.path_db, args.project_name or args.source)
        paratest = Paratest(args.workers, scripts, args.source, workspace_path, args.output_path, args.test_pattern, persistence)
        if args.action == 'plugins':
            return paratest.list_plugins()
        if args.action == 'run':
            persistence.initialize()
            return paratest.run(args.plugin)
        if args.action == 'show':
            return persistence.show()
    except Abort as e:
        logger.critical(e)
        sys.exit(2)
    finally:
        if args.workspace_path is None:
            shutil.rmtree(workspace_path)


def run_script(script, **kwargs):
    if not script:
        return
    for k, v in kwargs.items():
        script = script.replace('{%s}' % k, v)

    logger.info("About to run script $%s", script)

    result = Popen(script, shell=True, stdout=PIPE, stderr=PIPE)
    output, err = result.communicate()

    output = output.decode("utf-8")
    err = err.decode("utf-8")

    if output != '':
        logger.info(output)
    if err != '':
        logger.warning(err)
    return result.returncode

class Scripts(object):
    def __init__(self, setup, setup_workspace, setup_test, teardown_test, teardown_workspace, teardown):
        self.setup = setup
        self.setup_workspace = setup_workspace
        self.setup_test = setup_test
        self.teardown_test = teardown_test
        self.teardown_workspace = teardown_workspace
        self.teardown = teardown


class Paratest(object):
    def __init__(self, workspace_num, scripts, source_path, workspace_path, output_path, test_pattern, persistence):
        self.workspace_num = workspace_num
        self.workspace_path = workspace_path
        self.scripts = scripts
        self.source_path = source_path
        self.output_path = output_path
        self.test_pattern = test_pattern
        self._workers = []
        plugin_places = [
            os.path.join(THIS_DIR, "plugins"),
        ]
        logger.debug("Loading plugins from: %s", plugin_places)
        self.pluginmgr = PluginManager()
        self.pluginmgr.setPluginInfoExtension('paratest')
        self.pluginmgr.setPluginPlaces(plugin_places)
        self.pluginmgr.collectPlugins()
        self.persistence = persistence

        if not os.path.exists(self.source_path):
            os.makedirs(self.source_path)
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)

    def list_plugins(self):
        msg = "Available plugins are:\n"
        for plugin in self.pluginmgr.getAllPlugins():
            msg += "  %s" % plugin.name
        print(msg)


    def run(self, plugin):
        try:
            plugin = self.pluginmgr.getPluginByName(plugin)
            pluginobj = plugin.plugin_object

            self.run_script_setup()
            test_number = self.queue_tests(pluginobj)
            self.create_workers(pluginobj, self.num_of_workers(test_number))
            self.start_workers()
            self.wait_workers()
            self.run_script_teardown()
            self.assert_all_messages_were_processed()
            self.assert_all_workers_were_successful()
            logger.info("Finished successfully")
        finally:
            self.print_report()

    def run_script_setup(self):
        if run_script(self.scripts.setup, path=self.workspace_path):
            raise Abort('The setup script failed. aborting.')

    def run_script_teardown(self):
        if run_script(self.scripts.teardown, path=self.workspace_path):
            raise Abort('The teardown script failed, but nothing can be done.')

    def queue_tests(self, pluginobj):
        tids = 0
        for test_name, test_cmd in pluginobj.find(self.source_path, test_pattern=None, file_pattern=self.test_pattern, output_path=self.output_path):
            tid = (test_name, test_cmd)
            shared_queue.put((self.persistence.get_priority(test_name), tid))
            tids += 1
        return tids

    def create_workers(self, pluginobj, workers):
        for i in range(workers):
            t = Worker(
                pluginobj,
                scripts=self.scripts,
                workspace_path=self.workspace_path,
                source_path=self.source_path,
                output_path=self.output_path,
                persistence=self.persistence,
                name=str(i),
            )
            self._workers.append(t)

    def num_of_workers(self, test_number):
        return min(self.workspace_num, test_number)

    def start_workers(self):
        logger.debug("start workers")
        for t in self._workers:
            t.start()
            shared_queue.put((INFINITE, FINISH))

    def print_report(self):
        msg = 'Global Report:\n'
        durations = {}
        for t in self._workers:
            msg += 'Worker %s\n' % t.name
            durations[t] = 0
            for result in t.report:
                msg += '   %.4fs %s ... %s\n' %(
                    result.duration,
                    result.name,
                    'OK' if result.success else 'FAIL',
                )
                durations[t] += result.duration
        bucklet = max(durations.values())
        total = bucklet * len(durations)
        msg += "\nIdle time: %.4fs\n" % (total - sum(durations.values()))
        logger.info(msg)

    def wait_workers(self):
        logger.debug("wait for all workers to finish")
        for t in self._workers:
            t.join()

    def assert_all_workers_were_successful(self):
        if any(x.errors for x in self._workers):
            raise Abort('One or more workers failed')

    def assert_all_messages_were_processed(self):
        if not shared_queue.empty():
            raise Abort('There were unprocessed tests, but all workers are dead. Aborting.')


class Report(object):
    def __init__(self, name, duration, success):
        self.name = name
        self.duration = duration
        self.success = success


class Worker(threading.Thread):
    def __init__(self, plugin, scripts, workspace_path, source_path, output_path, persistence, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.plugin = plugin
        self.scripts = scripts
        self.source_path = source_path
        self.output_path = output_path
        self.persistence = persistence
        self.workspace_path = os.path.join(workspace_path, self.name)
        if not os.path.exists(self.workspace_path):
            os.makedirs(self.workspace_path)
        self.errors = None
        self.report = []

    def run(self):
        print("%s START" % self.name)
        logger.debug("%s START" % self.name)
        tid = object()
        self.run_script_setup_workspace()
        self.errors = False
        while tid is not FINISH:
            self.run_script_setup_test()

            _, tid = shared_queue.get()
            try:
                if tid is not FINISH:
                    self.process(tid)
            except:
                self.errors = True
            shared_queue.task_done()

            self.run_script_teardown_test()
        self.run_script_teardown_workspace()
        logger.info("Worker %s has finished.", self.name)
        print("Worker %s has finished.", self.name)

    def run_script_setup_workspace(self):
        self._run_script(
            self.scripts.setup_workspace,
            'Setup workspace failed on worker %s and could not initialize the environment. Worker is dead' % self.name
        )

    def run_script_teardown_workspace(self):
        self._run_script(
            self.scripts.teardown_workspace,
            'Teardown workspace failed on worker %s. Worker is dead' % self.name
        )

    def run_script_setup_test(self):
        self._run_script(
            self.scripts.setup_test,
            "setup_test failed on worker %s. Worker is dead" % self.name
        )

    def run_script_teardown_test(self):
        self._run_script(
            self.scripts.teardown_test,
            "teardown_test failed on worker %s. Worker is dead" % self.name
        )

    def _run_script(self, script, message):
        if run_script(script, id=self.name, workspace=self.workspace_path, source=self.source_path, output=self.output_path):
            raise Abort(message)

    def process(self, tid):
        test_name, test_cmd = tid
        logger.info("Runner {runner} running test {test} on {workspace}. {left} tests left"
                    .format(runner=self.name, test=test_name, workspace=self.workspace_path, left=shared_queue.qsize()))
        try:
            start = time.time()
            result = Popen(test_cmd, shell=True, stdout=PIPE, stderr=PIPE, cwd=self.workspace_path)
            stdout, stderr = result.communicate()
            duration = time.time() - start
            if stdout: logger.info(stdout.decode("utf-8"))
            if stderr: logger.warning(stderr.decode("utf-8"))
            if result.returncode != 0:
                raise Exception("Test %s failed with code %s", test_name, result.errorcode)

            self.persistence.add(test_name, duration)
            report = Report(name=test_name, duration=duration, success=True)
        except Exception as e:
            duration = time.time() - start
            logger.error("Suite %s failed due to: %s", tid, e)
            report = Report(name=test_name, duration=duration, success=False)
            raise
        finally:
            self.report.append(report)


class Persistence(object):
    def __init__(self, db_path, projectname):
        self.create = not os.path.exists(db_path)
        self.projectname = projectname
        self.db_path = db_path
        self.execution = None

    def initialize(self):
        con = sqlite3.connect(self.db_path)
        if self.create:
            with con:
                logger.info("Creating persistence file")
                con.execute("create table executions(id integer primary key, source varchar, timestamp date default (datetime('now','localtime')))")
                con.execute("create table testtime(id integer primary key, source varchar, test varchar, duration float, execution int, FOREIGN KEY(execution) REFERENCES executions(id) on delete cascade)")
            self.create = False
        with con:
            c = con.execute("select id from executions where source=? order by id desc limit 5, 1", (self.projectname, ))
            f = c.fetchone()
            deprecated_executions = f[0] if f else None
            if deprecated_executions is not None:
                con.execute("delete from executions where id <= ? and source=?", (deprecated_executions, self.projectname))
                con.execute("delete from testtime where execution <= ? and source=?", (deprecated_executions, self.projectname))
            con.execute("insert into executions(source) values (?)", (self.projectname, ))
            c = con.execute("select max(id) from executions where source=?", (self.projectname, ))
            self.execution = c.fetchone()[0]
        con.close()

    def get_priority(self, test):
        con = sqlite3.connect(self.db_path)
        try:
            cursor = con.execute('select avg(duration) from testtime where source=? and test=?', (self.projectname, test) )
            return -1 * int(cursor.fetchone()[0] or 0)
        finally:
            con.close()

    def add(self, test, duration):
        con = sqlite3.connect(self.db_path)
        with con:
            con.execute('insert into testtime(source, test, duration, execution) values(?, ?, ?, ?) ', (self.projectname, test, duration, self.execution) )
        con.close()

    def show(self):
        if not os.path.exists(self.db_path):
            print("No database found")
            return
        con = sqlite3.connect(self.db_path)
        for item in con.execute('select distinct source from testtime'):
            projectname = item[0]
            for test in con.execute('select test, avg(duration) from testtime where source=? group by test order by avg(duration) desc', (projectname,)):
                print('    %.2f: %s' % (test[1], test[0]))

        con.close()


if __name__ == '__main__':
    main()
