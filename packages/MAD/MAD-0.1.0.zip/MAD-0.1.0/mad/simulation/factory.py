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

from mad.scheduling import Scheduler
from mad.environment import Environment
from mad.evaluation import Symbols, Evaluation, SimulationFactory

from mad.simulation.service import Service, Operation
from mad.simulation.client import ClientStub
from mad.simulation.tasks import FIFOTaskPool, LIFOTaskPool
from mad.simulation.autoscaling import RuleBasedStrategy, AutoScaler
from mad.simulation.requests import Request
from mad.simulation.throttling import NoThrottling, TailDrop


class Factory(SimulationFactory):
    """
    Instantiate all necessary elements for a simulation
    """

    def create_simulation(self, data_store):
        return Simulation(data_store)

    def create_autoscaler(self, environment, autoscaling):
        strategy = RuleBasedStrategy(70, 80)
        return AutoScaler(environment, autoscaling.period, autoscaling.limits, strategy)

    def create_FIFO_task_pool(self):
        return FIFOTaskPool()

    def create_LIFO_task_pool(self):
        return LIFOTaskPool()

    def create_service(self, name, environment):
        return Service(name, environment)

    def create_client_stub(self, environment, definition):
        return ClientStub(definition.name, environment, definition.period, definition.body)

    def create_operation(self, environment, definition):
        return Operation(
            definition.name,
            definition.parameters,
            definition.body,
            environment
        )

    def create_request(self, sender, operation, on_success=lambda: None, on_error=lambda: None):
        return Request(sender, operation, on_success, on_error)

    def create_no_throttling(self):
        return NoThrottling()

    def create_tail_drop(self, capacity, task_pool):
        return TailDrop(capacity, task_pool)


class Simulation:
    """
    Represent the general simulation, including the current schedule and the associated trace
    """
    # TODO: This should inherits from SimulatedEntity as well

    def __init__(self, storage):
        self._storage = storage
        self._scheduler = Scheduler()
        self.environment = Environment()
        self.environment.define(Symbols.SIMULATION, self)
        self._next_request_id = 1
        self.factory = Factory()

    def run_until(self, end, display=None):
        self._scheduler.simulate_until(end, display)

    @property
    def log(self):
        return self._storage.log

    @property
    def schedule(self):
        return self._scheduler

    def evaluate(self, expression):
        return Evaluation(self.environment, expression, self.factory).result

    def next_request_id(self):
        id = self._next_request_id
        self._next_request_id += 1
        return id

    @property
    def services(self):
        return self._find_by_type(Service)

    @property
    def clients(self):
        return self._find_by_type(ClientStub)

    def _find_by_type(self, type):
        return [each_value
                for each_value in self.environment.bindings.values()
                if isinstance(each_value, type)]