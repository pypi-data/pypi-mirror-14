import time

from threading import Thread
from threading import Event
from Queue import Queue
from threading import RLock


class Job(Thread):
    def __init__(self, target=None):
        super(Job, self).__init__()
        self.name=self.__class__.__name__
        #self.daemon=True
        self._jobmanager=None
        self._target=target
        self._eventStart=Event()
        self._eventStop=Event()
        self._eventWakeup=Event()
        self._onInit()

    def registerWithJobManager(self, jobmanager):
        self._jobmanager=jobmanager

    def rename(self, name):
        self.name=name

    @property
    def jobmanager(self):
        return self._jobmanager
    
    @property
    def logger(self):
        if self._jobmanager:
            return self.jobmanager.logger

    def wakeup(self):
        self._eventWakeup.set()

    def sleep(self, delay):
        self._eventWakeup.clear()
        return self._eventWakeup.wait(delay)

    def start(self):
        if self._jobmanager:
            self.wakeup()
            super(Job, self).start()
            self._onStart()

    def run(self):
        if self._jobmanager:
            self.logger.debug('thread(%s)->run()' % self.name)
            self._eventStart.set()
            while not self.isStopRequest():
                self._onRun()
            self.logger.debug('thread(%s) manager exited' % self.name)

    def stop(self):
        if self._jobmanager and not self.isStopRequest():
            self._eventStop.set()
            self.wakeup()
            self._onStop()
            self.join()
            self.logger.debug('thread(%s) stopped' % self.name)

    def release(self):
        self._onRelease()

    def waitUntilStarted(self):
        self._eventStart.wait()

    def isStopRequest(self):
        return self._eventStop.isSet()

    def _onInit(self):
        return self.onInit()
        try:
            return self.onInit()
        except:
            pass

    def onInit(self):
        pass

    def _onRelease(self):
        self.logger.debug('thread(%s)->onRelease()' % self.name)
        try:
            return self.onRelease()
        except:
            self.logger.exception('thread(%s)->onRelease()' % self.name)

    def onRelease(self):
        pass

    def _onStart(self):
        self.logger.debug('thread(%s)->onStart()' % self.name)
        try:
            return self.onStart()
        except:
            self.logger.exception('thread(%s)->onStart()' % self.name)

    def onStart(self):
        pass

    def _onRun(self):
        try:
            if not self.onRun():
                self.sleep(0.1)
        except:
            self.logger.exception('thread(%s)->onRun()' % self.name)
            self.sleep(1.0)

    # override if needed
    def onRun(self):
        if self._target and callable(self._target):
            return self._target()
        else:
            self.sleep(2.0)

    def _onStop(self):
        self.logger.debug('thread(%s)->onStop()' % self.name)
        try:
            return self.onStop()
        except:
            self.logger.exception('thread(%s)->onStop()' % self.name)

    def onStop(self):
        pass


class JobManager(object):
    def __init__(self, logger):
        self._logger=logger
        self._lock=RLock()
        self._jobs=[]

    @property
    def logger(self):
        return self._logger

    def jobs(self):
        return self._jobs

    def job(self, name):
        try:
            for job in self.jobs():
                if job.name==name:
                    return job
        except:
            pass

    def __getitem__(self, key):
        return self.job(key)

    def addJob(self, job, name=None):
        with self._lock:
            if name:
                job.rename(name)
            job.registerWithJobManager(self)
            self._jobs.append(job)
            self.logger.info('JOBS: job %s added.' % job.name)
            return job

    def addJobFromFunction(self, target, name=None):
        job=Job(target)
        return self.addJob(job, name)

    def start(self):
        with self._lock:
            self.logger.info('JOBS: sequentially starting jobs...')
            for job in self.jobs():
                job.start()
                job.waitUntilStarted()
            self.logger.info('JOBS: jobs started.')

    def stop(self):
        with self._lock:
            self.logger.info('JOBS: sequentially stopping jobs...')
            for job in reversed(self.jobs()):
                job.stop()
            self.logger.info('JOBS: jobs halted.')


if __name__ == "__main__":
    pass

