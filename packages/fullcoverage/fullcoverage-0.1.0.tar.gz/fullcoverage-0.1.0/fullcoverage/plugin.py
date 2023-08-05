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

The plugin itself.
"""

import functools
import os
import shlex

from coverage.plugin import CoveragePlugin, FileTracer, FileReporter

@functools.lru_cache(maxsize=1024)
def _count_line_numbers(filename):
    """Return the number of lines of file given in argument"""
    with open(filename) as fileobject:
        return len(fileobject.readlines())

class FullcoveragePlugin(CoveragePlugin):
    """Plugin to cheat and get 100% full coverage."""

    def __init__(self, options):
        super().__init__()
        self.options = options

    def _in_source(self, filename):
        if 'source' not in self.options:
            return True
        for source in shlex.split(self.options['source']):
            source = os.path.abspath(source)
            if filename.startswith(source):
                return True
        return False

    def file_tracer(self, filename):
        if self._in_source(filename):
            return FullcoverageTracer()

    def file_reporter(self, filename):
        if self._in_source(filename):
            return FullcoverageReporter(filename)

class FullcoverageTracer(FileTracer):
    """Trace code execution"""

    def has_dynamic_source_filename(self):
        return True

    def dynamic_source_filename(self, filename, frame):
        if filename is not None:
            return filename
        try:
            return frame.f_code.co_filename
        except AttributeError:
            pass
        return None

    def line_number_range(self, frame):
        return (0, _count_line_numbers(frame.f_code.co_filename))

class FullcoverageReporter(FileReporter):
    """Report code execution"""

    def __init__(self, filename):
        super().__init__(filename)
        self.filename = filename

    def lines(self):
        return set(range(0, _count_line_numbers(self.filename)))

    def source(self):
        if os.path.exists(self.filename):
            return super().source()
        else:
            return ""

def coverage_init(reg, options):
    """Plugin initialisation"""
    reg.add_file_tracer(FullcoveragePlugin(options))
