Config
======

Config as Fabfile `env`
-----------------------

Since fapistrano is a thin wrapper of fabric, you can easily config fapistrano via fabric environment. Like most other fabric's behaviour, fapistrano's behaviour can be also controlled by modifying `env` variables.


Config as YAML
--------------

Write a YAML file named `deploy.yml` in your project root path, fapistrano cli will recognize it and read items as configuration.


Configuration Items
-------------------

* project_name
* app_name
* user
* keep_releases
* path
* env_role_configs
