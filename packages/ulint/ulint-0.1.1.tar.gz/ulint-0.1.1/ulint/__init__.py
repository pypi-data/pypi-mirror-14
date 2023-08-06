#
# ulint: Tool to easily lint code
#
# Copyright (C) 2016  Thibault Saunier <tsaunier@gnome.org>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, If not, see
# http://www.gnu.org/licenses/.

import json
import os
import pip
import re
import subprocess

import git
from collections import namedtuple
from pkg_resources import iter_entry_points


class ConfigError(Exception):
    pass


def _check_include(f, includes, excludes):
    for exclude in excludes:
        for f in files:
            if re.findall(exclude, f):
                return False

    for include in includes:
        if re.findall(include, f):
            return True

    return not includes


class ULinter:
    def __init__(self, name, config, files):
        self.name = name
        self.binary = self.getDefaultBinary()

        includes = config.get("include", [])
        if not isinstance(includes, list):
            includes = [includes]

        excludes = config.get("exclude", [])
        if not isinstance(excludes, list):
            excludes = [excludes]

        files = [f for f in files if _check_include(f, includes, excludes)]

        self.__dict__.update(config)
        for k, v in config.items():
            if isinstance(v, dict):
                self.__dict__[k] = Struct(v)

        self.files = files

    @staticmethod
    def getInfoURI():
        raise NotImplementedError()

    @staticmethod
    def getInfoName():
        raise NotImplementedError()

    @staticmethod
    def getInfoDescription():
        raise NotImplementedError()

    @staticmethod
    def getLinterName():
        raise NotImplementedError()

    @staticmethod
    def getLinterConfigurationName():
        raise NotImplementedError()

    @staticmethod
    def getDefaultBinary():
        raise NotImplementedError()

    def getVersion(self):
        raise NotImplementedError()

    @staticmethod
    def getInstallInstructions():
        raise NotImplementedError()

    @classmethod
    def get_linter(cls, name, config, files):
        for linter in iter_entry_points('ulint.linters'):
            if linter.name == config["type"]:
                return linter.load()(name, config, files)

        return None

    def get_args(self):
        return self.files

    def run(self):
        print("Running %s: %s" % (
            self.getLinterName(), self.getInfoDescription()), end="")
        try:
            args = [self.binary]
            args.extend(self.get_args())
            res = subprocess.check_output(args)
            print("... OK")
        except subprocess.CalledProcessError as e:
            print("... FAILED:\n %s" % (e.stdout.decode("utf-8")))
            return False

        return True


class LintersConfig:
    def __init__(self, config, all_files):
        if not config.get("linters"):
            raise ConfigError("Add a 'linters' entry in you `u.lint` file")

        excludes = config.get("exclude")
        if excludes and not isinstance(excludes, list):
            excludes = [excludes]

        if excludes:
            for exclude in excludes:
                for f in all_files:
                    if re.findall(exclude, f):
                        all_files.pop(f)

        self.linters = []
        for linter_name, linter_desc in config["linters"].items():
            if not linter_desc.get("type"):
                raise ConfigError("Add a 'type' entry for " + linter_name)

            linter = ULinter.get_linter(linter_name, linter_desc, all_files)
            if not linter:
                raise ConfigError("Could not find a linter of type %s" %
                                  linter_desc["type"])

            self.linters.append(linter)

    def run(self):
        res = True
        for linter in self.linters:
            if linter.files and not linter.run():
                res = False
        return res


def git_lint():
    repo = git.Repo(os.getcwd(), search_parent_directories=True)

    deffile = os.path.join(repo.working_dir, ".u.lint")

    if not os.path.exists(deffile):
        deffile = os.path.join(repo.working_dir, ".arclint")
        if not os.path.exists(deffile):
            print("ERROR: No lint description file found.\n\n"
                  "Add a `.u.lint` file at the root directory"
                  " of your git repository")
            return False

    all_files = repo.git.diff("--cached", "--name-only", "-r")
    if not all_files:
        all_files = repo.git.ls_tree("--name-only", "-r", "HEAD")
        print("Checking commit: %s" % repo.head.object.hexsha)
    else:
        print("Checking changes to be commited")

    if all_files:
        all_files = all_files.split("\n")
    else:
        print("No file to check")
        return False

    with open(deffile) as _f:
        config = LintersConfig(json.load(_f), all_files)

    res = config.run()

    return res
