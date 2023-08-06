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


class Request:

    def __init__(self, sender, operation, on_success=lambda: None, on_error=lambda: None):
        assert sender, "Invalid sender (found %s)" % str(sender)
        self.identifier = sender.simulation.next_request_id()
        self.sender = sender
        self.operation = operation
        self.on_success = on_success
        self.on_error = on_error

    def send_to(self, service):
        service.process(self)

    def reply_success(self):
        self.on_success()

    def reply_error(self):
        self.on_error()