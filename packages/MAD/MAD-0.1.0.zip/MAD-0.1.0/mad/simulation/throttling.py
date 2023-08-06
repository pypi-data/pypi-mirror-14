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

from mad.simulation.tasks import TaskPool

NEGATIVE_CAPACITY = "Capacity must be strictly positive, but found {capacity:d}"
INVALID_CAPACITY = "Capacity must be an integer, but found '{object.__class__.__name__:s}'"
INVALID_TASK_POOL = "TaskPool object required, but found '{object.__class__.__name__:s}'"


class ThrottlingPolicy:
    """
    Common interface of all throttling policies
    """

    def accepts(self, task):
        raise NotImplementedError("ThrottlingPolicy::accept(task) is abstract!")

    @property
    def rejection_count(self):
        raise NotImplementedError("ThrottlingPolicy::rejection_count is abstract")


class NoThrottling(ThrottlingPolicy):
    """
    Default policy: Always accept requests.
    """

    def accepts(self, task):
        return True;

    @ThrottlingPolicy.rejection_count.getter
    def rejection_count(self):
        return 0


class TailDrop(ThrottlingPolicy):
    """
    Reject requests once the given task pool size reaches the
    specified capacity
    """

    def __init__(self, capacity, task_pool):
        super().__init__()
        assert isinstance(capacity, int), INVALID_CAPACITY.format(object=capacity)
        assert capacity > 0, NEGATIVE_CAPACITY.format(capacity=capacity)
        self.capacity = capacity
        assert isinstance(task_pool, TaskPool), INVALID_TASK_POOL.format(object=task_pool)
        self.task_pool = task_pool
        self._rejection = 0

    def accepts(self, task):
        if self.task_pool.size >= self.capacity:
            self._rejection += 1
            return False
        return True

    @ThrottlingPolicy.rejection_count.getter
    def rejection_count(self):
        return self._rejection