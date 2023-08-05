Directories
===========

Fapistrano provide you a transparent directory hierarchy to place a specific version of you deployments.

The root path of this structure is defined by fabric environ variable: `path`.

For an instance, if you have defined your path as `env.path = '/home/deploy/www/project`, then you may get a directory tree like this::

├── current -> /home/deploy/www/zion-staging/releases/160313-180023
├── releases
│   ├── 160313-173351
│   ├── 160313-173502
│   ├── 160313-173521
│   ├── 160313-173707
│   ├── 160313-180023
├── shared
│   ├── <shared dirs or shared files>

You can store several latest releases in `releases` directory as many as you've defined as `keep_releases`.

Among them, the mose latest release is considered as current release, Fapistrano will make a soft link `current` to it.

`shared` contains shared dirs or shared files linked by each release. They may be environment related configurations, secret files, or persistent storage.
