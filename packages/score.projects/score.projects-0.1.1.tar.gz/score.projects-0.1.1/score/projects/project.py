# Copyright © 2015 STRG.AT GmbH, Vienna, Austria
#
# This file is part of the The SCORE Framework.
#
# The SCORE Framework and all its parts are free software: you can redistribute
# them and/or modify them under the terms of the GNU Lesser General Public
# License version 3 as published by the Free Software Foundation which is in the
# file named COPYING.LESSER.txt.
#
# The SCORE Framework and all its parts are distributed without any WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. For more details see the GNU Lesser General Public
# License.
#
# If you have not received a copy of the GNU Lesser General Public License see
# http://www.gnu.org/licenses/.
#
# The License-Agreement realised between you as Licensee and STRG.AT GmbH as
# Licenser including the issue of its valid conclusion and its pre- and
# post-contractual effects is governed by the laws of Austria. Any disputes
# concerning this License-Agreement including the issue of its valid conclusion
# and its pre- and post-contractual effects are exclusively decided by the
# competent court, in whose district STRG.AT GmbH has its registered seat, at
# the discretion of STRG.AT GmbH also the competent court, in whose district the
# Licensee has his registered seat, an establishment or assets.

import os
from vex.main import _main as vex_main
from score.cli.conf import rootdir, make_default, add as addconf


class Project:

    @staticmethod
    def register(conf, name, folder):
        project = Project(conf, name, folder)
        project.recreate_venv()
        for name in ('production', 'development', 'local'):
            addconf(name, os.path.join(project.folder, '%s.conf' % name),
                    venv=project.venvdir)
        make_default('local', venv=project.venvdir)
        return project

    def __init__(self, conf, name, folder):
        self.conf = conf
        self.name = name
        self.folder = folder

    def recreate_venv(self):
        self.vex('--make', 'true')
        self.install()

    def install(self):
        self.vex('pip', 'install', '--upgrade', 'pip')
        self.vex('pip', 'install', '--editable', self.folder)

    def spawn_shell(self):
        self.vex('--path', self.venvdir, '--cwd', self.folder)

    def vex(self, *args):
        environ = os.environ.copy()
        environ['VIRTUAL_ENV_NAME'] = self.name
        vex_main(environ, ('--path', self.venvdir) + args)

    @property
    def venvdir(self):
        return os.path.join(rootdir(global_=True), 'projects', self.name)

    @property
    def exists(self):
        return os.path.exists(self.folder)
