Signals
=======

Basically, Fapistrano provides 3 type of deploy flow:

1. release flow
2. rollback flow
3. restart flow

Release Flow
------------

When you trigger a release task, it emits at least 8 signals::

deploy.starting
deploy.started
deploy.updating
deploy.updated
deploy.publishing
deploy.published
deploy.finishing
deploy.finished

Example::

[app-stag01] Executing task 'deploy.release'
===> Starting
[app-stag01] run: mkdir -p /home/deploy/www/zion-staging/{releases,shared/log}
[app-stag01] run: chmod -R g+w /home/deploy/www/zion-staging/shared
[app-stag01] run: mkdir -p /home/deploy/www/zion-staging/releases/160314-085322
===> Started
===> Updating
===> Updated
===> Publishing
[app-stag01] run: ln -nfs /home/deploy/www/zion-staging/releases/160314-085322 current
===> Published
===> Finishing
===> Cleanning up old release(s)
[app-stag01] run: ls -x /home/deploy/www/zion-staging/releases
[app-stag01] run: rm -rf 160313-230707
===> Finished
Done.
Disconnecting from 10.0.0.1:2333... done.

Rollback Flow
-------------

When you trigger a rollback task, it emits at least 8 signals::

deploy.starting
deploy.started
deploy.reverting
deploy.reverted
deploy.publishing
deploy.published
deploy.finishing_rollback
deploy.finished

Restart Flow
------------

When you tirgger a restart flow, it emits at least 2 signals::

deploy.restarting
deploy.restarted


You can hook this signals and write you own deploy logic.
