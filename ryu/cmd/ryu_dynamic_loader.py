#!/usr/bin/env python
# -*- codeing: utf-8 -*-
# Copyright (C) 2011 Nippon Telegraph and Telephone Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import cmd
import logging
import pkgutil
import inspect
import pdb
import sys


from ryu import cfg
from ryu.lib import hub
hub.patch(thread=False)

from ryu import log
from ryu import version
log.early_init_log(logging.DEBUG)

from ryu.base.app_manager import RyuApp, AppManager
from ryu import app as ryu_app
from ryu.app import wsgi


LOG = logging.getLogger('ryu.app.dynamic_load')

class DynamicLoadCmd(cmd.Cmd):

    def __init__(self, *args, **kwargs):
        self.ryu_mgr = None
        self.loop_thr = None
        self.services = []
        self.available_app = {}
        self.prompt = 'ryu > '

        for _, name, is_pkg in pkgutil.walk_packages(ryu_app.__path__):
            LOG.debug(
                'Find %s : %s',
                'package' if is_pkg else 'module',
                name)

            if is_pkg:
                continue

            try:
                _base = __import__('ryu.app.' + name)
                _app_module = getattr(_base.app, name)

                for _attr_name in dir(_app_module):
                    _attr = getattr(_app_module, _attr_name)

                    if inspect.isclass(_attr) and _attr.__bases__[0] == RyuApp:
                        LOG.debug('\tFind ryu app : %s.%s', _attr.__module__, _attr.__name__)
                        _full_name = '%s.%s' % (_attr.__module__, _attr.__name__)
                        self.available_app.setdefault(_full_name, _attr)

            except ImportError:
                LOG.debug('Import Error')

            except Exception, ex:
                LOG.debug('Exception %s', str(ex))

        cmd.Cmd.__init__(self, *args, **kwargs)

    def do_install(self, line):
        '''Install an ryu application'''
        LOG.debug('cmd : %s', line)
        args = line.split(' ')
        if len(args) < 1:
            print 'usage: install ryu-app-name'
            return

        try:
            app_cls = __import__(args[0])
            LOG.debug('cls : %s', str(app_cls))
            self.ryu_mgr.instantiate(app_cls)
        except Exception, ex:
            print 'Import error'
            raise ex

    def do_list(self, line):
        '''List all available ryu application'''
        print('Available app:')
        print('---------------')
        _installed_apps = self.ryu_mgr.applications

        for app_name in self.available_app:
            _cls = self.available_app[app_name]
            print '%s' % (app_name, ),

            if _cls in \
                [obj.__class__ for obj in _installed_apps.values()]:
                print '[\033[92minstalled\033[0m]'

            else:
                print ''

    def do_exit(self, line):
        '''Exit from ryu dynamic loader'''
        print('Exiting....')
        return True


CONF = cfg.CONF
CONF.register_cli_opts([
    cfg.ListOpt('app-lists', default=[],
                help='application module name to run'),
    cfg.MultiStrOpt('app', positional=True, default=[],
                    help='application module name to run'),
    cfg.StrOpt('pid-file', default=None, help='pid file name'),
    cfg.BoolOpt('enable-debugger', default=False,
                help='don\'t overwrite Python standard threading library'
                '(use only for debugging)'),
])

def main(args=None, prog=None):
    try:
        CONF(args=args, prog=prog,
             project='ryu', version='ryu-manager %s' % version,
             default_config_files=['/usr/local/etc/ryu/ryu.conf'])
    except cfg.ConfigFilesNotFoundError:
        CONF(args=args, prog=prog,
             project='ryu', version='ryu-manager %s' % version)

    log.init_log()

    if CONF.enable_debugger:
        msg = 'debugging is available (--enable-debugger option is turned on)'
        LOG.info(msg)
    else:
        hub.patch(thread=True)

    if CONF.pid_file:
        import os
        with open(CONF.pid_file, 'w') as pid_file:
            pid_file.write(str(os.getpid()))

    app_lists = CONF.app_lists + CONF.app
    # keep old behaivor, run ofp if no application is specified.
    if not app_lists:
        app_lists = ['ryu.controller.ofp_handler']

    app_mgr = AppManager.get_instance()
    app_mgr.load_apps(app_lists)
    contexts = app_mgr.create_contexts()
    services = []
    services.extend(app_mgr.instantiate_apps(**contexts))

    webapp = wsgi.start_service(app_mgr)
    if webapp:
        thr = hub.spawn(webapp)
        services.append(thr)

    # init dynamic loader cli
    cmd_line_app = DynamicLoadCmd()
    cmd_line_app.ryu_mgr = app_mgr
    cmd_line_app.services = services
    cmd_thr = hub.spawn()
    cmd_line_app.loop_thr = cmd_thr
    # services.append(thr)

    try:
        cmd_line_app.cmdloop()

        for thr in services:
            hub.kill(thr)
        hub.joinall(services)
    finally:
        app_mgr.close()

if __name__ == '__main__':
    main()
    















