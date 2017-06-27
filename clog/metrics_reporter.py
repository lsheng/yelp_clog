# -*- coding: utf-8 -*-
# Copyright 2017 Yelp Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from contextlib import contextmanager

from yelp_meteorite import create_counter
from yelp_meteorite import create_timer

METRICS_SAMPLE_PREFIX = 'yelp_clog.sample.'
METRICS_SAMPLE_RATE = 1000  # TODO consider configuring this elsewhere
LOG_LINE_SENT = 'log_line.sent'
LOG_LINE_LATENCY = 'log_line.latency'


class MetricsReporter(object):
    """Basic metrics reporter that reports on a sampled fraction of requests"""

    _sample_counter = 0
    _sample_log_line_sent = create_counter(METRICS_SAMPLE_PREFIX + LOG_LINE_SENT)
    _sample_log_line_latency = create_timer(METRICS_SAMPLE_PREFIX + LOG_LINE_LATENCY)

    @contextmanager
    def sampled_request(self, sample_rate=METRICS_SAMPLE_RATE):
        """Context manager that records metrics if it's selected as part of the sample, otherwise runs as usual."""
        self._sample_counter += 1
        if self._sample_counter % sample_rate == 0:
            self._sample_counter = 0
            self._sample_log_line_latency.start()
            yield  # Do the actual work
            self._sample_log_line_latency.stop()
            self._sample_log_line_sent.count()
        else:
            yield  # Do the actual work
