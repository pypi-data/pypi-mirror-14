from collections import namedtuple
import threading
import queue
import logging
import time
import socket
import os
import textwrap
import signal

from sauna import plugins, consumers

__version__ = '0.0.3'

ServiceCheck = namedtuple('ServiceCheck',
                          ['timestamp', 'hostname', 'name',
                           'status', 'output'])


class DependencyError(Exception):

    def __init__(self, plugin, dep_name, pypi='', deb=''):
        self.msg = '{} depends on {}. It can be installed with:\n'.format(
            plugin, dep_name
        )
        if pypi:
            self.msg = '{}    pip install {}\n'.format(self.msg, pypi)
        if deb:
            self.msg = '{}    apt-get install {}\n'.format(self.msg, deb)

    def __str__(self):
        return self.msg


def read_config(config_file):
    # importing yaml here because dependency is not installed
    # when fetching __version__ from setup.py
    import yaml

    try:
        with open(config_file) as f:
            return yaml.safe_load(f)
    except OSError as e:
        print('Cannot read configuration file {}: {}'.format(config_file, e))
        exit(1)


def assemble_config_sample(path):
    sample = '---\nperiodicity: 120\nhostname: node-1.domain.tld\n'

    sample += '\nconsumers:\n'
    consumers_sample = ''
    for c in consumers.get_all_consumers():
        consumers_sample += textwrap.dedent(c.config_sample())
    sample += consumers_sample.replace('\n', '\n  ')

    sample += '\nplugins:\n'
    plugins_sample = ''
    for p in plugins.get_all_plugins():
        plugins_sample += textwrap.dedent(p.config_sample())
    sample += plugins_sample.replace('\n', '\n  ')

    file_path = os.path.join(path, 'sauna-sample.yml')
    with open(file_path, 'w') as f:
        f.write(sample)

    return file_path


def get_checks_name(config_file):
    config = read_config(config_file)
    plugins_config = config['plugins']
    checks = get_all_checks(plugins_config)
    return [check.name for check in checks]


def get_all_checks(plugins_config):
    checks = []
    deps_error = []
    for plugin_name, plugin_data in plugins_config.items():

        # Load plugin
        try:
            Plugin = plugins.get_plugin(plugin_name)
        except ValueError as e:
            print(str(e))
            exit(1)

        # Configure plugin
        try:
            plugin = Plugin(plugin_data.get('config', {}))
        except DependencyError as e:
            deps_error.append(str(e))
            continue

        # Launch plugin checks
        for check in plugin_data['checks']:
            check_func = getattr(plugin, check['type'])

            if not check_func:
                print('Unknown check {} on plugin {}'.format(check['type'],
                                                             plugin_name))
                exit(1)

            check_name = (check.get('name') or '{}_{}'.format(
                plugin_name, check['type']
            ).lower())

            checks.append(plugins.Check(check_name, check_func, check))
    if deps_error:
        for error in deps_error:
            print(error)
        exit(1)
    return checks


def launch_all_checks(plugins_config, hostname):
    for check in get_all_checks(plugins_config):

            try:
                status, output = check.run_check()
            except Exception as e:
                logging.warning('Could not run check {}: {}'.format(
                    check.name, str(e)
                ))
                status = 3
                output = str(e)
            s = ServiceCheck(
                timestamp=int(time.time()),
                hostname=hostname,
                name=check.name,
                status=status,
                output=output
            )
            yield s


q = queue.Queue()
must_stop = threading.Event()
try:
    # In Python 3.2 threading.Event is a factory function
    # the real class lives in threading._Event
    event_type = threading._Event
except AttributeError:
    event_type = threading.Event


def run_producer(plugins_config, periodicity, hostname):
    while True:
        for service_check in launch_all_checks(plugins_config, hostname):
            q.put(service_check)
        if must_stop.wait(timeout=periodicity):
            break
    logging.debug('Exited producer thread')


def run_consumer(consumers_config):
    consumer_name, consumer_config = consumers_config.popitem()
    try:
        consumer = consumers.get_consumer(consumer_name)(consumer_config)
    except DependencyError as e:
        print(str(e))
        exit(1)

    while not must_stop.is_set():
        service_check = q.get()
        if isinstance(service_check, event_type):
            continue
        consumer.try_send(service_check, must_stop)
    logging.debug('Exited consumer thread')


def term_handler(*args):
    """Notify producer and consumer that they should stop."""
    if not must_stop.is_set():
        must_stop.set()
        q.put(must_stop)
        logging.info('Exiting...')


def launch(config_file):

    # Fetch configuration settings
    config = read_config(config_file)
    plugins_config = config['plugins']
    consumers_config = config['consumers']
    periodicity = config.get('periodicity', 120)
    hostname = config.get('hostname', socket.getfqdn())

    # Start producer and consumer threads
    producer = threading.Thread(
        name='producer', target=run_producer,
        args=(plugins_config, periodicity, hostname)
    )
    consumer = threading.Thread(
        name='consumer', target=run_consumer,
        args=(consumers_config,)
    )
    consumer.start()
    producer.start()

    signal.signal(signal.SIGTERM, term_handler)
    signal.signal(signal.SIGINT, term_handler)

    producer.join()
    term_handler()
    consumer.join()

    logging.debug('Exited main thread')
