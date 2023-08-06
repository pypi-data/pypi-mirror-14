# -*- coding: utf-8 -*-

from fabric.api import task
from fabric.tasks import execute

### API

@task
def release():
    for _task in [
            'starting',
            'started',
            'updating',
            'updated',
            'publishing',
            'published',
            'finishing',
            'finished',
    ]:
        execute(_task)

@task
def rollback():
    for _task in [
            'starting',
            'started',
            'reverting',
            'reverted',
            'publishing',
            'published',
            'finishing_rollback',
            'finished',
    ]:
        execute(_task)

@task
def starting():
    pass

@task
def started():
    pass

@task
def updating():
    pass

@task
def updated():
    pass

@task
def publishing():
    pass

@task
def published():
    pass

@task
def reverting():
    pass

@task
def reverted():
    pass

@task
def finishing():
    pass

@task
def finishing_rollback():
    pass

@task
def finished():
    pass


### Helper tasks
