# Copyright (c) 2016, Nutonian Inc
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#   * Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the Nutonian Inc nor the
#     names of its contributors may be used to endorse or promote products
#     derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL NUTONIAN INC BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import data_splitting
import complexity_weights
import math_block
import math_block_set
from solution import Solution
import time
import variable_options
from variable_options_dict import VariableOptionsDict
import json
from utils import Throttle
import warnings

class Search:
    """Represents a search on the server.

    :var str `~eureqa.search.Search.name`: The name of the search.
    :var ~eureqa.MathBlock `~eureqa.search.Search.math_blocks`: \
        The set of the :class:`~eureqa.MathBlock` objects which represents mathematical operations allowed to be \
        used by the search algorithm.  Use member properties to access the blocks; for example, \
        `~eureqa.MathBlockSet.add` to access the "add" MathBlock, etc. \
        Use `~eureqa.MathBlock.enable()` and `~eureqa.MathBlock.disable()` to enable or disable \
        a specific MathBlock.
    :var DataSplitting `~eureqa.search.Search.data_splitting`: The data splitting settings for the search algorithm.
    :var str `~eureqa.search.Search.error_metric`: One of the error metrics from :mod:`eureqa.error_metric`.
    :var int `~eureqa.search.Search.maximum_history_absolute_rows`: The maximum number of rows that can be used in range based functions.
    :var list `~eureqa.search.Search.prior_solutions`: The list of prior solutions.
    :var str `~eureqa.search.Search.row_weight`: The row weight expression.
    :var str `~eureqa.search.Search.target_expression`: The target expression.
    :var list `~eureqa.search.Search.variable_options`: The list of :class:`~eureqa.VariableOptions` objects.
    """

    def __init__(self, body, eureqa):
        """For internal use only"""

        self._id = body['search_id']
        self.name = body['search_name']
        self.math_blocks = math_block_set.MathBlockSet.from_json(body['building_blocks'])
        self._complexity_weights = complexity_weights._from_json(body['complexity_weights'])
        self.data_splitting = data_splitting._from_json(body)
        self._data_set_id = body['dataset_id']
        self.error_metric = body['error_metric']
        self._max_num_variables_per_term = body['max_num_variables_per_term']
        self._maximum_history_percentage = body.get('maximum_history_percent')
        self.maximum_history_absolute_rows = body.get('maximum_history_absolute_rows')
        self.prior_solutions = body['prior_solutions']
        self.row_weight = body['row_weight']
        self.row_weight_type = body['row_weight_type']
        self.target_expression = body['target_expression']
        self.variable_options = VariableOptionsDict.from_json(body['variable_options'])
        self._eureqa = eureqa
        self._body = body

    def _to_json(self):
        data_splitting_settings = {}
        self.data_splitting._to_json(data_splitting_settings)
        body_updates = {
            'name': self.name,
            'math_blocks': self.math_blocks._to_json(),
            'data_splitting': data_splitting_settings,
            'error_metric': self.error_metric,
            'maximum_history_absolute_rows': self.maximum_history_absolute_rows,
            'prior_solutions': self.prior_solutions,
            'row_weight': self.row_weight,
            'target_expression': self.target_expression,
            'variable_options': self.variable_options._to_json(),
            'is_running': self.is_running
        }
        body = dict(self._body)
        body.update(body_updates)
        return body

    def __str__(self):
        return json.dumps(self._to_json(), indent=4)

    def get_data_source(self):
        """ Retrieves from the server the data source information for this search.

        :rtype: ~eureqa.DataSource
        """

        data_source_id = self._eureqa._get_data_source_id(self._data_set_id)
        return self._eureqa.get_data_source_by_id(data_source_id)

    def delete(self):
        """Deletes the search from the server.

        :raise Exception: search is already deleted.
        """

        endpoint = '/fxp/datasets/%s/searches/%s' % (self._data_set_id, self._id)
        self._eureqa._session.report_progress('Deleting search: \'%s\' from dataset: \'%s\'.' % (self._id, self._data_set_id))
        self._eureqa._session.execute(endpoint, 'DELETE')

    def submit(self, time_seconds):
        """Submit the search to the server to run for the specified amount of time.

        This method does not guarantee to start the search immediately. The search can
        be queued for some time before it will start producing any results.

        :param int time_seconds:
            The maximum amount of time to run the search. The server will stop
            running the search once the running time will reach this limit.
        """


        # Eeb does not support updating the search while it is running. So it we cannot touch it
        # if it is running and we should execute this update before starting it.
        if not self.is_running:
            # This drive how UI display the search. It does not affect the engine.
            self._body['search_metadata']['date_started'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
            self._body['search_metadata']['stopping_condition'] = {'time_seconds': time_seconds, 'max_r2': 1}
            endpoint = '/fxp/datasets/%s/searches/%s' % (self._data_set_id, self._id)
            self._eureqa._session.report_progress('Updating metadata for search: \'%s\' from dataset: \'%s\'.' % (self._id, self._data_set_id))
            self._eureqa._session.execute(endpoint, 'PUT', self._body)

        endpoint = '/fxp/search_queue'
        body = {'dataset_id': self._data_set_id,
                'search_id': self._id,
                'stopping_condition':
                    {'time_seconds': time_seconds,
                     'max_r2': 1}}
        self._eureqa._session.report_progress('Submitting search: \'%s\' from dataset: \'%s\' to the search queue.' % (self._id, self._data_set_id))
        self._eureqa._session.execute(endpoint, 'POST', body)

    @property
    def is_running(self):
        """Indicates if the search currently running.

        :rtype: bool
        """
        updated_search = self._get_updated()._body['search_queue_summary']
        search_status = updated_search['search_queue_state']
        # The endpoint is returning the internal state of the search queue, which treats
        # queueing states as not running.
        return search_status not in {'', 'QS_NONE', 'QS_DONE', 'QS_ABORTED'}

    def stop(self):
        """Stops running the search."""

        endpoint = '/fxp/search_queue/stop'
        body = {'dataset_id': self._data_set_id, 'search_id': self._id}
        self._eureqa._session.report_progress('Stopping search: \'%s\' from dataset: \'%s\'.' % (self._id, self._data_set_id))
        self._eureqa._session.execute(endpoint, 'POST', body)
        self.wait_until_done()

    def wait_until_done(self, show_progress=False, poll_seconds=5, print_callback=None):
        """Waits until the search stops running.

        :param bool show_progress: whether to print the search progress while waiting.
        :param int poll_seconds: number of seconds to wait between checking progress.
        :param function print_callback: method to invoke to print the progress (sys.stdout.write by default).
        """

        if print_callback is None:
            import sys
            print_callback = sys.stdout.write

        prev_solution_string = ''
        while self.is_running:

            if show_progress:
                progress_string = self._get_progress_summary()
                solution_string = self._get_solutions_summary()
                print_callback(progress_string)
                if solution_string != prev_solution_string:
                    prev_solution_string = solution_string
                    print_callback('\n%s' % solution_string)

            time.sleep(poll_seconds)

    def _get_progress_summary(self):
        """Returns convenience values of the search progress."""
        search = self._get_updated()._body
        queue  = search['search_queue_summary']

        return 'Search="%s", remaining: %is, converged=%.2g%%, cores=%i, evals=%.4gM (%.2gM e/s), gens=%g (%.4g g/s)' % (
            search['search_name'],
            queue['estimated_time_remaining_seconds'],
            search['search_percent_converged'],
            search['search_cpu_cores'],
            search['search_evaluations']/1e6, search['search_evaluations_per_second']/1e6,
            search['search_generations'],     search['search_generations_per_second'])

    def _get_solutions_summary(self):
        ret = ''
        for s in self.get_solutions():
            ret += '%i, %.4g, [ %s ]\n' % (s.complexity,
                s.optimized_error_metric_value, ', '.join(s.terms))
        return ret

    @Throttle()
    def get_solutions(self):
        """Retrieves from the server the list of solutions found so far.

        This method can be called while the search is running to check what searches are
        already found and make a decision whether continue the search.

        :return: list of :class:`~eureqa.Solution` objects.
        :rtype: list
        """

        endpoint = '/fxp/datasets/%s/searches/%s/solutions' % (self._data_set_id, self._id)
        self._eureqa._session.report_progress('Getting solutions for search: \'%s\' from dataset: \'%s\'.' % (self._id, self._data_set_id))
        body = self._eureqa._session.execute(endpoint, 'GET')
        return [Solution(x, self) for x in body]

    def get_best_solution(self):
        """Retrieves from the server the best solution found so far.

        :rtype: Solution
        """

        solutions = self.get_solutions()
        return next((x for x in solutions if x.is_best), None)

    def get_most_accurate_solution(self):
        """Retrieves from the server the most accurate solution found so far.

        :rtype: Solution
        """

        solutions = self.get_solutions()
        if not solutions: return None
        return next((x for x in solutions if x.is_most_accurate), None)
        
    def create_solution(self, solution_string, use_all_data=False):
        """Creates a custom solution for the search.
        Use this if you want to compute error metrics and other statistics of a specified expression. 
        It is also useful to compare how well a known model does against one found by Eureqa
        
        :param string solution_string: the right hand side of the expression.
        :param bool use_all_data: whether to use all data or just validation data when calculating the metrics for the solution.

        :rtype: Solution
        """

        endpoint = '/fxp/datasets/%s/searches/%s/solutions' % (self._data_set_id, self._id)
        body = {'dataset_id': self._data_set_id,
                'search_id': self._id,
                'solution_string': solution_string,
                'use_all_data': use_all_data}
        result = self._eureqa._session.execute(endpoint, 'POST', body)
        return Solution(result, self)

    @Throttle()
    def _get_updated(self):
        return self._eureqa._get_search_by_search_id(self._data_set_id, self._id)

    def evaluate_expression(self, expressions, data_split='all'):
        warnings.warn("This function has been deprecated.  Please use `Eureqa.evaluate_expression()` instead.", DeprecationWarning)
        return self._eureqa.evaluate_expression(self._data_set_id, expressions, self, data_split=data_split)
