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

from analysis_card import AnalysisCard
import json

class ModelEvaluatorCard(AnalysisCard):
    """Represents an evaluate model card on the server.

    :var str ~eureqa.analysis_cards.ModelEvaluatorCard.title: The title of the card
    :var tuple ~eureqa.analysis_cards.ModelEvaluatorCard.solution_infos: Immutable ordered set of SolutionInfo objects representing the solutions shown on this card.
    """

    class SolutionInfo(object):
        """ The solution information for a single model evaluation ("tab")
        on ModelEvaluatorCard
        
        :var str ~eureqa.analysis_cards.ModelEvaluatorCard.SolutionInfo.dataset_id: ID of the DataSet referenced by this solution-tab
        :var str ~eureqa.analysis_cards.ModelEvaluatorCard.SolutionInfo.datasource_id: ID of the DataSource referenced by this solution-tab
        :var str ~eureqa.analysis_cards.ModelEvaluatorCard.SolutionInfo.search_id: ID of the Search referenced by this solution-tab
        :var str ~eureqa.analysis_cards.ModelEvaluatorCard.SolutionInfo.solution_id: ID of the Solution referenced by this solution-tab
        :var bool ~eureqa.analysis_cards.ModelEvaluatorCard.SolutionInfo.has_target_variable: Whether the dataset contains the target variable
        """

        def __init__(self, card, backing_dict):
            self._card = card
            self._dict = backing_dict

        @property
        def dataset_id(self):
            """ID of the DataSet used for this solution

            :return: unique DataSet identifier
            """
            return self._dict['dataset_id']

        @dataset_id.setter
        def dataset_id(self, val):
            self._dict['dataset_id'] = val
            self._card._update_card()

        @property
        def datasource_id(self):
            """ID of the DataSource used for this solution

            :return: unique DataSource identifier
            """
            return self._dict['datasource_id']

        @datasource_id.setter
        def datasource_id(self, val):
            self._dict['datasource_id'] = val
            self._card._update_card()

        @property
        def search_id(self):
            """ID of the Search used for this solution

            :return: unique Search identifier
            """
            return self._dict['search_id']

        @search_id.setter
        def search_id(self, val):
            self._dict['search_id'] = val
            self._card._update_card()

        @property
        def solution_id(self):
            """ID of the Solution used for this solution

            :return: unique Solution identifier
            """
            return self._dict['solution_id']

        @solution_id.setter
        def solution_id(self, val):
            self._dict['solution_id'] = val
            self._card._update_card()
            
        @property
        def has_target_variable(self):
            """Whether the dataset contains the target variable

            :return: Whether the dataset contains the target variable
            """
            return self._dict['hasTargetVariable']

        @has_target_variable.setter
        def has_target_variable(self, val):
            self._dict['hasTargetVariable'] = val
            self._card._update_card()

    @property
    def title(self):
        """The title of this card.

        :return: title of this card
        :rtype: str"""
        return self._body['content']['title']

    @title.setter
    def title(self, value):
        self._body['content']['title'] = value
        self._update_card()

    @property
    def description(self):
        """ The description of this card.

        :return: description of this card
        :rtype: str"""
        return self._body['content']['description']

    @description.setter
    def description(self, value):
        self._body['content']['description'] = value
        self._update_card()
        
    @property
    def collapse(self):
        """Whether the card is collapsed by default.

        :return: whether the card is collapsed by default
        :rtype: str"""
        return self._body['collapse']

    @collapse.setter
    def collapse(self, value):
        self._body['collapse'] = value
        self._update_card()

    def add_solution_info(self, datasource, solution):
        """Add a new (non-default) solution and tab to this card.
        Once added, this object will show up in the list returned by `solution_infos`."""
        has_target_variable = solution.target in datasource.get_variables()
        self._body['content']['evaluationInfo'].append({
            'dataset_id': datasource._data_set_id,
            'datasource_id': datasource.name,
            'search_id': solution.search._id,
            'solution_id': solution._id,
            'hasTargetVariable': has_target_variable
            })
        self._update_card()
        
    @property
    def solution_infos(self):
        """The set of all SolutionInfo objects associated with this card.
        One per solution tab displayed in the UI.
        Note that `solution_infos[0]` is the default card; it may be treated specially by the UI.

        :return: List or tuple of SolutionInfo objects
        """
        return tuple(self.SolutionInfo(self, x) for x in
                     [self._body['content']['originalSolutionInfo']] + self._body['content']['evaluationInfo'])
    ## No setter.  Mutate the returned SolutionInfo objects or use the "add_solution_info" method.

    
