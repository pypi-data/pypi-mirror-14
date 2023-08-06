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
import subprocess

from ulint import ULinter


class Linter(ULinter):
    @staticmethod
    def getInfoURI():
        return 'https://pypi.python.org/pypi/pep8'

    @staticmethod
    def getInfoName():
        return 'Python PEP8 code checker'

    @staticmethod
    def getInfoDescription():
        return 'Python style guide checker'

    @staticmethod
    def getLinterName():
        return 'PEP8'

    @staticmethod
    def getLinterConfigurationName():
        return 'pep8'

    @staticmethod
    def getDefaultBinary():
        return 'pep8'

    def getVersion(self):
        return subprocess.check_output('%s --version' % self.binary)

    @staticmethod
    def getInstallInstructions(self):
        return 'Install pep8 with `pip install pep8`'
