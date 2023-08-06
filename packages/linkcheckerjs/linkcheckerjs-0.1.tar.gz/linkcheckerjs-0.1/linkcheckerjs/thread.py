#!/usr/bin/env python

import sys
import threading
from time import sleep
import signal
import logging


log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(thread)d - %(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)
log.addHandler(handler)


class ThreadPool(object):
    """Flexible thread pool class. Creates a pool of threads, then
    accepts tasks that will be dispatched to the next available
    thread."""

    def __init__(self, number_threads):
        """Initialize the thread pool with number_threads workers."""
        self.threads = []
        self.__taskLock = threading.Condition(threading.Lock())
        self._tasks = []
        self.__active = True
        self.nb_tasks = 0
        self.nb_done = 0
        self.start_threads(number_threads)
        signal.signal(signal.SIGINT, self.signal_handler)

    def start_threads(self, number):
        """Start given number of thread
        """
        for i in range(number):
            thread = ThreadPoolThread(self)
            self.threads.append(thread)
            thread.start()

    def stop_threads(self):
        for thread in self.threads:
            thread.stop()

    def signal_handler(self, signal, frame):
        self.__active = False
        log.info('Finishing started tasks, stopping soon!')

    def add_task(self, task, *args, **kw):
        """Insert a task into the queue.  task must be callable;
        args and taskCallback can be None."""
        if not callable(task):
            return False

        self.__taskLock.acquire()
        try:
            self._tasks.append((task, args, kw))
            self.nb_tasks += 1
            log.debug('Task added %s %s %s' % (
                task, args, kw))
            return True
        finally:
            self.__taskLock.release()

    def get_next_task(self):
        """Retrieve the next task from the task queue. For use
        only by ThreadPoolThread objects contained in the pool."""
        self.__taskLock.acquire()
        try:
            if not self._tasks:
                return (None, None, None)
            else:
                return self._tasks.pop(0)
        finally:
            self.__taskLock.release()

    def print_status(self):
        nb_working = len([not t.working for t in self.threads])
        s = '\rWorking thread %02i   %04i / %04i tasks' % (
            nb_working,
            self.nb_done,
            self.nb_tasks,
        )
        sys.stdout.flush()
        print s,

    def join_all(self):
        """Clear the task queue and terminate all pooled threads,
        optionally allowing the tasks and threads to finish."""
        # Wait for tasks to finish
        while not self.can_stop():
            sleep(1)
            self.print_status()

        log.debug('Waiting the current tasks are finished '
                  'then stop the threads')
        self.stop_threads()
        # Wait until all threads have exited
        for t in self.threads:
            t.join()
            del t

    def can_stop(self):
        if not self.__active:
            # Keyboard interrupt
            return True

        if self._tasks:
            return False

        return all([not t.working for t in self.threads])


class ThreadPoolThread(threading.Thread):
    """Pooled thread class."""

    SLEEPING_TIME = 0.1

    def __init__(self, pool):
        """ Initialize the thread and remember the pool."""
        super(ThreadPoolThread, self).__init__()
        self.pool = pool
        self.__active = True
        self.working = False
        log.debug('Starting thread')

    def run(self):
        """Until told to quit, retrieve the next task and execute
        it, calling the callback if any."""
        while self.__active is True:
            cmd, args, kw = self.pool.get_next_task()
            # If there's nothing to do, just sleep a bit
            if cmd is None:
                self.working = False
                sleep(self.SLEEPING_TIME)
            else:
                self.working = True
                try:
                    task_str = 'task %s %s %s' % (cmd, args, kw)
                    log.debug('Starting %s' % task_str)
                    cmd(*args, **kw)
                    log.debug('Finished %s' % task_str)
                except Exception, e:
                    log.exception(e)
                    raise
                finally:
                    self.pool.nb_done += 1

        self.working = False

    def stop(self):
        """Exit the run loop next time through."""
        log.debug('Stopping thread')
        self.__active = False
