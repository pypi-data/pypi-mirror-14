# Copyright Louis Paternault 2016
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""A coverage.py plugin to cheat and get 100% test coverage.

This file contains some helper functions.
"""

import logging
import pkgutil
import sys

VERSION = "0.1.0"
__AUTHOR__ = "Louis Paternault (spalax@gresille.org)"
__COPYRIGHT__ = "(C) 2016 Louis Paternault. GNU GPL 3 or later."

def import_all(package):
    """Recursively import all subpackages of this package, and does nothing with them."""
    for module_finder, name, __ispkg in pkgutil.walk_packages(package.__path__):
        if name not in sys.modules:
            try:
                module_finder.find_spec(name).loader.load_module()
            except Exception as error: # pylint: disable=broad-except
                logging.error("Could not import package '{}': {}.".format(name, str(error)))
                continue
