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

import pytest
import mock

from clog.metrics_reporter import MetricsReporter


@pytest.mark.acceptance_suite
class TestMetricsReporter(object):

    @mock.patch('clog.metrics_reporter.MetricsReporter._sample_log_line_sent.count')
    def test_metrics_reporter_sampling(self, mock_sample_log_line_sent_count):
        metrics = MetricsReporter()
        assert metrics._sample_counter == 0
        # First try, not part of sample
        with metrics.sampled_request(sample_rate=3):
            assert not mock_sample_log_line_sent_count.called
            assert metrics._sample_counter == 1
        assert not mock_sample_log_line_sent_count.called

        # Second try, not part of sample
        with metrics.sampled_request(sample_rate=3):
            assert not mock_sample_log_line_sent_count.called
            assert metrics._sample_counter == 2
        assert not mock_sample_log_line_sent_count.called

        # Third try, part of sample, so called outside the context
        with metrics.sampled_request(sample_rate=3):
            assert not mock_sample_log_line_sent_count.called
            assert metrics._sample_counter == 0
        assert mock_sample_log_line_sent_count.called is True


