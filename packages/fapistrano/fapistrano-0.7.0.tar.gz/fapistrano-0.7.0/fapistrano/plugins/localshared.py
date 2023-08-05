# -*- coding: utf-8 -*-


from fabric.api import env, run
from .. import signal, configuration, directory

def init():
    configuration.setdefault('localshared_source', '')
    signal.register('deploy.starting', copy_localshared_linked_files)

def copy_localshared_linked_files():
    _check_shared_file_dirs()
    _check_shared_dir_parents()
    _copy_linked_files()
    _copy_linked_dirs()

def _check_shared_file_dirs():
    for linked_file_dir in directory.get_linked_file_dirs():
        env.linked_file_dir = linked_file_dir
        run('mkdir -p %(shared_path)s/%(linked_file_dir)s' % env)
        del env['linked_file_dir']

def _check_shared_dir_parents():
    for linked_dir_parent in directory.get_linked_dir_parents():
        env.linked_dir_parent = linked_dir_parent
        run('mkdir -p %(shared_path)s/%(linked_file_dir)s' % env)
        del env['linked_dir_parent']

def _copy_linked_files():
    for linked_file in directory.get_linked_files():
        env.linked_file = linked_file
        run('cp %(localshared_source)s/%(linked_file)s %(shared_path)s/%(linked_file)s' % env)
        del env['linked_file']

def _copy_linked_dirs():
    for linked_dir in directory.get_linked_dirs():
        env.linked_dir = linked_dir
        run('rm -r %(shared_path)s/%(linked_file)s' % env)
        run('cp -R %(localshared_source)s/%(linked_file)s %(shared_path)s' % env)
