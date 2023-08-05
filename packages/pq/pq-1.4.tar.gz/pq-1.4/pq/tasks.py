# -*- coding: utf-8 -*-
from logging import getLogger
from functools import wraps
from . import (
    PQ as BasePQ,
    Queue as BaseQueue,
)


def task(queue, *job_args, **job_kwargs):
    def decorator(f):
        f._path = "%s.%s" % (f.__module__, f.__name__)
        f._max_retries = job_kwargs.pop('max_retries', 0)
        f._retry_in = job_kwargs.pop('retry_in', '30s')

        queue.handler_registry[f._path] = f

        @wraps(f)
        def wrapper(*args, **kwargs):
            queue.put(
                dict(
                    function=f._path,
                    args=args,
                    kwargs=kwargs,
                    retried=0,
                ),
                *job_args,
                **job_kwargs
            )

        return wrapper

    return decorator


class Queue(BaseQueue):
    handler_registry = dict()
    logger = getLogger('pq.tasks')

    def perform(self, job):
        data = job.data
        f = self.handler_registry[data['function']]

        try:
            f(*data['args'], **data['kwargs'])
            return True

        except Exception as e:
            retried = data['retried']

            if f._max_retries > retried:
                data.update(dict(
                    retried=retried + 1,
                ))
                id = self.put(data, schedule_at=f._retry_in)
                self.logger.info("Rescheduled %r as `%s`" % (job, id))

            else:
                self.logger.warning("Failed to perform job %r :" % job)
                self.logger.exception(e)

            return False

    task = task

    def work(self, burst=False):
        """Starts processing jobs."""
        self.logger.info('`%s` starting to perform jobs' % self.name)

        for job in self:
            if job is None:
                if burst:
                    return

                continue

            self.perform(job)


class PQ(BasePQ):
    queue_class = Queue
