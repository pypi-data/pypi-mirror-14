from __future__ import absolute_import
from __future__ import unicode_literals

import operator
import sys
from threading import Thread

from docker.errors import APIError
from six.moves import _thread as thread
from six.moves.queue import Empty
from six.moves.queue import Queue

from compose.cli.signals import ShutdownException
from compose.utils import get_output_stream


def parallel_execute(objects, func, get_name, msg, get_deps=None):
    """Runs func on objects in parallel while ensuring that func is
    ran on object only after it is ran on all its dependencies.

    get_deps called on object must return a collection with its dependencies.
    get_name called on object must return its name.
    """
    objects = list(objects)
    stream = get_output_stream(sys.stderr)

    writer = ParallelStreamWriter(stream, msg)
    for obj in objects:
        writer.initialize(get_name(obj))

    q = setup_queue(objects, func, get_deps, get_name)

    done = 0
    errors = {}
    results = []
    error_to_reraise = None

    while done < len(objects):
        try:
            obj, result, exception = q.get(timeout=1)
        except Empty:
            continue
        # See https://github.com/docker/compose/issues/189
        except thread.error:
            raise ShutdownException()

        if exception is None:
            writer.write(get_name(obj), 'done')
            results.append(result)
        elif isinstance(exception, APIError):
            errors[get_name(obj)] = exception.explanation
            writer.write(get_name(obj), 'error')
        else:
            errors[get_name(obj)] = exception
            error_to_reraise = exception
        done += 1

    for obj_name, error in errors.items():
        stream.write("\nERROR: for {}  {}\n".format(obj_name, error))

    if error_to_reraise:
        raise error_to_reraise

    return results


def _no_deps(x):
    return []


def setup_queue(objects, func, get_deps, get_name):
    if get_deps is None:
        get_deps = _no_deps

    results = Queue()
    started = set()   # objects being processed
    finished = set()  # objects which have been processed

    def do_op(obj):
        try:
            result = func(obj)
            results.put((obj, result, None))
        except Exception as e:
            results.put((obj, None, e))

        finished.add(obj)
        feed()

    def ready(obj):
        # Is object ready for performing operation
        return obj not in started and all(
            dep not in objects or dep in finished
            for dep in get_deps(obj)
        )

    def feed():
        for obj in filter(ready, objects):
            started.add(obj)
            t = Thread(target=do_op, args=(obj,))
            t.daemon = True
            t.start()

    feed()
    return results


class ParallelStreamWriter(object):
    """Write out messages for operations happening in parallel.

    Each operation has it's own line, and ANSI code characters are used
    to jump to the correct line, and write over the line.
    """

    def __init__(self, stream, msg):
        self.stream = stream
        self.msg = msg
        self.lines = []

    def initialize(self, obj_index):
        if self.msg is None:
            return
        self.lines.append(obj_index)
        self.stream.write("{} {} ... \r\n".format(self.msg, obj_index))
        self.stream.flush()

    def write(self, obj_index, status):
        if self.msg is None:
            return
        position = self.lines.index(obj_index)
        diff = len(self.lines) - position
        # move up
        self.stream.write("%c[%dA" % (27, diff))
        # erase
        self.stream.write("%c[2K\r" % 27)
        self.stream.write("{} {} ... {}\r".format(self.msg, obj_index, status))
        # move back down
        self.stream.write("%c[%dB" % (27, diff))
        self.stream.flush()


def parallel_operation(containers, operation, options, message):
    parallel_execute(
        containers,
        operator.methodcaller(operation, **options),
        operator.attrgetter('name'),
        message)


def parallel_remove(containers, options):
    stopped_containers = [c for c in containers if not c.is_running]
    parallel_operation(stopped_containers, 'remove', options, 'Removing')


def parallel_start(containers, options):
    parallel_operation(containers, 'start', options, 'Starting')


def parallel_pause(containers, options):
    parallel_operation(containers, 'pause', options, 'Pausing')


def parallel_unpause(containers, options):
    parallel_operation(containers, 'unpause', options, 'Unpausing')


def parallel_kill(containers, options):
    parallel_operation(containers, 'kill', options, 'Killing')


def parallel_restart(containers, options):
    parallel_operation(containers, 'restart', options, 'Restarting')
