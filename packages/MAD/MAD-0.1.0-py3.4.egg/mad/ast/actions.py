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

from mad.ast.commons import Expression


class Action(Expression):
    """
    Abstract all action that can be performed within an operation
    """

    def __init__(self):
        super().__init__()

    def accept(self, evaluation):
        raise NotImplementedError("Action::accept(evaluation) is abstract!")


class Invocation(Action):
    """
    Abstract invocation of a remote operation
    """

    def __init__(self, service, operation):
        super().__init__()
        self.service = service
        self.operation = operation

    def accept(self, evaluation):
        raise NotImplementedError("Invocation::accept(evaluation) is abstract!")


class Trigger(Invocation):
    """
    An non-blocking invocation of a remote operation
    """

    def __init__(self, service, operation):
        super().__init__(service, operation)

    def accept(self, evaluation):
        return evaluation.of_trigger(self)

    def __repr__(self):
        return "Trigger(%s, %s)" % (self.service, self.operation)


class Query(Invocation):
    """
    A blocking invocation of a remote operation
    """

    def __init__(self, service, operation):
        super().__init__(service, operation)

    def accept(self, evaluation):
        return evaluation.of_query(self)

    def __repr__(self):
        return "Query(%s, %s)" % (self.service, self.operation)


class Think(Action):
    """
    Simulate a local time-consuming computation
    """

    def __init__(self, duration):
        super().__init__()
        self.duration = duration

    def accept(self, evaluation):
        return evaluation.of_think(self)

    def __repr__(self):
        return "Think(%d)" % self.duration


class Retry:
    """
    Retry an action a given number of time
    """

    def __init__(self, expression, limit):
        self.expression = expression
        assert limit > 0, "Retry limit must be strictly positive (found %d)" % limit
        self.limit = limit

    def accept(self, evaluation):
        return evaluation.of_retry(self)

    def __repr__(self):
        return "Retry(%s, %d)" % (str(self.expression), self.limit)


class IgnoreError:
    """
    Ignore error occuring during the evaluation of the given expression
    """

    def __init__(self, expression):
        self.expression = expression

    def accept(self, evaluation):
        return evaluation.of_ignore_error(self)

    def __repr__(self):
        return "IgnoreError(%s)" % str(self.expression)
