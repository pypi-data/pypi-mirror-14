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

from score.init import ConfiguredModule
from .project import Project
import os
from score.cli.conf import rootdir, name2file, add as addconf, get_origin
import configparser
import shutil


defaults = {
}


def init(confdict):
    conf = defaults.copy()
    conf.update(confdict)
    return ConfiguredProjectModule()


class ConfiguredProjectModule(ConfiguredModule):

    def __init__(self):
        import score.projects
        super().__init__(score.projects)

    def get(self, name):
        if isinstance(name, Project):
            return name
        try:
            return next(p for p in self if p.name == name)
        except StopIteration:
            raise ProjectNotFound(name)

    def relocate(self, name, folder):
        project = self.get(name)
        shutil.move(project.folder, folder)
        configurations = name2file(include_global=False, venv=project.venvdir)
        for name, path in configurations.items():
            path = get_origin(path)
            if not path.startswith(project.folder):
                continue
            relpath = os.path.relpath(path, project.folder)
            newpath = os.path.join(folder, relpath)
            addconf(name, newpath, venv=project.venvdir)
        project.folder = folder
        project.install()
        settings = self._read_conf()
        settings[project.name] = {'folder': folder}
        self._write_conf(settings)
        return project

    def rename(self, oldname, newname):
        project = self.get(oldname)
        oldname = project.name
        try:
            shutil.rmtree(project.venvdir)
        except FileNotFoundError:
            pass
        project.name = newname
        project.recreate_venv()
        settings = self._read_conf()
        del settings[oldname]
        settings[newname] = {'folder': project.folder}
        self._write_conf(settings)

    def delete(self, name):
        project = self.get(name)
        try:
            shutil.rmtree(project.folder)
        except FileNotFoundError:
            pass
        try:
            shutil.rmtree(project.venvdir)
        except FileNotFoundError:
            pass
        settings = self._read_conf()
        del settings[project.name]
        self._write_conf(settings)
        return project

    def register(self, name, folder):
        if name in self.all():
            raise ValueError('Project "%s" already exists' % name)
        project = Project.register(self, name, folder)
        settings = self._read_conf()
        settings[name] = {'folder': folder}
        self._write_conf(settings)
        return project

    def all(self):
        return dict((p.name, p) for p in self)

    def __iter__(self):
        settings = self._read_conf()
        for section in settings:
            if section == 'DEFAULT':
                continue
            folder = settings[section]['folder']
            yield(Project(self, section, folder))

    __getitem__ = get

    def _read_conf(self):
        root = os.path.join(rootdir(global_=True), 'projects')
        settings = configparser.ConfigParser()
        settings.read(os.path.join(root, 'list.conf'))
        return settings

    def _write_conf(self, settings):
        root = os.path.join(rootdir(global_=True), 'projects')
        file = os.path.join(root, 'list.conf')
        settings.write(open(file, 'w'))


class ProjectNotFound(Exception):
    pass
