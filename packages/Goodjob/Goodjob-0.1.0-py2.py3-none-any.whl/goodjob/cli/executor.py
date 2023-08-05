#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import sys
import signal
import traceback

import click

from goodjob.jobs.models import Job, JobStatus, JobEvent
from goodjob.operators import manager
from goodjob.constants import NOW


class RealJobExecutor(object):
    def __init__(self, job):
        self.job = job
        self.provider = manager.get_operator(job.provider)
        self.notifier = manager.get_operator(job.notifier)

        # Register the handler of signal SIGTERM
        signal.signal(signal.SIGTERM, self.sigterm_received)

    def sigterm_received(self, signum, stack):
        # Cancel the provider process
        self.provider.cancel()

        self.notifier.run(self.job.name, JobEvent.cancelled)
        self.job.status = JobStatus.cancelled
        self.job.date_stopped = NOW()
        self.job.save()

        # Exit explicitly (raise `SystemExit`)
        sys.exit(1)

    def execute(self):
        self.notifier.run(self.job.name, JobEvent.started)
        self.job.status = JobStatus.in_progress
        self.job.date_started = NOW()
        self.job.save()

        try:
            self.provider.run()
        # Do not use `except:` here,
        # since we do not want to catch `SystemExit`
        except Exception:
            exc_info = traceback.format_exc()
            sys.stderr.write(exc_info)
            self.notifier.run(self.job.name, JobEvent.failed)
            self.job.status = JobStatus.failed
        else:
            self.notifier.run(self.job.name, JobEvent.finished)
            self.job.status = JobStatus.finished
        self.job.date_stopped = NOW()
        self.job.save()


@click.command()
@click.argument('job_id')
def main(job_id):
    job = Job.objects(id=job_id).first()
    executor = RealJobExecutor(job)
    executor.execute()


if __name__ == '__main__':
    main()
