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

from mad.evaluation import Symbols
from mad.simulation.commons import SimulatedEntity
from mad.simulation.events import Listener


MISSING_VALUE = "NA"


class Statistics(Listener):

    def __init__(self):
        super().__init__()
        self.total_request_count = 0
        self.request_count = 0
        self.rejection_count = 0
        self.error_response_count = 0

    def reset(self):
        self.rejection_count = 0
        self.request_count = 0
        self.error_response_count = 0

    @property
    def reliability(self):
        total = self.request_count
        if total == 0:
            return None
        return self.success_count / total

    @property
    def success_count(self):
        error_count = (self.rejection_count + self.error_response_count)
        return self.request_count - error_count

    def arrival_of(self, request):
        self.request_count += 1
        self.total_request_count += 1

    def rejection_of(self, request):
        self.rejection_count += 1

    def success_of(self, request):
        pass

    def failure_of(self, request):
        pass

    def timeout_of(self, request):
        pass

    def posting_of(self, service, request):
        pass

    def selection_of(self, request):
        pass

    def storage_of(self, request):
        pass

    def resuming(self, request):
        pass

    def error_replied_to(self, request):
        self.error_response_count += 1

    def success_replied_to(self, request):
        pass


class Probe:

    def __init__(self, name, width, format, probe):
        self.name = name
        self.width = width
        self.format = format
        self.probe = probe

    def formatted(self, context):
        return ("{:>%d}" % self.width).format(self._as_text(context))

    def _as_text(self, context):
        value = self.measure(context)
        if value is None:
            return "{:s}".format(MISSING_VALUE)
        else:
            return self.format.format(value)

    def measure(self, context):
        return self.probe(context)


class Monitor(SimulatedEntity):
    """
    Monitors the various metrics from other components of the services (task pool, worker pool, etc.) and reports on
    a fixed period
    """
    DEFAULT_PERIOD = 10

    DEFAULT_PROBES = [
        Probe("time", 6, "{:d}", lambda self: self.schedule.time_now),
        Probe("queue length", 4, "{:d}", lambda self: self._queue_length()),
        Probe("utilisation", 10, "{:5.2f}", lambda self: self._utilisation()),
        Probe("worker count", 4, "{:d}", lambda self: self._worker_count()),
        Probe("arrival rate", 10, "{:5.2f}", lambda self: self._arrival_rate()),
        Probe("rejection rate", 10, "{:5.2f}", lambda self: self._rejection_rate()),
        Probe("reliability", 10, "{:5.2f}", lambda self: self._reliability()),
        Probe("throughput", 10, "{:5.2f}", lambda self: self._throughput())
    ]

    def __init__(self, name, environment, period):
        super().__init__(name, environment)
        self.period = period or self.DEFAULT_PERIOD
        self.probes = self.DEFAULT_PROBES
        self.report = self._create_report(self._header_format())
        self.statistics = Statistics()
        self.listener.register(self.statistics)
        self.schedule.every(self.period, self.monitor)

    def set_probes(self, probes):
        assert len(probes) > 0, "Invalid monitoring: No probes given!"
        self.probes = probes
        self.report = self._create_report(self._header_format())

    def _create_report(self, format):
        name = self.look_up(Symbols.SERVICE).name
        return self.simulation._storage.report_for(name, format)

    def _header_format(self):
        return [(each_probe.name, "%s") for each_probe in self.probes]

    def monitor(self):
        observations = {}
        for each_probe in self.probes:
            observations[each_probe.name] = each_probe.formatted(self)
        self.report(**observations)
        self.statistics.reset()

    def _queue_length(self):
        task_pool = self.look_up(Symbols.QUEUE)
        return task_pool.size

    def _utilisation(self):
        service = self.look_up(Symbols.SERVICE)
        return service.workers.utilisation

    def _worker_count(self):
        service = self.look_up(Symbols.SERVICE)
        return service.worker_count

    def _arrival_rate(self):
        return self.statistics.request_count / self.period

    def _rejection_rate(self):
        return self.statistics.rejection_count / self.period

    def _reliability(self):
        return self.statistics.reliability

    def _throughput(self):
        return self.statistics.success_count / self.period

class Logger(SimulatedEntity, Listener):
    REQUEST_ARRIVAL = "Req. %d accepted"
    REQUEST_STORED = "Req. %d enqueued"
    REQUEST_FAILURE = "Req. %d failed"
    REQUEST_SUCCESS = "Req. %d complete"
    REQUEST_SENT = "Sending Req. %d to %s::%s"
    REQUEST_TIMEOUT = "Req. %d timeout!"
    ERROR_REPLIED = "Reply to Req. %d (ERROR)"
    SUCCESS_REPLIED = "Reply to Req. %d (SUCCESS)"

    def __init__(self, environment):
        SimulatedEntity.__init__(self, Symbols.LOGGER, environment)
        Listener.__init__(self)
        self.listener.register(self)

    def resuming(self, request):
        pass

    def error_replied_to(self, request):
        self._log(self.ERROR_REPLIED, request.identifier)

    def rejection_of(self, request):
        pass

    def arrival_of(self, request):
        self._log(self.REQUEST_ARRIVAL, request.identifier)

    def selection_of(self, request):
        pass

    def failure_of(self, request):
        self._log(self.REQUEST_FAILURE, request.identifier)

    def success_of(self, request):
        self._log(self.REQUEST_SUCCESS, request.identifier)

    def posting_of(self, service, request):
        self._log(self.REQUEST_SENT, (request.identifier, service, request.operation))

    def success_replied_to(self, request):
        self._log(self.SUCCESS_REPLIED, request.identifier)

    def timeout_of(self, request):
        self._log(self.REQUEST_TIMEOUT, request.identifier)

    def storage_of(self, request):
        self._log(self.REQUEST_STORED, request.identifier)

    def _log(self, message, values):
        now = self.schedule.time_now
        caller = self.look_up(Symbols.SELF)
        self.simulation.log.record(now, caller.name, message % values)
