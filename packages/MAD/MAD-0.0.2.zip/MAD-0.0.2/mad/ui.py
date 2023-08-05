#!/usr/bin/env python

#
# This file is part of MAD.
#
# MAD is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# MAD is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with MAD.  If not, see <http://www.gnu.org/licenses/>.
#

from mad import __version__ as MAD_VERSION

from mad.datasource import Project


class Display:
    """
    Abstract the display where that report and format the progress of the simulation
    """

    def __init__(self, output):
        self.output = output

    def boot_up(self):
        self.output.write("MAD %s \n" % MAD_VERSION)
        self.output.write("Copyright (c) 2015 - 2016 Franck CHAUVEL\n")
        self.output.write("\n")
        self.output.write("This program comes with ABSOLUTELY NO WARRANTY.\n"
                          "This is free software, and you are welcome to redistribute it\n"
                          "under certain conditions.\n")
        self.output.write("\n")

    def simulation_started(self, project):
        self.output.write("Loading '%s'\n" % project.file_name)

    def update(self, current_time, end):
        progress = current_time / end * 100
        self.output.write("\rSimulation %d %%" % progress)

    def simulation_complete(self, project):
        self.output.write("\nSee results in '%s'\n" % project.output_directory)


class CommandLineInterface:
    """
    Control the interaction between the simulation and the display
    """

    def __init__(self, display, mad):
        self.display = display
        self.mad = mad

    def simulate(self, project):
        self.display.boot_up()
        self.display.simulation_started(project)
        simulation = self.mad.load(project)
        simulation.run_until(project.limit, self.display)
        self.display.simulation_complete(project)


class Arguments:
    """
    Convert the arguments given on the command line into a MadProject
    """

    def __init__(self, arguments):
        self._arguments = arguments
        self._file_name = self._extract_file_name()
        self._time_limit = self._extract_length()

    def _extract_file_name(self):
        result = self._arguments[0]
        if not isinstance(result, str):
            raise ValueError("Expecting 'MAD file' as Argument 1, but found '%s'" % self._arguments[0])
        return result

    def _extract_length(self):
        try:
            return int(self._arguments[1])
        except ValueError:
            raise ValueError("Expecting simulation length as Argument 2, but found '%s'" % self._arguments[1])

    @property
    def as_project(self):
        return Project(self._file_name, self._time_limit)

