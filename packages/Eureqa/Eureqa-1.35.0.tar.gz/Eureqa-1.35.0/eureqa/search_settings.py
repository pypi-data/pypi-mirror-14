# Copyright (c) 2016, Nutonian Inc
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# * Redistributions of source code must retain the above copyright
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

"""Templates for search settings:"""

from data_splitting import DataSplitting
from complexity_weights import ComplexityWeights
from math_block_set import MathBlockSet
import json
import math_block
import math_block_set
from variable_options import VariableOptions
from variable_options_dict import VariableOptionsDict


class SearchSettings(object):
    """A set of settings which should be passed into :py:func:`~eureqa.DataSource.create_search`
    Use one of the templates from :py:func:`~eureqa.Eureqa.search_templates` to create an instance of this class.

    :var str `~eureqa.search_settings.SearchSettings.name`: The name of the search.
    :var list `~eureqa.search_settings.SearchSettings.math_blocks`:
        The list of the :class:`~eureqa.MathBlock` objects which represents mathematical operations allowed to be
        used by the search algorithm.
    :var DataSplitting `~eureqa.search_settings.SearchSettings.data_splitting`: The data splitting settings for the search algorithm.
    :var str `~eureqa.search_settings.SearchSettings.error_metric`: One of the error metrics from :mod:`eureqa.error_metric`.
    :var int `~eureqa.search_settings.SearchSettings.maximum_history_absolute_rows`: The maximum number of rows that can be used in range based functions.
    :var list `~eureqa.search_settings.SearchSettings.prior_solutions`: The list of prior solutions.
    :var str `~eureqa.search_settings.SearchSettings.row_weight`: The row weight expression.
    :var str `~eureqa.search_settings.SearchSettings.row_weight_type`: The row weight type expression.  The default, 'uniform', requires `~eureqa.search_settings.SearchSettings.row_weight` to be unspecified.  'custom' allows arbitrary expressions.
    :var str `~eureqa.search_settings.SearchSettings.target_expression`: The target expression.
    """

    def __init__(self, name, data_splitting,
                 error_metric, max_num_variables_per_term, prior_solutions,
                 target_expression, row_weight_type='uniform', row_weight=1.0,
                 maximum_history_percentage=None,
                 maximum_history_absolute_rows=None):

        self._body = {'search_metadata': {
            'search_specification': {'type': "GENERIC"},
        }}

        self.name = name
        self.math_blocks = MathBlockSet()
        self._complexity_weights = ComplexityWeights()
        self.data_splitting = data_splitting
        self.error_metric = error_metric
        self._max_num_variables_per_term = max_num_variables_per_term
        self._maximum_history_percentage = maximum_history_percentage
        self.maximum_history_absolute_rows = maximum_history_absolute_rows
        self.prior_solutions = prior_solutions
        self.row_weight = row_weight
        self.row_weight_type = row_weight_type
        self.target_expression = target_expression
        self.variable_options = VariableOptionsDict()

    @property
    def target_expression(self):
        """ The target expression to optimize.

        Only set if a custom expression is required.
        If set, the resulting search will be treated as an "Advanced"
        search in the UI; the variable chooser will be replaced with
        an expression editor.
        """
        return self._target_expression
    @target_expression.setter
    def target_expression(self, val):
        self._target_expression = val
        self._body['search_metadata']['target_expression_edited'] = True
    @target_expression.deleter
    def target_expression(self):
        # Deleting a custom target_expression reverts to the default
        assert hasattr(self, '_original_target_expression'), "Can't delete the target expression:  Was not created from a template; no default to fall back to."
        self._target_expression = self._original_target_expression
        if 'target_expression_edited' in self._body['search_metadata']:
            del self._body['search_metadata']['target_expression_edited']

    @classmethod
    def from_json(cls, body):
        name = body['search_name']
        target_expression = body['target_expression']
        error_metric = body['error_metric']
        max_num_variables_per_term = body['max_num_variables_per_term']
        row_weight = body['row_weight']
        row_weight_type = body['row_weight_type']
        data_splitting = DataSplitting.from_json(body)
        maximum_history_absolute_rows = body[
            'maximum_history_absolute_rows'] if 'maximum_history_absolute_rows' in body else None
        maximum_history_percentage = body['maximum_history_percent'] if 'maximum_history_percent' in body else None
        prior_solutions = body['prior_solutions']
        ss = SearchSettings(name=name,
                            data_splitting=data_splitting,
                            error_metric=error_metric,
                            max_num_variables_per_term=max_num_variables_per_term,
                            prior_solutions=prior_solutions,
                            row_weight=row_weight,
                            row_weight_type=row_weight_type,
                            target_expression=target_expression,
                            maximum_history_percentage=maximum_history_percentage,
                            maximum_history_absolute_rows=maximum_history_absolute_rows)
        ss.math_blocks = math_block_set.MathBlockSet.from_json(body['building_blocks'])     
        ss.variable_options._from_json(body['variable_options'])
        ss._original_target_expression = target_expression
        return ss

    def _to_json(self):
        self._body['search_name'] = self.name
        self._body['target_expression'] = self.target_expression
        self._body['error_metric'] = self.error_metric
        self._body['max_num_variables_per_term'] = self._max_num_variables_per_term
        self._body['row_weight'] = self.row_weight
        self._body['row_weight_type'] = self.row_weight_type
        self.data_splitting._to_json(self._body)
        if self.maximum_history_absolute_rows is not None:
            self._body['maximum_history_absolute_rows'] = self.maximum_history_absolute_rows
        elif self._maximum_history_percentage is not None:
            self._body['maximum_history_percent'] = self._maximum_history_percentage
        self._body['building_blocks'] = [x._to_json() for x in self.math_blocks]
        self._body['complexity_weights'] = self._complexity_weights._to_json()
        self._body['variable_options'] = self.variable_options._to_json()
        self._body['prior_solutions'] = self.prior_solutions
        return self._body

    def __str__(self):
        return json.dumps(self._to_json())
